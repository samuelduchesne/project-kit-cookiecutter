.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@if [ ! -d .git ]; then \
		echo "❌ Error: Not a git repository. Run 'git init -b main' first (see README step 1)."; \
		exit 1; \
	fi
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running {{ cookiecutter.type_checker }}"
	@uv run {% if cookiecutter.type_checker == "mypy" %}mypy{% elif cookiecutter.type_checker in ["ty", "pyrefly"] %}{{ cookiecutter.type_checker }} check{% else %}pyright{% endif %}
{%- if cookiecutter.deptry %}
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry {% if cookiecutter.layout == "src" %}src{% else %}.{% endif %}
{%- endif %}

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
{%- if cookiecutter.codecov %}
	@uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml
{%- else %}
	@uv run python -m pytest --doctest-modules
{%- endif%}

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

{%- if cookiecutter.publish_to_pypi %}

.PHONY: publish
publish: ## Publish a release to PyPI.
	@echo "🚀 Publishing."
	@uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.
{%- endif%}

{%- if cookiecutter.mkdocs %}

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve
{%- endif %}

{%- if cookiecutter.dockerfile %}

.PHONY: docker-build
docker-build: ## Build Docker image for the project
	@echo "🚀 Building Docker image {{ cookiecutter.project_name }}:latest"
	@docker build -t {{ cookiecutter.project_name }}:latest .

.PHONY: docker-run
docker-run: ## Run Docker container (maps host:8000 to container:8000)
	@echo "🚀 Running Docker container {{ cookiecutter.project_name }}"
	@docker run --rm -it -p 8000:8000 --name {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}:latest

.PHONY: docker-run-detached
docker-run-detached: ## Run Docker container in background (detached)
	@echo "🚀 Running Docker container {{ cookiecutter.project_name }} (detached)"
	@docker run -d --rm -p 8000:8000 --name {{ cookiecutter.project_name }} {{ cookiecutter.project_name }}:latest
{%- endif %}

{%- if cookiecutter.dvc %}

.PHONY: dvc-repro
dvc-repro: ## Run DVC pipeline (reproduces all stages)
	@echo "🚀 Running DVC pipeline"
	@uv run dvc repro

.PHONY: dvc-pull
dvc-pull: ## Pull data from DVC remote
	@echo "🚀 Pulling DVC data"
	@uv run dvc pull

.PHONY: dvc-push
dvc-push: ## Push data to DVC remote
	@echo "🚀 Pushing DVC data"
	@uv run dvc push

.PHONY: dvc-status
dvc-status: ## Show DVC pipeline status
	@echo "🚀 DVC pipeline status"
	@uv run dvc status

.PHONY: dvc-dag
dvc-dag: ## Show DVC pipeline DAG
	@echo "🚀 DVC pipeline DAG"
	@uv run dvc dag
{%- endif %}

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
