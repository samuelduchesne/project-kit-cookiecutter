"""Data preparation script for DVC pipeline.

This is a sample script that demonstrates how to structure
data processing code for use with DVC pipelines.

Run with: uv run dvc repro
"""

from __future__ import annotations

import json
from pathlib import Path

from {{ cookiecutter.project_slug }}.schemas import PipelineParams


def main() -> None:
    """Run data preparation."""
    params = PipelineParams.from_yaml()
    prepare_params = params.prepare

    # Create output directory
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    # TODO: Add your data preparation logic here
    # Example workflow:
    # 1. Load raw data from data/raw/
    # 2. Apply transformations using prepare_params
    # 3. Save processed data to data/processed/

    print(f"Data preparation complete with seed={prepare_params.seed}, test_split={prepare_params.test_split}")

    # Write a manifest as proof of execution
    manifest = {
        "status": "complete",
        "seed": prepare_params.seed,
        "test_split": prepare_params.test_split,
    }
    with (output_dir / "manifest.json").open("w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    main()
