"""Schema definitions for DVC pipeline parameters."""

from __future__ import annotations

from {{ cookiecutter.project_slug }}.schemas.params import (
    EvaluateParams,
    PipelineParams,
    PrepareParams,
    TrainParams,
)

__all__ = ["EvaluateParams", "PipelineParams", "PrepareParams", "TrainParams"]
