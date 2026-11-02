# Contributing to `{{cookiecutter.project_name}}`

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

You can contribute in many ways:

# Types of Contributions

## Report Bugs

Report bugs at https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/issues

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

## Fix Bugs

Look through the GitHub issues for bugs.
Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

## Implement Features

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

## Write Documentation

{{cookiecutter.project_name}} could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

## Submit Feedback

The best way to send feedback is to file an issue at https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/issues.

If you are proposing a new feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

# Get Started!

Ready to contribute? Here's how to set up `{{cookiecutter.project_name}}` for local development.
Please note this documentation assumes you already have Node.js {{cookiecutter.node_version}} or newer, pnpm (`npm install -g pnpm`), `uv` and `Git` installed.

1. Fork the `{{cookiecutter.project_name}}` repo on GitHub.

2. Clone your fork locally:

```bash
cd <directory_in_which_repo_should_be_created>
git clone git@github.com:YOUR_NAME/{{cookiecutter.project_name}}.git
```

3. Install the dependencies and the pre-commit hooks:

```bash
cd {{cookiecutter.project_name}}
make install
```

4. Create a branch for local development:

```bash
git checkout -b name-of-your-bugfix-or-feature
```

Now you can make your changes locally.

5. Don't forget to add test cases for your added functionality to the `tests` directory.

6. When you're done making changes, check that your changes pass the linting, formatting and type checks:

```bash
make check
```

Now, validate that all unit tests are passing:

```bash
make test
```

7. Commit your changes and push your branch to GitHub:

```bash
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

8. Submit a pull request through the GitHub website.

# Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated.
   Document new exports with a TSDoc comment, and add the feature to `README.md`.
{%- if cookiecutter.changelog %}

3. Update CHANGELOG.md under [Unreleased].
   Add a bullet under the matching [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) category
   (Added, Changed, Deprecated, Removed, Fixed, Security) for any user-facing change.
{%- endif %}
