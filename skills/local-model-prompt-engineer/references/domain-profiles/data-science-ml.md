# Domain Profile: Data Science, Machine Learning, and AI

Use this profile when the repo or task involves data science, ML, notebooks, model training, evaluation, RAG, LLM apps, or AI workflows.

## Detection Signals

- `notebooks/`, `*.ipynb`
- `pandas`, `numpy`, `sklearn`, `torch`, `tensorflow`, `keras`, `xgboost`, `lightgbm`
- `mlflow`, `wandb`, `dvc`
- `data/`, `models/`, `features/`, `training`, `evaluation`

## Data Handling

- Do not assume data files are small enough to load fully.
- Inspect schema, shape, missing values, and target definitions before modeling.
- Do not modify raw data in place.
- Keep raw, interim, processed, and model output data separate when the project supports it.
- Do not commit large datasets, model checkpoints, caches, or generated outputs unless the repo intentionally tracks them.

## Leakage Prevention

- Split train/validation/test data before fitting preprocessing steps.
- Fit scalers, encoders, imputers, feature selection, and dimensionality reduction only on training data.
- Apply fitted preprocessing to validation/test data.
- Do not use test data for model selection, prompt tuning, or hyperparameter tuning.
- For time series, split by time unless the task explicitly justifies another split.

## Evaluation

- Define the metric before optimizing.
- Use baselines before complex models.
- Report validation/test metrics separately.
- Include uncertainty, variance, or repeated-run notes when practical.
- Avoid cherry-picking a single favorable run.

## Reproducibility

- Set random seeds where supported.
- Record data versions, feature definitions, model parameters, and environment details.
- Prefer scripts or pipelines over manual notebook-only workflows for repeatable tasks.

## LLM / RAG Standards

- Separate prompts, retrieval config, model config, and evaluation data.
- Track prompt versions and model/runtime versions.
- Evaluate with representative cases, edge cases, and failure cases.
- For RAG, inspect retrieval quality before blaming generation.
- Keep evidence anchors or citations when factuality matters.
- Do not send secrets, credentials, private user data, or proprietary docs to external APIs without approval.
