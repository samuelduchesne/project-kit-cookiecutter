# Makefile

The generated repository will have a `Makefile` available. A list of all
available commands can be obtained by running `make help` in the terminal.

!!! note "Windows Users"
    Windows does not include `make` by default. You have two options:

    1. **Install make** via [Chocolatey](https://chocolatey.org/), [Scoop](https://scoop.sh/), or [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) (see [Installing Make on Windows](#installing-make-on-windows))
    2. **Run the underlying commands directly** (shown in the table below)

## Available Commands

Initially, if all features are selected, the following commands are available:

| Make Command | Direct Command (Windows-friendly) | Description |
|:-------------|:----------------------------------|:------------|
| <nobr>`make install`</nobr> | `uv sync && uv run pre-commit install` | Install the uv environment and pre-commit hooks |
| <nobr>`make check`</nobr> | See [check commands](#check-command-breakdown) | Lint and check code |
| <nobr>`make test`</nobr> | `uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml` | Test the code with pytest |
| <nobr>`make build`</nobr> | `uvx --from build pyproject-build --installer uv` | Build wheel file |
| <nobr>`make clean-build`</nobr> | `uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"` | Clean build artifacts |
| <nobr>`make publish`</nobr> | `uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*` | Publish a release to PyPI |
| <nobr>`make docs-test`</nobr> | `uv run mkdocs build -s` | Test documentation build |
| <nobr>`make docs`</nobr> | `uv run mkdocs serve` | Build and serve documentation |
| <nobr>`make docker-build`</nobr> | `docker build -t <project_name>:latest .` | Build Docker image |
| <nobr>`make docker-run`</nobr> | `docker run --rm -it -p 8000:8000 <project_name>:latest` | Run Docker container |
| <nobr>`make dvc-repro`</nobr> | `uv run dvc repro` | Run DVC pipeline (if `dvc` enabled) |
| <nobr>`make dvc-pull`</nobr> | `uv run dvc pull` | Pull data from DVC remote (if `dvc` enabled) |
| <nobr>`make dvc-push`</nobr> | `uv run dvc push` | Push data to DVC remote (if `dvc` enabled) |
| <nobr>`make dvc-status`</nobr> | `uv run dvc status` | Show DVC pipeline status (if `dvc` enabled) |
| <nobr>`make dvc-dag`</nobr> | `uv run dvc dag` | Show DVC pipeline DAG visualization (if `dvc` enabled) |

### Check Command Breakdown

The `make check` command runs multiple quality checks in sequence:

=== "macOS / Linux"

    ```bash
    make check
    ```

=== "Windows (PowerShell)"

    Run these commands in order:

    ```powershell
    # Check lock file consistency
    uv lock --locked

    # Run pre-commit hooks (linting, formatting)
    uv run pre-commit run -a

    # Run type checker (mypy or ty, depending on your choice)
    uv run mypy
    # or: uv run ty check

    # Run deptry (if enabled)
    uv run deptry .
    ```

## Installing Make on Windows

If you prefer using `make` commands, install it via one of these package managers:

=== "Chocolatey"

    ```powershell
    choco install make
    ```

=== "Scoop"

    ```powershell
    scoop install make
    ```

=== "winget"

    ```powershell
    winget install GnuWin32.Make
    ```

After installation, restart your terminal and `make` commands will work as documented.
