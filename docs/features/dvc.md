# Data Version Control with DVC

If `dvc` is set to `True`, the generated project includes [DVC (Data Version Control)](https://dvc.org/) for versioning data, models, and creating reproducible ML/data pipelines.

## What's Included

When you enable DVC, the following files are created:

| File/Directory | Purpose |
|----------------|---------|
| `.dvc/` | DVC configuration directory |
| `.dvc/config` | DVC settings (remote storage configuration) |
| `.dvcignore` | Patterns for files DVC should ignore |
| `dvc.yaml` | Pipeline definition with example stages |
| `params.yaml` | Pipeline parameters file |
| `<package>/schemas/params.py` | Pydantic schema for params.yaml validation |
| `<package>/schemas/params.schema.json` | JSON schema for VS Code validation |
| `data/raw/` | Directory for raw input data |
| `data/processed/` | Directory for processed/transformed data |
| `<package>/prepare.py`, `<package>/train.py`, `<package>/evaluate.py` | Example pipeline scripts |

## Getting Started

### 1. Configure Remote Storage

DVC supports multiple storage backends. Configure your preferred remote:

=== "Amazon S3"

    ```bash
    uv run dvc remote add -d storage s3://mybucket/dvc-storage
    ```

=== "Google Cloud Storage"

    ```bash
    uv run dvc remote add -d storage gs://mybucket/dvc-storage
    ```

=== "Azure Blob Storage"

    ```bash
    uv run dvc remote add -d storage azure://mycontainer/dvc-storage
    ```

=== "Local/Network Path"

    ```bash
    # Local directory
    uv run dvc remote add -d storage /path/to/storage

    # Network/SSH path
    uv run dvc remote add -d storage ssh://user@server/path/to/storage
    ```

!!! info "Recommended Setup"
    Contact your team for the recommended remote storage configuration for your organization's projects.

### 2. Add Your Data

Place your raw data in `data/raw/`, then track it with DVC:

```bash
# Add a single file
uv run dvc add data/raw/your-dataset.csv

# Or add an entire directory
uv run dvc add data/raw/

# Commit the tracking files to git
git add data/raw.dvc data/.gitignore
git commit -m "Add raw dataset"
```

### 3. Run the Pipeline

Execute all pipeline stages:

=== "macOS / Linux"

    ```bash
    make dvc-repro
    ```

=== "Windows (PowerShell)"

    ```powershell
    uv run dvc repro
    ```

### 4. Push Data to Remote

After running your pipeline, push data and outputs to your remote:

=== "macOS / Linux"

    ```bash
    make dvc-push
    ```

=== "Windows (PowerShell)"

    ```powershell
    uv run dvc push
    ```

### 5. Pull Data (for collaborators)

Team members can pull data from the remote:

=== "macOS / Linux"

    ```bash
    make dvc-pull
    ```

=== "Windows (PowerShell)"

    ```powershell
    uv run dvc pull
    ```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make dvc-repro` | Run DVC pipeline (reproduces all stages) |
| `make dvc-pull` | Pull data from DVC remote |
| `make dvc-push` | Push data to DVC remote |
| `make dvc-status` | Show DVC pipeline status |
| `make dvc-dag` | Show DVC pipeline DAG visualization |

## Use Cases

### Machine Learning Workflows

DVC excels at versioning ML experiments:

- **Dataset versioning**: Track different versions of training data alongside your code
- **Model versioning**: Version trained models without bloating your git repository
- **Experiment tracking**: Compare metrics across experiments with `dvc metrics diff`
- **Reproducibility**: Anyone can reproduce your exact results with `dvc repro`

Example workflow:
```bash
# Train a model
uv run dvc repro

# Check metrics
uv run dvc metrics show

# Compare with previous run
uv run dvc metrics diff
```

### Data Pipelines / ETL

DVC also works well for data engineering:

- **ETL pipelines**: Define data transformation stages in `dvc.yaml`
- **Data lineage**: Track which raw data produced which outputs
- **Incremental processing**: DVC only reruns stages when dependencies change
- **Collaboration**: Share large datasets without storing them in Git

Example pipeline flow:
```
data/raw/ → prepare stage → data/processed/ → transform stage → data/final/
```

## GitHub Actions Integration

When `include_github_actions` is enabled, the CI pipeline includes a `dvc-pipeline` job that:

1. Pulls data from your configured remote (if available)
2. Verifies the pipeline is reproducible with `dvc repro --dry`

### Required Secrets

Configure these repository secrets for cloud storage access:

| Provider | Secrets Required |
|----------|------------------|
| AWS S3 | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |
| GCP | `GCP_SERVICE_ACCOUNT_KEY` (JSON content) |
| Azure | `AZURE_STORAGE_ACCOUNT`, `AZURE_STORAGE_KEY` |

To add secrets:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each required secret for your storage provider

## Pipeline Structure

The default `dvc.yaml` includes a sample pipeline:

```yaml
stages:
  prepare:
    cmd: uv run python your_package/prepare.py
    deps:
      - data/raw
      - your_package/prepare.py
    params:
      - prepare
    outs:
      - data/processed
```

### Key Concepts

- **`cmd`**: The command to run for this stage
- **`deps`**: Files/directories this stage depends on (triggers rerun if changed)
- **`params`**: Parameters from `params.yaml` (triggers rerun if changed)
- **`outs`**: Output files/directories (cached and tracked by DVC)
- **`metrics`**: JSON/YAML files with metrics (for experiment comparison)
- **`plots`**: Visualization files

### Extending the Pipeline

Add more stages by uncommenting or adding to `dvc.yaml`:

```yaml
stages:
  prepare:
    # ... existing stage ...

  train:
    cmd: uv run python your_package/train.py
    deps:
      - data/processed
      - your_package/train.py
    params:
      - train
    outs:
      - models/model.pkl
    metrics:
      - metrics/train_metrics.json:
          cache: false

  evaluate:
    cmd: uv run python your_package/evaluate.py
    deps:
      - models/model.pkl
      - data/processed
    metrics:
      - metrics/eval_metrics.json:
          cache: false
```

## Parameter Schema Validation

Pipeline parameters are validated using [Pydantic](https://docs.pydantic.dev/) to catch configuration errors early.

### How It Works

1. **`<package>/schemas/params.py`** defines Pydantic models for all pipeline parameters
2. **`<package>/schemas/params.schema.json`** provides JSON schema for VS Code validation
3. **Pipeline scripts** use `PipelineParams.from_yaml()` to load and validate parameters

### Adding New Parameters

When modifying `params.yaml`, you **must** also update the schema:

1. Edit `<package>/schemas/params.py` to add/modify Pydantic models
2. Regenerate the JSON schema:
   ```bash
   uv run python -c "from <package>.schemas import PipelineParams; PipelineParams.generate_json_schema()"
   ```
3. Commit both `params.yaml` and the updated schema files

### Example: Adding a New Parameter

```python
# In <package>/schemas/params.py
class TrainParams(BaseModel):
    epochs: int = Field(default=10, ge=1)
    learning_rate: float = Field(default=0.001, gt=0.0)
    batch_size: int = Field(default=32, ge=1)
    # Add new parameter:
    dropout: float = Field(default=0.5, ge=0.0, le=1.0, description="Dropout rate")
```

Then update `params.yaml`:
```yaml
train:
  epochs: 10
  learning_rate: 0.001
  batch_size: 32
  dropout: 0.5  # New parameter
```

### VS Code Integration

With the Red Hat YAML extension installed, VS Code provides:

- **Autocomplete** for parameter names
- **Validation** against the schema
- **Hover documentation** from field descriptions

The extension is included in `.vscode/extensions.json` recommendations.

## Best Practices

1. **Commit `.dvc` files**: Always commit the `.dvc` tracking files to Git
2. **Use meaningful stage names**: Make your pipeline self-documenting
3. **Parameterize everything**: Put hyperparameters in `params.yaml` for easy experimentation
4. **Track metrics**: Use `metrics:` in dvc.yaml for experiment comparison
5. **Document dependencies**: List all file and parameter dependencies explicitly
6. **Use `cache: false` for metrics**: Keeps metrics files in the repo for easy comparison
7. **Keep schema in sync**: Always update `schemas/params.py` when changing `params.yaml`

## Further Reading

- [DVC Documentation](https://dvc.org/doc)
- [DVC Pipelines Guide](https://dvc.org/doc/user-guide/pipelines)
- [DVC Remote Storage](https://dvc.org/doc/user-guide/data-management/remote-storage)
- [DVC Experiments](https://dvc.org/doc/start/experiments)
- [DVC with CI/CD](https://dvc.org/doc/use-cases/ci-cd-for-machine-learning)
