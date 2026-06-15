# Complexity Gate

This is a **reactive** check — it catches complexity after writing. For **proactive** prevention (how to write simple code that never triggers this gate), see the **Write Simple Code First** section in `shared/coding-standards.md`.

After any Python changes, run these checks and refactor until complexity is ≤ B:

```bash
uvx radon cc <path> -s -a | grep -E " - [CDEF] "
uvx radon mi <path> -s | grep -E " - [BCDEF] "
```

## Cyclomatic Complexity (radon cc)

| Grade | Range | Meaning |
| ------- | ------- | --------- |
| A | 1-5 | Low complexity |
| B | 6-10 | Moderate complexity |
| C | 11-20 | Complex — must refactor |
| D | 21-30 | Very complex |
| F | 31+ | Extremely complex |

**Target:** All touched functions ≤ B.

## Maintainability Index (radon mi)

| Grade | Range | Meaning |
| ------- | ------- | --------- |
| A | 20-100 | Highly maintainable |
| B | 10-19 | Moderately maintainable |
| C | 0-9 | Difficult to maintain |

**Target:** All touched files ≥ A.

## Enforced Workflow

1. After modifying Python code, run `uvx radon cc` and `uvx radon mi` on the changed files.
2. If any touched function is C/D/E/F, refactor it until it is A or B.
3. If any touched file is B/C, refactor until it is A.
4. Run lint, format, and tests after each refactoring pass.
5. Report before-and-after scores.
