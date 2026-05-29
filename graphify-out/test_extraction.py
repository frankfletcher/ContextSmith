import json, os, sys, glob as globmod
from pathlib import Path
from graphify.llm import extract_corpus_parallel, extract_files_direct

# Build file list manually (bypasses gitignore)
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

print(f'Files: {len(filtered_files)}')

# Test 1: ollama backend with OLLAMA_BASE_URL
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:8080/v1'
os.environ['OLLAMA_API_KEY'] = 'llamallama'

print('\nTest 1: ollama backend')
try:
    r1 = extract_files_direct([filtered_files[0]], backend='ollama', api_key='llamallama', model='qwen3.6-27b', root=Path('.'), deep_mode=True)
    print(f'  OK: {len(r1.get("nodes",[]))} nodes, {len(r1.get("edges",[]))} edges')
except Exception as e:
    print(f'  FAILED: {e}')

# Test 2: openai backend with monkey-patched base_url
from graphify import llm as llm_mod
llm_mod.BACKENDS['openai'] = {**llm_mod.BACKENDS['openai'], 'base_url': 'http://localhost:8080/v1'}

os.environ['OPENAI_API_KEY'] = 'llamallama'

print('\nTest 2: openai backend (patched base_url)')
try:
    r2 = extract_files_direct([filtered_files[0]], backend='openai', api_key='llamallama', model='qwen3.6-27b', root=Path('.'), deep_mode=True)
    print(f'  OK: {len(r2.get("nodes",[]))} nodes, {len(r2.get("edges",[]))} edges')
except Exception as e:
    print(f'  FAILED: {e}')
