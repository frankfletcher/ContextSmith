#!/usr/bin/env python3
"""Merge semantic extraction results into existing structural graph, rebuild communities, regenerate HTML + report."""

import json, os, sys, time
from pathlib import Path

os.environ["OPENAI_API_KEY"] = "llamallama"

from graphify import llm as llm_mod
llm_mod.BACKENDS["openai"] = {
    **llm_mod.BACKENDS["openai"],
    "base_url": "http://localhost:8080/v1",
    "max_tokens": 65536,
}

from graphify.build import build_merge
from graphify.cluster import cluster as detect_communities
from graphify.export import to_html, to_json
from graphify.report import generate as generate_report
from graphify.cluster import cohesion_score

OUT = Path("graphify-out")
GRAPH_PATH = OUT / "graph.json"
SEMANTIC_PATH = OUT / ".graphify_semantic.json"
LABELS_PATH = OUT / ".graphify_labels.json"
COST_PATH = OUT / "cost.json"

# ── Step 1: Load semantic data ───────────────────────────────────────
print("Loading semantic extraction results...")
semantic = json.loads(SEMANTIC_PATH.read_text(encoding="utf-8"))
print(f"  {len(semantic['nodes'])} nodes, {len(semantic['edges'])} edges")

# ── Step 2: Merge into existing graph ────────────────────────────────
print("Merging with structural graph...")
G = build_merge(
    new_chunks=[semantic],
    graph_path=GRAPH_PATH,
    directed=False,
    dedup=True,
)
print(f"  Merged graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Save merged graph to disk (build_merge returns but doesn't write)
to_json(G, {}, str(GRAPH_PATH), force=True)
print("  Saved: graph.json")

# ── Step 3: Detect communities ───────────────────────────────────────
print("Detecting communities (Leiden)...")
communities = detect_communities(G, resolution=1.0)
print(f"  Found {len(communities)} communities")

# Note: community ID remapping skipped for first merge (IDs will shift, labels re-generated below)

# ── Step 4: Generate community labels via LLM ────────────────────────
print("Labeling communities...")
from collections import Counter

labels = {}
for cid, members in communities.items():
    # Simple heuristic label from most common file prefix / node label
    prefixes = []
    for nid in members:
        data = G.nodes[nid]
        src = data.get("source_file", "") or ""
        if "/" in src:
            prefixes.append("/".join(src.split("/")[:2]))
        elif src:
            prefixes.append(src.split(".")[0][:30])
    if prefixes:
        top = Counter(prefixes).most_common(1)[0][0]
        labels[cid] = top.replace("/", "_")[:40]

LABELS_PATH.write_text(json.dumps(labels, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"  Saved {len(labels)} community labels")

# ── Step 5: Generate HTML visualization ──────────────────────────────
print("Generating HTML visualization...")
to_html(
    G=G,
    communities=communities,
    output_path=str(OUT / "graph.html"),
    community_labels={int(k): v for k, v in labels.items()},
)
print("  Saved: graph.html")

# ── Step 6: Generate report ──────────────────────────────────────────
print("Generating audit report...")
cohesion = {cid: cohesion_score(G, members) for cid, members in communities.items()}

# Top hub nodes
degree_sorted = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:20]
god_nodes = [
    {"node": nid, "label": G.nodes[nid].get("label", nid), "degree": deg, "type": "hub"}
    for nid, deg in degree_sorted[:10]
]

# Edge type distribution
edge_types = Counter()
for u, v, d in G.edges(data=True):
    edge_types[d.get("relation", "unknown")] += 1

surprise = []
# Count files and words in the corpus for report metadata
import os as _os
total_files = 0
total_words = 0
for root_dir, dirs, files in _os.walk("."):
    if "graphify-out" in root_dir or ".git" in root_dir:
        continue
    for f in files:
        if f.endswith((".md", ".yml", ".yaml")):
            total_files += 1
            try:
                fp = _os.path.join(root_dir, f)
                total_words += len(open(fp).read().split())
            except Exception:
                pass

detection_result = {
    "algorithm": "leiden",
    "resolution": 1.0,
    "n_communities": len(communities),
    "total_files": total_files,
    "total_words": total_words,
}
token_cost = {
    "input_tokens": semantic.get("input_tokens", 0),
    "output_tokens": semantic.get("output_tokens", 0),
}

report = generate_report(
    G=G,
    communities=communities,
    cohesion_scores=cohesion,
    community_labels={int(k): v for k, v in labels.items()},
    god_node_list=god_nodes,
    surprise_list=surprise,
    detection_result=detection_result,
    token_cost=token_cost,
    root=str(Path(".").resolve()),
)

REPORT_PATH = OUT / "GRAPH_REPORT.md"
REPORT_PATH.write_text(report, encoding="utf-8")
print(f"  Saved: GRAPH_REPORT.md ({len(report)} chars)")

# ── Step 7: Update cost tracker ──────────────────────────────────────
if COST_PATH.exists():
    cost = json.loads(COST_PATH.read_text(encoding="utf-8"))
else:
    cost = {"runs": []}

cost["runs"].append({
    "type": "semantic_merge",
    "input_tokens": semantic.get("input_tokens", 0),
    "output_tokens": semantic.get("output_tokens", 0),
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
})

COST_PATH.write_text(json.dumps(cost, indent=2), encoding="utf-8")

# ── Summary ──────────────────────────────────────────────────────────
print(f"\nDone!")
print(f"  Graph:     {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
print(f"  Communties: {len(communities)}")
print(f"  Artifacts: graph.json, graph.html, GRAPH_REPORT.md, .graphify_labels.json")
