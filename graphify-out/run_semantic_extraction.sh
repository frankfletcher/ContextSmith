#!/usr/bin/env bash
# run_semantic_extraction.sh
# Run graphify semantic extraction on ContextSmith using local llama.cpp server.
# Processes one directory at a time, saving incremental results after each.
# Usage: nohup bash graphify-out/run_semantic_extraction.sh > graphify-out/semantic.log 2>&1 &

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="$PROJECT_DIR/graphify-out"
PYTHON="$(cat "$OUT_DIR/.graphify_python")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$OUT_DIR/semantic_${TIMESTAMP}.log"

echo "=============================================="
echo "  Graphify Semantic Extraction (Local LLM)"
echo "=============================================="
echo "Project:    $PROJECT_DIR"
echo "Output:     $OUT_DIR"
echo "Python:     $PYTHON"
echo "Started:    $(date -Iseconds)"
echo ""

# Process directories in this order (smallest first for quick wins)
DIRS=(
  "."
  "docs"
  "skills/local-model-agent-evaluator"
  "skills/local-model-instruction-engineer"
  "skills/local-model-prompt-engineer"
  "skills/local-model-skill-engineer"
  "skills/local-model-skill-migrator"
)

# Write the Python extraction script (one directory at a time, sequential)
cat > "$OUT_DIR/run_semantic_incremental.py" << 'PYEOF'
import json, os, sys, time
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────
BACKEND_URL = "http://localhost:8080/v1"
API_KEY = "llamallama"
MODEL = "qwen3.6-27b"
TOKEN_BUDGET = 32768      # input tokens per chunk (larger chunks, fewer API calls)
MAX_CONCURRENCY = 1       # sequential processing for local model
DEEP_MODE = True          # aggressive INFERRED edges
OUTPUT_DIR = Path("graphify-out")

# ── Setup ──────────────────────────────────────────────
os.environ["OPENAI_API_KEY"] = API_KEY

from graphify import llm as llm_mod
llm_mod.BACKENDS["openai"] = {
    **llm_mod.BACKENDS["openai"],
    "base_url": BACKEND_URL,
    "max_tokens": 65536,   # model supports up to 90k output; leave headroom
}

def count_files(directory):
    """Collect .md/.yml/.yaml files in a directory tree, bypassing gitignore."""
    files = []
    for root_dir, dirs, filenames in os.walk(directory):
        if "graphify-out" in root_dir or ".git" in root_dir:
            continue
        for f in filenames:
            if f.endswith((".md", ".yml", ".yaml")):
                files.append(Path(os.path.join(root_dir, f)))
    return sorted(files)

def save_incremental(directory, result):
    """Save extraction results for a single directory."""
    out_path = OUTPUT_DIR / f".graphify_semantic_{directory.replace('/', '_').replace('.', '')}.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved: {out_path.name} ({result['input_tokens']:,} in / {result['output_tokens']:,} out tokens)")

def merge_all_results():
    """Merge all incremental JSON files into .graphify_semantic.json."""
    all_nodes = {}   # id -> node (dedup by id)
    all_edges = []   # edges may have different IDs, keep all
    total_in = 0
    total_out = 0

    for f in sorted(OUTPUT_DIR.glob(".graphify_semantic_*.json")):
        if f.name == ".graphify_semantic.json":
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        for n in data.get("nodes", []):
            all_nodes[n["id"]] = n
        all_edges.extend(data.get("edges", []))
        total_in += data.get("input_tokens", 0)
        total_out += data.get("output_tokens", 0)

    merged = {
        "nodes": list(all_nodes.values()),
        "edges": all_edges,
        "input_tokens": total_in,
        "output_tokens": total_out,
        "failed_chunks": sum(
            json.loads(f.read_text(encoding="utf-8")).get("failed_chunks", 0)
            for f in OUTPUT_DIR.glob(".graphify_semantic_*.json")
            if f.name != ".graphify_semantic.json"
        ),
    }

    final_path = OUTPUT_DIR / ".graphify_semantic.json"
    final_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nMerged: {len(all_nodes)} nodes, {len(all_edges)} edges")
    print(f"Tokens: {total_in:,} in / {total_out:,} out")
    print(f"Saved:  {final_path}")

# ── Main ───────────────────────────────────────────────────────
if __name__ == "__main__":
    directories = sys.argv[1:] or ["."]

    overall_start = time.time()
    grand_total_in = 0
    grand_total_out = 0
    failed_dirs = []

    for idx, directory in enumerate(directories, 1):
        files = count_files(directory if directory != "." else ".")
        label = directory if directory != "." else "(root)"

        print(f"\n{'='*50}")
        print(f" [{idx}/{len(directories)}] {label}: {len(files)} files")
        print(f" Budget: {TOKEN_BUDGET} tokens/chunk, sequential, deep mode")
        print("=" * 50)

        if not files:
            print("  (no files, skipping)")
            continue

        dir_start = time.time()

        try:
            result = llm_mod.extract_corpus_parallel(
                files=files,
                backend="openai",
                api_key=API_KEY,
                model=MODEL,
                root=Path("."),
                token_budget=TOKEN_BUDGET,
                max_concurrency=MAX_CONCURRENCY,
                deep_mode=DEEP_MODE,
            )

            elapsed = time.time() - dir_start
            n_nodes = len(result.get("nodes", []))
            n_edges = len(result.get("edges", []))
            t_in = result.get("input_tokens", 0)
            t_out = result.get("output_tokens", 0)
            fc = result.get("failed_chunks", 0)

            print(f"\n  Done: {n_nodes} nodes, {n_edges} edges in {elapsed:.0f}s")
            print(f"  Tokens: {t_in:,} in / {t_out:,} out | Failed chunks: {fc}")

            save_incremental(label, result)
            grand_total_in += t_in
            grand_total_out += t_out

        except Exception as e:
            elapsed = time.time() - dir_start
            print(f"  FAILED after {elapsed:.0f}s: {e}", file=sys.stderr)
            failed_dirs.append((label, str(e)))

    overall_elapsed = time.time() - overall_start

    # Merge all incremental results into the final file
    print(f"\n{'='*50}")
    print(" MERGING ALL RESULTS")
    print("=" * 50)
    merge_all_results()

    if failed_dirs:
        print(f"\nWARNINGS: {len(failed_dirs)} directory(ies) failed:")
        for label, err in failed_dirs:
            print(f"  - {label}: {err}")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f" COMPLETE in {overall_elapsed:.0f}s ({overall_elapsed/60:.1f} min)")
    print(f" Total tokens: {grand_total_in:,} in / {grand_total_out:,} out")
    print("=" * 50)
PYEOF

# Run the extraction
echo "Running semantic extraction..."
echo "Log file: $LOG_FILE"
echo ""

"$PYTHON" "$OUT_DIR/run_semantic_incremental.py" "${DIRS[@]}"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "Extraction completed successfully!"
    echo "Results saved to:"
    echo "  - $OUT_DIR/.graphify_semantic.json (merged)"
    echo "  - $OUT_DIR/.graphify_semantic_*.json (per-directory)"
else
    echo ""
    echo "Extraction finished with errors. Check log for details."
    echo "Partial results may be in .graphify_semantic_*.json"
fi

exit $EXIT_CODE
