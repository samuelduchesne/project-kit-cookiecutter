"""Training script for DVC pipeline.

This is a sample script that demonstrates how to structure
model training code for use with DVC pipelines.

Run with: uv run dvc repro
"""

from __future__ import annotations

import json
from pathlib import Path

from {{ cookiecutter.project_slug }}.schemas import PipelineParams


def main() -> None:
    """Run model training."""
    params = PipelineParams.from_yaml()
    train_params = params.train

    # Create output directories
    models_dir = Path("models")
    metrics_dir = Path("metrics")
    models_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)

    # TODO: Add your training logic here
    # Example workflow:
    # 1. Load processed data from data/processed/
    # 2. Train model using train_params
    # 3. Save model to models/model.pkl
    # 4. Save metrics to metrics/metrics.json

    print(
        f"Training complete with epochs={train_params.epochs}, "
        f"lr={train_params.learning_rate}, batch_size={train_params.batch_size}"
    )

    # Write metrics as proof of execution
    metrics = {
        "accuracy": 0.0,
        "loss": 0.0,
        "epochs": train_params.epochs,
        "learning_rate": train_params.learning_rate,
        "batch_size": train_params.batch_size,
    }
    with (metrics_dir / "metrics.json").open("w") as f:
        json.dump(metrics, f, indent=2)

    # Write a placeholder model file
    with (models_dir / "model.pkl").open("wb") as f:
        f.write(b"placeholder")


if __name__ == "__main__":
    main()
