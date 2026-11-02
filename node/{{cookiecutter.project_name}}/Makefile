PRE_COMMIT := uvx pre-commit@4.7.0

.PHONY: install
install: ## Install dependencies and the pre-commit hooks
	@if [ ! -d .git ]; then \
		echo "❌ Error: Not a git repository. Run 'git init -b main' first (see README)."; \
		exit 1; \
	fi
	@echo "🚀 Installing dependencies with pnpm"
	@pnpm install
	@$(PRE_COMMIT) install

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'package.json'"
	@pnpm install --frozen-lockfile
	@echo "🚀 Linting and formatting: Running pre-commit"
	@$(PRE_COMMIT) run -a
	@echo "🚀 Static type checking: Running tsc"
	@pnpm typecheck

.PHONY: test
test: ## Test the code with Vitest
	@echo "🚀 Testing code: Running vitest"
{%- if cookiecutter.codecov %}
	@pnpm test:coverage
{%- else %}
	@pnpm test
{%- endif %}

.PHONY: build
build: clean-build ## Build the package into dist/
	@echo "🚀 Building with tsc"
	@pnpm build

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@rm -rf dist

.PHONY: help
help:
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
