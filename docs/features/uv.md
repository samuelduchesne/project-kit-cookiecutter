# Dependency management with uv

The generated repository uses [uv](https://docs.astral.sh/uv/)
for its dependency management.

## Installing uv

If you don't have uv installed yet:

=== "macOS / Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows (PowerShell)"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

For more installation options, see the [uv documentation](https://docs.astral.sh/uv/#getting-started).

## Adding dependencies

When you have created your repository using this cookiecutter template, a uv environment is pre-configured
in `pyproject.toml`. Add your project-specific dependencies with:

```bash
uv add <package>
```

## Installing the environment

Install the environment with:

```bash
uv sync
```

## Running commands

You can run commands within your virtual environment using `uv run`:

```bash
uv run python -m pytest
```

Or activate the virtual environment and run commands directly:

=== "macOS / Linux"

    ```bash
    source .venv/bin/activate
    python -m pytest
    ```

=== "Windows (PowerShell)"

    ```powershell
    .venv\Scripts\Activate.ps1
    python -m pytest
    ```

=== "Windows (cmd)"

    ```cmd
    .venv\Scripts\activate.bat
    python -m pytest
    ```
