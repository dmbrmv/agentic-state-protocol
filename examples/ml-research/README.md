# Example: ML Research Project

This example shows how to set up a machine learning research project for earth science with the Agentic State Protocol.

## Project Type
- **Architecture**: ML Research Project
- **Tech Stack**: Python (ML / Data Science)
- **Use Case**: Hydrological modeling, land use classification, climate prediction

## Initialization

```bash
# From the agentic-state-protocol root directory
python init_project.py

# When prompted:
# - Project name: "Streamflow Predictor"
# - Tech stack: Python (1)
# - Architecture: Monolithic Application (1)
```

## Resulting Structure

```
streamflow_predictor/
├── docs/                          # Protocol documentation
├── data/                          # Data directory (gitignored)
│   ├── raw/                       # Original datasets
│   ├── processed/                 # Feature-engineered datasets
│   └── splits/                    # Train/val/test splits
├── models/                        # Trained model artifacts (gitignored)
│   ├── checkpoints/               # Training checkpoints
│   └── final/                     # Production-ready models
├── experiments/                   # Experiment tracking
│   ├── configs/                   # Hyperparameter configs
│   └── results/                   # Metrics, plots, logs
├── notebooks/                     # Marimo notebooks for exploration
│   ├── 01_data_exploration.py
│   ├── 02_feature_analysis.py
│   └── 03_model_evaluation.py
├── src/streamflow_predictor/      # Main package
│   ├── __init__.py
│   ├── cli.py                     # CLI entry point
│   ├── data/                      # Data loading and preprocessing
│   │   ├── __init__.py
│   │   ├── loader.py              # Dataset loaders
│   │   └── features.py            # Feature engineering
│   ├── models/                    # Model definitions
│   │   ├── __init__.py
│   │   ├── baseline.py            # Statistical baselines
│   │   └── xgb_model.py           # XGBoost model
│   ├── training/                  # Training logic
│   │   ├── __init__.py
│   │   ├── trainer.py             # Training loop
│   │   └── optimize.py            # Optuna hyperparameter search
│   └── evaluation/                # Evaluation and metrics
│       ├── __init__.py
│       ├── metrics.py             # NSE, KGE, RMSE, PBIAS
│       └── plots.py               # Hydrograph plots, scatter
├── tests/
│   ├── test_data.py
│   ├── test_models.py
│   └── test_metrics.py
├── scripts/
│   ├── train.py                   # Training entry point
│   └── evaluate.py                # Evaluation entry point
├── configs/
│   └── default.yaml               # Default experiment config
├── .claude/
├── CLAUDE.md
├── pyproject.toml
└── README.md
```

## Recommended pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "streamflow-predictor"
version = "0.1.0"
description = "ML-based streamflow prediction for watershed modeling"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "scikit-learn>=1.3.0",
    "xgboost>=2.0.0",
    "optuna>=3.4.0",
    "xarray>=2023.1.0",
    "pyyaml>=6.0.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
    "matplotlib>=3.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "pyright>=1.1.0",
]
notebooks = [
    "marimo>=0.3.0",
]

[project.scripts]
predictor = "streamflow_predictor.cli:app"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "basic"
```

## Sample Training Code

```python
# src/streamflow_predictor/training/trainer.py
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from streamflow_predictor.evaluation.metrics import compute_nse, compute_kge


def set_reproducibility(seed: int) -> None:
    """Set random seeds for reproducible results."""
    np.random.seed(seed)


def load_config(config_path: Path) -> dict[str, Any]:
    """Load experiment configuration."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def train_model(config_path: Path) -> dict[str, float]:
    """Train a streamflow prediction model.

    Args:
        config_path: Path to experiment config YAML.

    Returns:
        Dictionary of evaluation metrics.
    """
    config = load_config(config_path)
    seed = config.get("seed", 42)
    set_reproducibility(seed)

    # Load data
    data = pd.read_parquet(config["data"]["path"])
    feature_cols = config["data"]["features"]
    target_col = config["data"]["target"]

    X = data[feature_cols].values
    y = data[target_col].values

    # Split data (temporal split for time series)
    split_idx = int(len(X) * config["data"]["train_fraction"])
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Train model
    model_params = config.get("model", {})
    model = XGBRegressor(
        n_estimators=model_params.get("n_estimators", 500),
        max_depth=model_params.get("max_depth", 6),
        learning_rate=model_params.get("learning_rate", 0.05),
        random_state=seed,
    )
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )

    # Evaluate
    y_pred = model.predict(X_test)
    metrics = {
        "nse": compute_nse(y_test, y_pred),
        "kge": compute_kge(y_test, y_pred),
        "rmse": float(np.sqrt(np.mean((y_test - y_pred) ** 2))),
    }

    # Save model
    output_dir = Path(config.get("output_dir", "models/final"))
    output_dir.mkdir(parents=True, exist_ok=True)
    model.save_model(str(output_dir / "xgb_streamflow.json"))

    return metrics
```

## Sample Metrics Code

```python
# src/streamflow_predictor/evaluation/metrics.py
import numpy as np
from numpy.typing import NDArray


def compute_nse(observed: NDArray, simulated: NDArray) -> float:
    """Nash-Sutcliffe Efficiency.

    NSE = 1 means perfect match, NSE < 0 means worse than mean.
    """
    numerator = np.sum((observed - simulated) ** 2)
    denominator = np.sum((observed - np.mean(observed)) ** 2)
    if denominator == 0:
        return float("nan")
    return float(1.0 - numerator / denominator)


def compute_kge(observed: NDArray, simulated: NDArray) -> float:
    """Kling-Gupta Efficiency.

    KGE = 1 means perfect match. Decomposes into correlation,
    variability bias, and mean bias.
    """
    r = float(np.corrcoef(observed, simulated)[0, 1])
    alpha = float(np.std(simulated) / np.std(observed))
    beta = float(np.mean(simulated) / np.mean(observed))
    return float(1.0 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2))
```

## Sample Experiment Config

```yaml
# configs/default.yaml
seed: 42

data:
  path: data/processed/features.parquet
  features:
    - precip_mm
    - temp_mean_c
    - precip_lag1
    - precip_lag2
    - precip_lag3
    - soil_moisture
    - ndvi
    - elevation_m
    - slope_deg
  target: streamflow_m3s
  train_fraction: 0.8

model:
  n_estimators: 500
  max_depth: 6
  learning_rate: 0.05

output_dir: models/final
```

## Marimo Notebook Workflow

```bash
# Launch interactive exploration notebook
marimo edit notebooks/01_data_exploration.py

# Run notebook as script (for CI/reproducibility)
marimo run notebooks/01_data_exploration.py

# Export to HTML for sharing
marimo export html notebooks/03_model_evaluation.py -o reports/evaluation.html
```

## Workflow Example

```bash
# Start session
/boot

# Plan a new model variant
/feature add-lstm-baseline

# After implementing
/done

# Run experiments
python scripts/train.py --config configs/default.yaml

# Review results
/calibrate-review

# Save and commit
/save
```

## Architecture Notes

The ML Research Project follows this structure:

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Data      │ - │  Feature   │ - │  Train     │ - │  Evaluate  │
│            │   │            │   │            │   │            │
│ - Load     │   │ - Engineer │   │ - Fit      │   │ - NSE/KGE  │
│ - Clean    │   │ - Select   │   │ - Optimize │   │ - Plots    │
│ - Split    │   │ - Scale    │   │ - Validate │   │ - Compare  │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
```

Key principles:
- **Reproducibility**: All experiments use explicit seeds and config files
- **Temporal splitting**: Never leak future data into training (no random split for time series)
- **Experiment tracking**: Configs and metrics stored alongside code
- **Notebook-code separation**: Notebooks for exploration, `src/` for production code
