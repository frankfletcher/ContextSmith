# CONTEXT.md

## Repo Map
```
ContextSmith/
├── shared/                           # 52 canonical reference files (35 root + 8 domain-profiles/ + 4 model-profiles/)
├── skills/
│   ├── local-model-prompt-engineer/  # 53 ref files (52 shared copies + help.md)
│   ├── local-model-skill-engineer/   # 53 ref files (same set)
│   ├── local-model-skill-migrator/   # 53 ref files (same set)
│   ├── local-model-instruction-engineer/  # 53 ref files (same set)
│   └── local-model-agent-evaluator/  # 53 ref files (same set)
├── scripts/
│   └── validate_skills.py           # 40 lines, checks SKILL.md frontmatter + refs/ existence
├── .gitignore                        # Empty (0 bytes)
└── .github/                          # Does not exist
```

## Key Facts
- **No version metadata** in any shared file — use git blob hashes for versioning
- **All 5 skills** have identical reference file sets (52 shared + 1 help.md)
- **help.md** is skill-local (NOT in shared/) and currently lives in references/
- **8 domain-profiles/**, **4 model-profiles/** in subdirectories
- **CONTRIBUTING.md** does not exist
- **.gitignore** is empty
- **No CI** exists

## Skip Rules
- Do NOT modify any SKILL.md file
- Do NOT modify any file in shared/
- Do NOT add new dependencies beyond PyYAML
- Do NOT run git add/commit/push without approval

## Shared File Blob Hashes (Reference Table)
| File | Blob Hash |
|---|---|
| shared/coding-standards.md | 14484e29d3eec2cb591f8f1aeb1dbfa3a36b9a4b |
| shared/context-management.md | 6e7d2dafcf947ef4305060efc8ce2b2d95682e14 |
| shared/control-parameters.md | d65cd90034824c859658ed83efa6e019201e3ab9 |
| shared/control-phrases.md | 7699947de82e57474c89c3e0d2df069efafafc41 |
| shared/documentation-quality.md | fe5be97e08f59cff8efff178fa40c9da6518a082 |
| shared/domain-intent.md | 320def729d99d3d9a69ad854b055a14b1f511497 |
| shared/domain-profiles/ai-modalities.md | 5c9033caac419850711ecb8a1deaafc9f626c3e3 |
| shared/domain-profiles/coding.md | 7403afd9f32001ffec5b1f5a3ba4a88cf687d26f |
| shared/domain-profiles/data-science-ml.md | 2adc5016894941d8048fd14fe96ecc3e0a1b7d19 |
| shared/domain-profiles/documents.md | 71ac6fb88770ad55e696cf8f0c62488481296df0 |
| shared/domain-profiles/email.md | 0041dfc9254ba3bc38fbf2d8662de3af0945396d |
| shared/domain-profiles/purchasing-tickets.md | 41747cf7f4519a69dba1ae51da2a422175703f00 |
| shared/domain-profiles/research.md | a8756a9d90d73f91cc55873fe9cecad4b7c7d663 |
| shared/domain-profiles/scheduling.md | fa14367f7fec176059dda4f826332d44439bc168 |
| shared/education-levels.md | efe335df0531804f485656fcb9604d6287f60661 |
| shared/educational-report.md | fdc27d10666e201aca854e5c77ca5ae9ce376596 |
| shared/engineering-metadata.md | 4cdd9e4090b54664ede4418c7601fe82c84cad09 |
| shared/evaluation-rubrics.md | 6492250665a63970e092f729c280ecdb9fa5046b |
| shared/git-hygiene.md | 1733224ec812f8d68ddea9711d9476528e9077a4 |
| shared/git-safety.md | 32748a1b9b452cb4ef49d3fd02ac25a6a4b43ee8 |
| shared/help-mode.md | d357885a1db9119791916dcef1d140b9cd165fcb |
| shared/implementation-plan-audit.md | 7db3715918ec8939606a7d7286356bc1c0adfd4c |
| shared/instruction-conflicts.md | bdfd76f41d7bb59105d63a1f89a470eb471a02c6 |
| shared/instruction-deduplication.md | e680c924e45326cbda6603fb0645076aaf4e3369 |
| shared/instruction-precedence.md | 47286ae2757083cd745fa440940c865e6c8d2736 |
| shared/interaction-modes.md | 13e79f4f9de2d6b505f7f06d5488c22a1d8fb8bf |
| shared/loop-safety.md | bc8cd164a91b84fa5f32259ac53e392954e7e0c7 |
| shared/model-capability-tiers.md | feabc377d10fbc5ecd19746e7853f7100d8f61f9 |
| shared/model-profiles/gemma4.md | 81f243db66ecaca17606876d94fd0e4487073329 |
| shared/model-profiles/generic-local.md | cbb79354512b0a3ebc809efb301f64dde3f95478 |
| shared/model-profiles/llama3.md | b0af3c61ac66f8d40fcbe80dbb139abf026ff9b0 |
| shared/model-profiles/qwen36.md | e145d6042e7022cf864f18724dcd69e227cbda71 |
| shared/output-location.md | 947121b0780f3d8b1f2f1b146e26ab6f530bab0a |
| shared/persistent-task-state.md | 9cc4bee5a65abac4769aac366afa508949fb7951 |
| shared/phase-code-review.md | fdd1f6359db85717634e3516e747611f03dc924d |
| shared/phase-compression.md | 5f23b65f19c071b96b301b1dfafeae4d1445e11d |
| shared/phased-planning.md | bcec10578be516993391a1c84d46aa7b506bb16b |
| shared/planner-executor-workflows.md | 79bf52190d69eaa243fd0d3279d244dffde61dc2 |
| shared/ralph-loop.md | 42b8ee45b3b2356e4e38e548900a413554cb1b35 |
| shared/reference-optimization.md | b6e069d250ff2c749e81a39deec1a9b8a06403ca |
| shared/run-configuration-preview.md | 7e1436e30495cd4ce11a3ed1418ce5cccba27cce |
| shared/runtime-stability.md | ecaf560bc90c860e4bd92f9d7b76ff75982e5738 |
| shared/side-effect-matrix.md | 646b309d8ccf59b5e2aac7493671cf8c93f0edcd |
| shared/skill-interoperability.md | 7097284676b2ec171082c360e00aa2a9c24b7f23 |
| shared/small-context-workflows.md | dac58d2f0715f0ce2bf428d502632b3733d720ee |
| shared/small-model-atomicity.md | 17fd68dba5eed082bd24c05cfabf6cb65ad82dce |
| shared/subagent-delegation.md | 9fd0a7d429c0e0741e062df55a197b6e219ae939 |
| shared/targeted-context-length.md | f51e9f173f66537ee37ef5d9022ea9b48084f146 |
| shared/test-quality-audit.md | 1cfacccbc756bfeba29912f74cdad5d0baba80ec |
| shared/ui-standards.md | b3212b4a28834d78ccd4112460f145bfe1b33fde |
| shared/upstream-artifact-audit.md | 6e9800efd32073c03b8176d5b853b6ea16f3fcb6 |
| shared/usage-patterns.md | c647ae5b5f9f050a705e20043e872b545787ec63 |
| **Total shared files** | **52** |
