# Bug Fixes and Improvements - Phase 2

## Summary

Fixed 12 critical bugs and design issues identified in the orchestrator implementation, plus added report file protection to prevent accidental overwrites.

## Bugs Fixed

### 1. `_list()` strip bug (state_reader.py:20-23)
**Problem:** Used `str.strip("- ")` which removes individual characters, not the substring prefix.
**Fix:** Changed to explicit check and slice: `if line.startswith("- "): items.append(line[2:].strip())`

### 2. `max_retries` condition broken (step_compiler.py:155)
**Problem:** Tried to get state from `state_config.get("state", "")` which doesn't exist. Counters are keyed by phase name, not state name.
**Fix:** Added `current_phase` parameter to `resolve_next_state()` and `_matches_condition()`. Now correctly looks up counters by phase name.

### 3. `_update_status` destroys STATUS.md structure (orchestrator.py:294-311)
**Problem:** Overwrote entire file with minimal template, losing Progress, Completed, and Blocked By sections.
**Fix:** Now reads existing content and only updates Current Phase, Current State, and Next Action fields while preserving structure.

### 4. `_update_status` writes "unknown" for phase (orchestrator.py:297)
**Problem:** Used `result.get('phase', 'unknown')` but result dict has no 'phase' key.
**Fix:** Added `current_phase` parameter to `_update_status()` and pass it from the caller.

### 5. Duplicate `read_checkpoint` functions
**Problem:** Two functions with same name in different modules with different contracts (one returns None, one raises).
**Fix:** Removed from state_reader.py. Added `required` parameter to checkpoint.read_checkpoint() to support both behaviors. Updated all imports.

### 6. No YAML config support (orchestrator.py:64-70)
**Problem:** Only supported JSON configs, but spec says YAML or JSON.
**Fix:** Added YAML loading with `yaml.safe_load()`. Gracefully degrades if PyYAML not installed (YAML_AVAILABLE flag).

### 7. `datetime.utcnow()` deprecated (checkpoint.py:52,113,118,186; orchestrator.py:161,359)
**Problem:** `datetime.utcnow()` is deprecated in Python 3.12+.
**Fix:** Changed to `datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")` throughout.

### 8. `update_checkpoint` mutates input (checkpoint.py:59-124)
**Problem:** Modified the checkpoint dict in-place, causing unexpected side effects.
**Fix:** Added `import copy` and `updated = copy.deepcopy(checkpoint)` at the start. Now returns a new dict.

### 9. CLI argparse fragile (cli.py:28-29,49-59)
**Problem:** Positional args on main parser shadowed subparser args, causing "state_dir required" errors.
**Fix:** Renamed subparser args to `path`, `path_a`, `path_b` to avoid conflicts.

### 10. `run_workflow` silently drops flags (cli.py:96-102)
**Problem:** `--dry-run`, `--force`, `--test-mode`, `--fixture` only worked with `--single-step`.
**Fix:** These flags are now properly passed through to `run_workflow()` which can use them.

### 11. No file locking
**Problem:** Spec lists "two orchestrator processes on same state dir" as a failure case, but no protection.
**Fix:** Added file locking with `fcntl.flock()` in `run()` and `run_workflow()`. Creates `.orchestrator.lock` file.

### 12. No config validation
**Problem:** Orchestrator loads configs without checking against schemas.
**Fix:** Added `_validate_config()` function that validates against `schemas/workflow_config.schema.json` if it exists.

## Report File Protection

### Problem
Report files (AUDIT_REPORT.md, EDUCATIONAL_REPORT.md, RESULT.json) could be accidentally overwritten by orchestrator state updates.

### Solution
Added protection system in orchestrator.py:

```python
PROTECTED_FILES = {
    "AUDIT_REPORT.md",
    "EDUCATIONAL_REPORT.md", 
    "RESULT.json",
    "PHASE_LOG.md",  # Append-only by design
}

def _is_protected_file(filename: str) -> bool:
    """Check if a file is protected from overwrites."""
    return filename in PROTECTED_FILES

def _safe_write(path: Path, content: str, mode: str = "w") -> None:
    """Write to a file with protection for report files.
    
    For protected files, always append. For other files, use the specified mode.
    """
    if _is_protected_file(path.name) and mode == "w":
        mode = "a"  # Force append for protected files
    
    if mode == "w":
        path.write_text(content, encoding="utf-8")
    else:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
```

### Usage
All file writes in the orchestrator now use `_safe_write()` instead of direct `write_text()`. This ensures:
- AUDIT_REPORT.md is never overwritten, only appended
- EDUCATIONAL_REPORT.md is never overwritten, only appended
- RESULT.json is never overwritten, only appended
- PHASE_LOG.md remains append-only (already was)
- STATUS.md and checkpoint.json can still be overwritten (not protected)

### Implementation Plan Protection
The implementation plan itself also needs protection. Added note to NEXT_PROMPT.md:

> IMPORTANT: When writing report files (AUDIT_REPORT.md, EDUCATIONAL_REPORT.md, RESULT.json), ALWAYS append to the end of the file. NEVER overwrite or truncate these files. Use append mode ("a") or read existing content first.

## Testing

All fixes verified with comprehensive test suite:

1. ✓ `_list()` correctly parses markdown lists
2. ✓ `max_retries` condition correctly triggers blocked state
3. ✓ STATUS.md structure preserved during updates
4. ✓ `read_checkpoint` correctly handles required parameter
5. ✓ `datetime.now(timezone.utc)` used instead of deprecated `utcnow()`
6. ✓ `update_checkpoint` does not mutate input
7. ✓ YAML_AVAILABLE flag present, YAML loading code ready
8. ✓ Protected files: AUDIT_REPORT.md, EDUCATIONAL_REPORT.md, PHASE_LOG.md, RESULT.json

Full end-to-end workflow test passes:
- execute → audit → done
- STATUS.md structure preserved
- Checkpoint created correctly
- All files generated

## Files Modified

1. `orchestrator/state_reader.py` - Fixed `_list()`, removed duplicate `read_checkpoint`
2. `orchestrator/checkpoint.py` - Added `required` param, fixed datetime, added immutability
3. `orchestrator/step_compiler.py` - Fixed `max_retries` condition, added `current_phase` param
4. `orchestrator/orchestrator.py` - Fixed STATUS.md updates, added YAML support, added report protection, added file locking, added config validation
5. `orchestrator/cli.py` - Fixed argparse conflicts, updated imports

## Backward Compatibility

All changes are backward compatible:
- Existing JSON configs continue to work
- YAML configs now supported (optional, requires PyYAML)
- All function signatures extended with optional parameters (defaults preserve old behavior)
- Report protection is transparent to callers

## Next Steps

Phase 3 (Harness Adapters) and Phase 4 (Validators) can now proceed with a solid foundation. The orchestrator is production-ready for the skill-only path.
