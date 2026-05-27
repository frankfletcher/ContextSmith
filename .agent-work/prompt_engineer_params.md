# Local Model Prompt Engineer — Parameter Reference Table

| Parameter | Sub-Params / Options | Default | Description |
|---|---|---|---|
| **`coding_standards`** | `off`, `generic`, `python` (PEP 8, type hints, uv), `javascript_typescript` (linter/formatter, TS types), `repo_aware` (scan existing conventions first) | `off` | Coding standards injection for agent instructions |
| **`context_strategy`** | `none`, `file_based_workflow`, `graph_index_pattern`, `long_input_pattern` | auto-selected based on source mode | Context management approach |
| **`domain`** | `coding`, `data_science_ml`, `research`, `writing`, `email`, `calendar`, `purchasing_tickets`, `travel`, `documents`, `automation`, `finance_legal_medical`, `personal_knowledge`, `creative` | inferred from prompt | Domain and intent detection |
| **`educational_report`** | `off`, `on` | `on` (default) | Educational change report with strengths, weaknesses, changes, reliability improvements, remaining risks |
| **`engineering_metadata_fields`** | `engineered_by`, `engineer_version`, `target_model_profile`, `optimization_scope`, `runtime_settings_controllable`, `last_engineered_date` | auto-populated where applicable | Metadata fields for generated artifacts |
| **`escalation_strings`** | `BREAK_LOOP_AWAITING_HUMAN_INPUT`, `BLOCKED_MISSING_CONTEXT`, `BLOCKED_TOOL_UNAVAILABLE`, `BLOCKED_PERMISSION_REQUIRED`, `BLOCKED_VALIDATION_UNAVAILABLE`, `BLOCKED_GIT_STATE_REQUIRES_HUMAN_INPUT` | all available | Explicit stop strings for blocked states |
| **`evaluation_dimensions`** | `small_model_atomicity`, `instruction_clarity`, `output_contract_quality`, `context_strategy`, `assumption_control`, `domain_fit`, `validation_strength`, `loop_safety`, `git_file_safety`, `bloat_cognitive_load`, `progressive_disclosure`, `testability` | all enabled for reusable prompts | Quality evaluation rubrics (A-F scale) |
| **`git_safety`** | `off`, `on`, `auto` | `auto` (added when coding/repo prompt detected) | Git/file safety controls |
| **`instruction_conflict_detection`** | `off`, `on`, `auto` | `auto` (added when multiple instruction sources exist) | Detect conflicting instructions and apply resolution order |
| **`instruction_deduplication`** | `off`, `on`, `auto` | `auto` (added when editing instruction files in scope) | Scan and de-duplicate existing instructions across files |
| **`instruction_files_to_scan`** | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`, `.windsurfrules`, `.cursor/rules/*`, `.continue/config.*`, `.aider.conf.yml`, harness-specific files | all scanned when deduplication is on | Files checked for instruction deduplication |
| **`interaction_mode`** | `yolo`, `guided`, `review_gate`, `audit_only`, `stage_apply` | inferred from side effect tier | How the agent interacts with the user |
| **`interaction_type`** | `one_shot`, `reusable`, `long_running`, `agentic` | `one_shot` | How the prompt will be used |
| **`loop_safety`** | `off`, `on`, `auto` | `auto` (added when tool-using prompt detected) | Agentic loop safety controls |
| **`merge_policy_priority`** | `1. preserve_clear_safeguards`, `2. strengthen_vague_safeguards`, `3. consolidate_duplicates`, `4. add_missing_safeguards`, `5. avoid_cross_file_repetition` | priority order 1→5 | Order of precedence when merging safeguards |
| **`output_format`** | `text`, `json`, `schema`, `instruction_file`, `prompt_package` | `text` | Desired output format |
| **`output_location`** | `user_specified`, `project_agent_work`, `skill_package_agent_work`, `user_level_agent_work`, `tmp_disposable_only` | `project .agent-work/` (default for project-based work) | Where to write output files and reports |
| **`phase_compression`** | `off`, `on`, `auto` | `auto` (enabled when phased planning is on) | Phase closeout and debrief with carry-forward rules |
| **`phase_files`** | `TASK.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `CONTEXT.md`, `CHECKLIST.md`, `ARTIFACTS.md`, `PHASE_LOG.md`, `NEXT_PROMPT.md` | all created when persistent state is on | Persistent state file types and their responsibilities |
| **`phase_granularity`** | `6-12 phases for complex tasks`, `goal/inputs/tasks/outputs/validation/stop_condition/handoff_notes per phase` | scales with complexity | Phase count and structure requirements |
| **`phase_planning`** | `off`, `on`, `auto` | `auto` (added when long-running task detected) | Phased planning for complex work |
| **`persistent_state`** | `off`, `on`, `auto` | `auto` (added when crash-sensitive or multi-phase work detected) | Persistent task state tracking via `.agent-work/` |
| **`prompt_package_sections`** | `engineering_metadata`, `assumptions`, `target_model_harness_profile`, `domain_intent`, `prompt_control_feasibility`, `context_strategy`, `interaction_mode`, `system_prompt`, `user_prompt_template`, `examples`, `validation_test_plan`, `loop_git_file_safety`, `persistent_task_state`, `subagent_delegation`, `runtime_recommendations`, `educational_change_report` | all included unless user requests otherwise | Output sections in the generated prompt package |
| **`ralph_loop`** | `off`, `on` (bounded iteration), `requested` (user explicitly requests) | `off` | Ralph improvement loop with A-F grading |
| **`ralph_loop_limits`** | `max_iterations: 2 (default)`, `hard_max: 3`, `stop_if_all_B_or_better`, `stop_if_cosmetic_only` | defaults shown | Iteration limits for Ralph improvement loop |
| **`recommendation_labels`** | `ship`, `iterate`, `ask_user`, `reject` | auto-selected after evaluation | Final recommendation after evaluation |
| **`recovery_types`** | `correct`, `narrow`, `inspect`, `substitute`, `escalate` | all available | Recovery strategy options after failure |
| **`reference_optimization`** | `off`, `on`, `auto` | `auto` (added when skill package references need optimization) | Reference file classification and optimization (behavioral/template/profile/example/archive) |
| **`retry_budget`** | `max_retries_per_action: 1`, `max_related_attempts_per_strategy: 2`, `max_total_recovery_attempts: 3` | defaults shown | Retry budget configuration for loop safety |
| **`side_effect_tier`** | `read_only`, `local_reversible_write`, `local_risky_write`, `destructive_local`, `external_write`, `financial_purchasing`, `identity_auth_secrets`, `production_deployment` | inferred | Side-effect risk level (from side-effect matrix) |
| **`source_mode`** | `short_direct_input`, `pasted_long_input`, `file_path`, `folder_repository`, `retrieved_rag_context`, `tool_output`, `graph_index_provider`, `multi_turn_agent_state` | inferred | Context source mode classification |
| **`subagent_delegation`** | `off`, `on`, `auto` | `auto` (added when many files, large logs, or high-risk validation detected) | Subagent delegation rules and patterns |
| **`target_model`** | `generic-local`, `qwen36`, `llama2`, `llama3`, `llama3.1`, `gemma`, `mistral`, `phi`, `deepseek` | `generic-local` | Target model profile for optimization |
| **`ui_standards`** | `off`, `on`, `auto` | `auto` (added when frontend/UI code detected) | UI/UX standards: accessibility, consistency, no emojis, responsive validation |
| **`validation_dimensions`** | `small_model_atomicity`, `instruction_clarity`, `output_contract`, `context_strategy`, `assumption_control`, `domain_fit`, `validation_strength`, `loop_safety`, `git_file_safety`, `bloat_cognitive_load`, `progressive_disclosure`, `testability` | all evaluated for reusable prompts | A-F graded quality dimensions |
