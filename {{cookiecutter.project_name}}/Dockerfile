# Install uv
FROM python:{{cookiecutter.development_python_version}}-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Enable uv bytecode compilation to speed up startup time at the cost of increased installation time
ENV UV_COMPILE_BYTECODE=1

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
COPY . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD [ "python", "{{cookiecutter.project_slug}}/foo.py" ]
