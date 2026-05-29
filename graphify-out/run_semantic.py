import json, os, sys, time
from pathlib import Path
from graphify.llm import extract_corpus_parallel

# Build file list (bypasses gitignore)
filtered_files = []
for root_dir, dirs, files in os.walk('.'):
    if 'graphify-out' in root_dir or '.git' in root_dir:
        continue
    for f in files:
        if f.endswith(('.md', '.yml', '.yaml')):
            rel = os.path.join(root_dir, f)
            parts = rel.lstrip('./').split('/')
            if len(parts) == 1 or parts[0] in ('skills', 'docs'):
                filtered_files.append(Path(rel))

# Monkey-patch openai backend to use llama.cpp server with higher max_tokens
from graphify import llm as llm_mod
llm_mod.BACKENDS['openai'] = {
    **llm_mod.BACKENDS['openai'],
    'base_url': 'http://localhost:8080/v1',
    'max_tokens': 32768,  # higher limit for large responses
}

os.environ['OPENAI_API_KEY'] = 'llamallama'

completed = [0]
failed = [0]

def on_chunk_done(idx, total, chunk_result):
    if chunk_result is None:
        failed[0] += 1
        print(f'  Chunk {idx+1}/{total}: FAILED')
    else:
        completed[0] += 1
        n_nodes = len(chunk_result.get('nodes', []))
        n_edges = len(chunk_result.get('edges', []))
        t_in = chunk_result.get('input_tokens', 0)
        t_out = chunk_result.get('output_tokens', 0)
        elapsed = time.time() - start_time
        print(f'  Chunk {idx+1}/{total}: {n_nodes} nodes, {n_edges} edges ({t_in:,} in / {t_out:,} out tokens) [{elapsed:.0f}s total]')

print(f'Semantic extraction: {len(filtered_files)} files')
print('Backend: openai patched to localhost:8080/v1, model: qwen3.6-27b')
print('Budget: 16k tokens/chunk, sequential, max_tokens: 32k, deep mode: on')
print()

start_time = time.time()

result = extract_corpus_parallel(
    files=filtered_files,
    backend='openai',
    api_key='llamallama',
    model='qwen3.6-27b',
    root=Path('.'),
    token_budget=16384,  # smaller chunks → faster per-chunk inference
    max_concurrency=1,   # sequential to avoid overwhelming the server
    deep_mode=True,
    on_chunk_done=on_chunk_done,
)

elapsed = time.time() - start_time
print(f'\nTotal time: {elapsed:.0f}s')
print(f'Result: {len(result["nodes"])} nodes, {len(result["edges"])} edges')
print(f'Tokens: {result.get("input_tokens",0):,} in / {result.get("output_tokens",0):,} out')
print(f'Failed chunks: {result.get("failed_chunks", 0)}')

Path('graphify-out/.graphify_semantic.json').write_text(
    json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8'
)
print('Saved to .graphify_semantic.json')