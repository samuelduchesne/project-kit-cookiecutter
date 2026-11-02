"""Pydantic schema for DVC pipeline parameters.

This module defines the schema for params.yaml validation.
When modifying params.yaml, update this schema accordingly.

Usage:
    from {{ cookiecutter.project_slug }}.schemas import PipelineParams
    params = PipelineParams.from_yaml("params.yaml")
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import yaml
from pydantic import BaseModel, Field


class PrepareParams(BaseModel):
    """Parameters for the data preparation stage."""

    seed: int = Field(default=42, description="Random seed for reproducibility")
    test_split: float = Field(default=0.2, ge=0.0, le=1.0, description="Fraction of data to use for testing")


class TrainParams(BaseModel):
    """Parameters for the model training stage."""

    epochs: int = Field(default=10, ge=1, description="Number of training epochs")
    learning_rate: float = Field(default=0.001, gt=0.0, description="Learning rate for optimizer")
    batch_size: int = Field(default=32, ge=1, description="Batch size for training")


class EvaluateParams(BaseModel):
    """Parameters for the model evaluation stage."""

    threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Classification threshold")


class PipelineParams(BaseModel):
    """Root schema for all DVC pipeline parameters.

    This schema validates the structure of params.yaml.
    Update this schema when adding or modifying pipeline parameters.
    """

    prepare: PrepareParams = Field(default_factory=PrepareParams)
    train: TrainParams = Field(default_factory=TrainParams)
    evaluate: EvaluateParams = Field(default_factory=EvaluateParams)

    @classmethod
    def from_yaml(cls, path: str | Path = "params.yaml") -> PipelineParams:
        """Load and validate parameters from a YAML file.

        Args:
            path: Path to the params.yaml file.

        Returns:
            Validated PipelineParams instance.

        Raises:
            FileNotFoundError: If the params file doesn't exist.
            pydantic.ValidationError: If the params don't match the schema.
        """
        with Path(path).open() as f:
            data = cast("dict[str, Any]", yaml.safe_load(f) or {})
        return cls.model_validate(data)

    @classmethod
    def generate_json_schema(cls, output_path: str | Path = "{% if cookiecutter.layout == 'src' %}src/{% endif %}{{ cookiecutter.project_slug }}/schemas/params.schema.json") -> None:
        """Generate JSON schema for IDE validation.

        Run this after modifying the Pydantic models to update the JSON schema:
            uv run python -c "from {{ cookiecutter.project_slug }}.schemas import PipelineParams; PipelineParams.generate_json_schema()"

        Args:
            output_path: Path to write the JSON schema file.
        """
        schema = cls.model_json_schema()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as f:
            json.dump(schema, f, indent=2)
        print(f"JSON schema written to {output_path}")


if __name__ == "__main__":
    # Generate JSON schema when run directly
    PipelineParams.generate_json_schema()
