# Example: Data Pipeline Project

This example shows how to set up a data processing pipeline with the Agentic State Protocol.

## Project Type
- **Architecture**: Data Pipeline
- **Tech Stack**: Python
- **Use Case**: ETL, ML pipelines, data processing, scientific computing

## Initialization

```bash
# From the agentic-state-protocol root directory
python init_project.py

# When prompted:
# - Project name: "My Data Pipeline"
# - Tech stack: Python (1)
# - Architecture: Data Pipeline (2)
```

## Resulting Structure

```
my_data_pipeline/
├── docs/                      # Protocol documentation
├── src/my_data_pipeline/      # Main package
│   ├── __init__.py
│   ├── ingestion/             # Data loaders (add)
│   │   ├── __init__.py
│   │   ├── api_loader.py
│   │   └── file_loader.py
│   ├── processing/            # Transformations (add)
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   └── transformer.py
│   ├── storage/               # Data persistence (add)
│   │   ├── __init__.py
│   │   └── db_writer.py
│   └── serving/               # Output/API (add)
│       ├── __init__.py
│       └── api.py
├── tests/
├── scripts/
├── configs/
│   └── pipeline.yaml          # Pipeline config (add)
├── data/                      # Data directory (add)
│   ├── raw/
│   ├── processed/
│   └── output/
├── .claude/
├── CLAUDE.md
├── pyproject.toml             # Add this
└── README.md                  # Add this
```

## Recommended pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-data-pipeline"
version = "0.1.0"
description = "A data processing pipeline"
requires-python = ">=3.9"
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "pyyaml>=6.0.0",
    "requests>=2.28.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "pyright>=1.1.0",
]
ml = [
    "scikit-learn>=1.3.0",
    "xgboost>=2.0.0",
]

[project.scripts]
pipeline = "my_data_pipeline.cli:main"

[tool.ruff]
line-length = 88
target-version = "py39"

[tool.pyright]
pythonVersion = "3.9"
typeCheckingMode = "basic"
```

## Sample Pipeline Code

```python
# src/my_data_pipeline/pipeline.py
from pathlib import Path
from typing import Any
import pandas as pd
import yaml


class Pipeline:
    """Main pipeline orchestrator."""

    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)
        self.data: pd.DataFrame | None = None

    def _load_config(self, path: Path) -> dict[str, Any]:
        with open(path) as f:
            return yaml.safe_load(f)

    def ingest(self) -> "Pipeline":
        """Load data from source."""
        source = self.config["source"]
        if source["type"] == "csv":
            self.data = pd.read_csv(source["path"])
        elif source["type"] == "api":
            # API loading logic
            pass
        return self

    def process(self) -> "Pipeline":
        """Apply transformations."""
        if self.data is None:
            raise ValueError("No data to process. Run ingest() first.")

        # Apply configured transformations
        for transform in self.config.get("transforms", []):
            if transform["type"] == "drop_nulls":
                self.data = self.data.dropna()
            elif transform["type"] == "filter":
                self.data = self.data.query(transform["query"])
        return self

    def store(self) -> "Pipeline":
        """Save processed data."""
        if self.data is None:
            raise ValueError("No data to store. Run process() first.")

        output = self.config["output"]
        if output["type"] == "csv":
            self.data.to_csv(output["path"], index=False)
        elif output["type"] == "parquet":
            self.data.to_parquet(output["path"], index=False)
        return self

    def run(self) -> None:
        """Run the full pipeline."""
        self.ingest().process().store()


# Example usage
if __name__ == "__main__":
    pipeline = Pipeline(Path("configs/pipeline.yaml"))
    pipeline.run()
```

## Sample Config

```yaml
# configs/pipeline.yaml
source:
  type: csv
  path: data/raw/input.csv

transforms:
  - type: drop_nulls
  - type: filter
    query: "value > 0"

output:
  type: parquet
  path: data/processed/output.parquet
```

## Workflow Example

```bash
# Start session
/boot

# Add new data source
/feature add-api-ingestion

# After implementing
/done

# Run pipeline test
pytest tests/ -v

# Save and commit
/save
```

## Architecture Notes

The Data Pipeline pattern follows this flow:

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ Ingest  │ → │ Process │ → │ Store   │ → │ Serve   │
│         │   │         │   │         │   │         │
│ - APIs  │   │ - Clean │   │ - DB    │   │ - API   │
│ - Files │   │ - Trans │   │ - Files │   │ - Dash  │
│ - Scrape│   │ - Valid │   │ - Cache │   │ - Export│
└─────────┘   └─────────┘   └─────────┘   └─────────┘
```

Each stage is independent and can be tested/run separately.
