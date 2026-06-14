"""Step compiler.

Compiles StepContract from config + state + plan. Implements state transition logic.
"""

from orchestrator.adapters.base import StepContract


def compile_step_contract(
    state: str,
    config: dict,
    plan: dict,
    context: dict,
    current_subphase: str = "",
) -> StepContract:
    """Compile a StepContract from config, plan, and context.

    Args:
        state: Current state machine state
        config: Workflow config dict
        plan: Parsed plan dict from state_reader
        context: Parsed context dict from state_reader

    Returns:
        StepContract with all required fields populated
    """
    # Get state config from workflow config
    state_config = config.get("states", {}).get(state, {})

    # Extract values with defaults
    agent_profile = state_config.get("agent", "contextsmith-default")
    permissions = state_config.get("permissions", "read-only")
    timeout_s = state_config.get("timeout_s", 300)
    max_retries = state_config.get("max_retries", 3)
    ralph_max_cycles = state_config.get("ralph_max_cycles", 0)
    validation_mode = state_config.get("validation_mode", "strict")
    model_pin = state_config.get("model_pin")
    checkpoint_before_run = state_config.get("checkpoint_before_run", False)
    prompt_template = state_config.get("prompt_template")

    # Get inputs and expected outputs from state config
    inputs = state_config.get("inputs", [])
    expected_outputs = state_config.get("expected_outputs", [])

    # Generate step_id from workflow_id and state
    workflow_id = config.get("workflow_id", "unknown")
    step_id = f"{workflow_id}-{state}"

    # Extract sub-phase metadata from plan if available
    subphase_name = current_subphase
    subphase_budget = _extract_subphase_budget(plan, current_subphase)

    return StepContract(
        step_id=step_id,
        state=state,
        agent_profile=agent_profile,
        permissions=permissions,
        inputs=inputs,
        expected_outputs=expected_outputs,
        timeout_s=timeout_s,
        max_retries=max_retries,
        ralph_max_cycles=ralph_max_cycles,
        validation_mode=validation_mode,
        model_pin=model_pin,
        checkpoint_before_run=checkpoint_before_run,
        prompt_template=prompt_template,
        workflow_id=workflow_id,
        subphase_name=subphase_name,
        subphase_context_budget=subphase_budget,
    )


def _extract_subphase_budget(plan: dict, subphase_name: str) -> int:
    """Extract context budget from a sub-phase in the plan.

    Searches all phases for a sub-phase whose name contains subphase_name.
    Returns the parsed Context Budget in tokens, or 0 if not found/not set.
    """
    if not subphase_name or not plan:
        return 0

    for phase in plan.get("phases", []):
        for sp in phase.get("subphases", []):
            if _name_matches(sp.get("name", ""), subphase_name):
                raw = sp.get("metadata", {}).get("Context Budget", "0")
                raw = str(raw).lower().replace(",", "").replace("_", "")
                multiplier = 1
                if "k" in raw:
                    multiplier = 1000
                    raw = raw.replace("k", "")
                try:
                    return int(float(raw) * multiplier)
                except ValueError, TypeError:
                    return 0

    return 0


def _name_matches(plan_name: str, search: str) -> bool:
    """Check if a plan sub-phase name matches the search term."""
    if not plan_name or not search:
        return False
    return search in plan_name or plan_name.startswith(search)


def resolve_next_state(
    current: str,
    current_phase: str,
    result: dict,
    validation: dict,
    config: dict,
    counters: dict,
) -> str:
    """Deterministic state transition.

    The orchestrator owns all state transitions. The agent's RESULT.json
    provides evidence of completion (status, artifacts), but the orchestrator
    alone decides the next state by matching transition conditions from the
    workflow config against that evidence.

    Rule: Agent output is evidence, not authority. The agent never chooses
    its next state. If no transition condition matches, the orchestrator
    transitions to 'blocked', not to whatever the agent requested.

    Args:
        current: Current state machine state
        current_phase: Current phase identifier (e.g., "phase_1")
        result: Step execution result dict (status only, next_action is ignored)
        validation: Validation result dict
        config: Workflow config dict
        counters: Current counter values for this phase

    Returns:
        Next state machine state
    """
    # Get state config from workflow config
    state_config = config.get("states", {}).get(current, {})
    transitions = state_config.get("transitions", [])

    # Check each transition condition in order
    for transition in transitions:
        condition = transition.get("condition", "")
        target = transition.get("target", "")

        if _matches_condition(
            condition,
            current,
            current_phase,
            result,
            validation,
            counters,
            state_config,
        ):
            # Check if this is a retry and we've exceeded max retries
            if target == current:  # retry to same state
                current_retries = counters.get(current_phase, {}).get("retries", 0)
                max_retries = state_config.get("max_retries", 3)
                if current_retries >= max_retries:
                    # Exceeded max retries, go to blocked
                    return "blocked"

            return target

    # No matching transition found
    return "blocked"


def _matches_condition(
    condition: str,
    current_state: str,
    current_phase: str,
    result: dict,
    validation: dict,
    counters: dict,
    state_config: dict,
) -> bool:
    """Check if a transition condition matches the result and validation.

    Args:
        condition: Condition string from config
        current_state: Current state machine state
        current_phase: Current phase identifier
        result: Step execution result dict
        validation: Validation result dict
        counters: Current counter values
        state_config: State configuration dict

    Returns:
        True if condition matches, False otherwise
    """
    # Handle common conditions
    if condition == "output_valid":
        return validation.get("passed", False)

    if condition == "output_invalid":
        return not validation.get("passed", False)

    if condition == "pass":
        return result.get("status", "").lower() == "pass"

    if condition == "fail":
        return result.get("status", "").lower() == "fail"

    if condition == "max_retries":
        current_retries = counters.get(current_phase, {}).get("retries", 0)
        max_retries = state_config.get("max_retries", 3)
        return current_retries >= max_retries

    if condition == "always":
        return True

    if condition == "never":
        return False

    # Handle Ralph-specific conditions
    if condition == "ralph_complete":
        ralph_cycles = counters.get(current_phase, {}).get("ralph_cycles", 0)
        ralph_max = state_config.get("ralph_max_cycles", 0)
        return ralph_cycles >= ralph_max

    if condition == "ralph_incomplete":
        ralph_cycles = counters.get(current_phase, {}).get("ralph_cycles", 0)
        ralph_max = state_config.get("ralph_max_cycles", 0)
        return ralph_cycles < ralph_max

    # Unknown condition - treat as not matched
    return False
