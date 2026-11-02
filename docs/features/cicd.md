# CI/CD with Github actions

When `include_github_actions` is set to `true`, a `.github` directory is
added with the following structure:

    .github
    ├── actions
    │   └── setup-python-env
    │       └── action.yml
    ├── workflows
    │   ├── main.yml
    │   ├── on-release-main.yml
    │   ├── validate-codecov-config.yml
    │   └── copilot-setup-steps.yml
    └── copilot-instructions.md

`main.yml` is triggered on pushes to `main` and on pull requests. It runs
quality checks (linting, formatting, type checking) and tests across
multiple Python versions (3.9-3.14). The workflow uses the
`setup-python-env` action to set up the environment with uv.

`on-release-main.yml` is triggered whenever a new release is published.
It publishes the project to PyPI if `publish_to_pypi` is set to
`true`, and it builds and deploys the documentation
if `mkdocs` is set to `true`. To learn more about these features,
see [Publishing to PyPI](./publishing.md) and [Documentation with MkDocs](./mkdocs.md).

`validate-codecov-config.yml` validates the codecov configuration file
(only included if `codecov` is set to `true`).

`copilot-setup-steps.yml` provides setup steps for GitHub Copilot
(only included if `agent_instructions` includes Copilot).

## How to trigger a release?

To trigger a new release, navigate to your repository on GitHub, click `Releases` on the right, and then select `Draft
a new release`. If you fail to find the button, you could also directly visit
`https://github.com/<username>/<repository-name>/releases/new`.

Give your release a title, and add a new tag in the form `*.*.*` where the
`*`'s are alphanumeric. To finish, press `Publish release`.
