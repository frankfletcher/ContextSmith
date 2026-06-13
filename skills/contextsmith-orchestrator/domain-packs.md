# Domain Packs

Domain packs define what refinement, validation, self-audit, Ralph critique, and evidence mean for different work.

## Domain Router

Classify from the prompt, file paths, project evidence, and user parameters. If ambiguous and `--interaction refine` is active, ask which domain applies.

Supported domains:

- software-engineering
- frontend-ux
- data-analytics
- data-science-ml
- ai-ml-engineering
- research
- writing-editing
- business-strategy
- education-tutoring
- ops-devops
- legal-policy-compliance
- general-task

## Software Engineering

Refinement priorities:

- scope boundary
- test/build/lint expectations
- compatibility and migration tolerance
- file-editing permission

Validation:

- run available tests, lint, build, typecheck, or project validation
- record commands and results
- preserve unrelated user changes

Self-audit lens:

- behavior correctness
- regression risk
- missing tests
- file safety and Git safety

Ralph lens:

- Does the change satisfy the exact request without expanding scope?
- Are tests or validation strong enough to catch regressions?
- Did the run preserve unrelated user changes?

## Frontend UX

Refinement questions:

```markdown
1. Which frontend stack should I target?
- Existing project stack (Recommended when detected)
- React
- Next.js
- Vue
- Svelte
- Plain HTML/CSS/JS

2. What styling approach should I use?
- Existing design system (Recommended when detected)
- Tailwind CSS
- CSS Modules
- Plain CSS
- Styled components

3. What should I optimize for?
- Production maintainability (Recommended)
- Visual polish
- Fast prototype
- Accessibility-first
- Minimal dependencies
```

Validation:

- build and lint when available
- responsive behavior check when feasible
- accessibility and keyboard basics
- design-system consistency

Self-audit lens:

- did not assume React/Tailwind/shadcn without evidence
- mobile and desktop behavior considered
- visual hierarchy and interaction states are explicit

Ralph lens:

- Did the run use the chosen or existing stack consistently?
- Are accessibility, responsive behavior, and interaction states covered?
- Is the UI maintainable within the existing design system?

## Data Analytics

Refinement questions:

```markdown
1. What output do you want?
- Executive summary
- Charts or dashboard
- SQL query
- Notebook-style analysis
- Cleaned dataset

2. What should I prioritize?
- Accuracy (Recommended)
- Business insight
- Clear visuals
- Reproducibility
- Fast exploratory answer
```

Validation:

- schema and row-count checks
- calculation sanity checks
- missing-value and outlier notes
- reproducible query or script when relevant

Self-audit lens:

- calculations match data
- assumptions are named
- charts support the claim
- no unsupported causal claims

Ralph lens:

- Are calculations and aggregations defensible from the available data?
- Are business interpretations separated from measured facts?
- Would a reader know what data quality limits apply?

## Data Science And ML

Refinement questions:

```markdown
1. What kind of work is this?
- Data analysis / reporting
- Predictive modeling
- Model evaluation
- Experiment design
- Feature engineering

2. What should be optimized?
- Interpretability
- Accuracy
- Reproducibility (Recommended)
- Speed
- Low compute cost

3. What validation evidence is required?
- Summary statistics only
- Train/test evaluation
- Cross-validation
- Error analysis
- Reproducible notebook or script
```

Validation:

- leakage check
- baseline comparison
- appropriate metric selection
- seed/reproducibility note
- train/test split or cross-validation when modeling

Self-audit lens:

- metric matches objective
- leakage risks addressed
- uncertainty and limitations stated
- compute and data constraints respected

Ralph lens:

- Is there a baseline or clear reason no baseline is available?
- Are leakage, metric choice, and reproducibility addressed?
- Are limitations stated without overstating model quality?

## AI/ML Engineering

Refinement priorities:

- RAG, agent, prompt, eval, fine-tuning, or serving scope
- target model/provider
- latency, cost, and reliability constraints
- eval dataset and failure modes

Validation:

- prompt/eval cases
- retrieval quality checks
- hallucination and citation checks when RAG is involved
- latency/cost notes when serving is involved

Self-audit lens:

- target model constraints enforced
- evals test likely failures
- no hidden chain-of-thought requested
- safety and privacy boundaries stated

Ralph lens:

- Do evals cover likely failure modes rather than happy paths only?
- Are model, latency, cost, privacy, and safety constraints explicit?
- Does the run avoid hidden chain-of-thought or unsafe data handling?

## Research

Refinement questions:

```markdown
1. What kind of research output do you want?
- Quick answer
- Comparison table
- Source-backed brief (Recommended)
- Deep report
- Decision recommendation

2. What source quality should I require?
- Official sources only
- Recent sources preferred
- Academic or technical sources
- Broad web coverage
- User-provided sources only

3. How should uncertainty be handled?
- Cite uncertainty explicitly (Recommended)
- Give best-effort answer
- Separate facts from interpretation
- Ask before using weak sources
```

Validation:

- source quality and recency
- claim/source alignment
- conflicting evidence noted
- uncertainty separated from facts

Self-audit lens:

- no uncited factual claims when citations are required
- sources are appropriate for the decision
- missing evidence is disclosed

Ralph lens:

- Are important claims supported by appropriate sources?
- Are source recency, conflicts, and uncertainty handled clearly?
- Does the conclusion overreach beyond the evidence?

## Writing And Editing

Refinement questions:

```markdown
1. What tone should I target?
- Warm and concise
- Professional and direct (Recommended)
- Diplomatic
- Assertive
- Friendly casual

2. What should I preserve?
- Exact meaning (Recommended)
- Main ask only
- Sender's voice
- Politeness
- Brevity

3. What output do you want?
- One polished version
- Three variants
- Subject line plus body
- Critique first, then rewrite
```

Validation:

- meaning preservation
- tone match
- no invented facts, promises, dates, or commitments
- audience fit

Self-audit lens:

- intent preserved
- unnecessary verbosity removed
- voice and constraints followed

Ralph lens:

- Does the rewrite preserve facts, commitments, and intent?
- Does the tone match the selected audience and goal?
- Did the run avoid adding context the user did not provide?

## Business Strategy

Validation:

- assumptions named
- decision criteria explicit
- risks and tradeoffs included
- recommendation tied to evidence

Self-audit lens:

- separates facts from judgment
- no unsupported certainty
- next steps are practical

Ralph lens:

- Are assumptions, tradeoffs, and risks explicit?
- Is the recommendation tied to criteria and evidence?
- Are next steps actionable for the intended audience?

## Education And Tutoring

Validation:

- explanation matches learner level
- examples are correct
- common misconceptions addressed
- practice or check-for-understanding included when requested

Self-audit lens:

- not overcomplicated
- no hidden reasoning exposure
- answer teaches the requested concept

Ralph lens:

- Does the explanation match the learner's level?
- Are examples correct and useful?
- Are likely misconceptions addressed without overloading the learner?

## Ops And DevOps

Validation:

- environment and deployment target clear
- secrets and credentials not exposed
- rollback and observability considered
- commands are safe or approval-gated

Self-audit lens:

- irreversible actions gated
- production risks named
- verification and rollback explicit

Ralph lens:

- Are destructive or production-impacting steps approval-gated?
- Are rollback, monitoring, and verification concrete?
- Are secrets and environment assumptions handled safely?

## Legal, Policy, And Compliance

Validation:

- jurisdiction or policy source boundaries stated
- non-lawyer/non-professional caveat when needed
- risks separated from recommendations
- source support for claims when applicable

Self-audit lens:

- avoids definitive legal advice unless user provided qualified source
- uncertainty and escalation paths included

Ralph lens:

- Are jurisdiction, policy source, and authority boundaries clear?
- Are risks framed without pretending to give legal advice?
- Are escalation or professional-review paths stated when needed?

## General Task

Use generic refinement and validation. If the run becomes domain-specific during execution, switch to the relevant domain pack and record the switch.

Ralph lens:

- Did the run satisfy the user's stated goal?
- Were material assumptions named or resolved?
- Is the final output usable without hidden context?
