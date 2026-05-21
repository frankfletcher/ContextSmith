# Small-Model Atomicity

Smaller/local models often need more explicit, atomic execution steps than frontier hosted models. Add detail where it reduces inference burden.

## Atomic Instruction Pattern

Convert abstract instructions into executable micro-steps.

Weak:

```text
Run a semantic diff.
```

Better:

```text
1. List source behaviors.
2. For each behavior, find the matching output behavior.
3. Mark preserved, changed, removed, or added.
4. Explain every changed/removed/added behavior.
5. Revise if a change lacks justification.
```

## Use Atomicity For

- validation gates
- file edits
- semantic preservation
- context inspection
- tool use
- side-effect boundaries
- long-running phases
- structured output generation

## Avoid

- vague verbs without stop conditions
- hidden assumptions
- “be careful” instructions without concrete checks
- very broad phases for complex work
