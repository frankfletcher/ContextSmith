# Domain Profile: AI Modalities

Use only the relevant modality sections.

## Tabular ML

- Track categorical encoding, missing-value handling, target definition, and leakage-prone columns.
- Compare against simple baselines.
- Use pipelines where possible to keep preprocessing and modeling together.

## Time Series

- Split by time, not random row split, unless explicitly justified.
- Fit preprocessing only on past/training windows.
- Avoid leakage from future features.
- Use backtesting or rolling validation when appropriate.

## Computer Vision

- Preserve image preprocessing consistency between training and inference.
- Avoid leakage through near-duplicate images, same subjects, or same capture sessions.
- Track augmentations, image sizes, and normalization.
- Validate on representative lighting, angle, device, and domain variation when relevant.

## NLP

- Preserve text normalization consistency.
- Watch for train/test contamination through duplicated documents or templated text.
- Use task-specific metrics and inspect representative errors.

## Speech / Audio

- Track sampling rate, channels, normalization, segmentation, and transcript alignment.
- Avoid leakage from speaker/session overlap across splits.
- Validate on representative devices, noise levels, and accents when relevant.

## Multimodal / Agentic AI

- Keep modality-specific preprocessing explicit.
- Record model/runtime versions.
- Separate source evidence from model inference.
- Validate tool use, retrieval quality, and final answer quality separately.
