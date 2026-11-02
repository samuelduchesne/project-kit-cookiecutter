"""Evaluation script for DVC pipeline.

This is a sample script that demonstrates how to structure
model evaluation code for use with DVC pipelines.

Run with: uv run dvc repro
"""

from __future__ import annotations

import json
from pathlib import Path

from {{ cookiecutter.project_slug }}.schemas import PipelineParams


def main() -> None:
    """Run model evaluation."""
    params = PipelineParams.from_yaml()
    eval_params = params.evaluate

    # Create output directories
    metrics_dir = Path("metrics")
    plots_dir = Path("plots")
    metrics_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    # TODO: Add your evaluation logic here
    # Example workflow:
    # 1. Load model from models/model.pkl
    # 2. Load test data from data/processed/
    # 3. Run predictions and calculate metrics
    # 4. Save metrics to metrics/eval.json
    # 5. Generate plots to plots/

    print(f"Evaluation complete with threshold={eval_params.threshold}")

    # Write evaluation metrics
    eval_metrics = {
        "precision": 0.0,
        "recall": 0.0,
        "f1_score": 0.0,
        "threshold": eval_params.threshold,
    }
    with (metrics_dir / "eval.json").open("w") as f:
        json.dump(eval_metrics, f, indent=2)

    # Write a placeholder plot file
    with (plots_dir / "confusion_matrix.png").open("wb") as f:
        f.write(b"placeholder")


if __name__ == "__main__":
    main()
