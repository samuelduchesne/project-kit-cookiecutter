# Test coverage with codecov

If `codecov` is set to `true`, `pytest-cov` is added as a development dependency,
and `make test` will run the tests and output a coverage report as `coverage.xml`.

## Setting up Codecov

1. Sign up at [codecov.io](https://about.codecov.io/) with your GitHub account
2. Your **public repositories** should work automatically
3. For **private repositories**, you need to add a secret:
    - Go to [app.codecov.io](https://app.codecov.io/) and select your repository
    - Copy the "Repository Upload Token"
    - In your GitHub repository, go to `Settings > Secrets and variables > Actions`
    - Add a new repository secret named `CODECOV_TOKEN`

For more details on token types, see [Codecov's documentation](https://docs.codecov.com/docs/codecov-tokens).

## Configuration

A `codecov.yaml` file is created with the following defaults:

```yaml
# Badge color changes from red to green between 70% and 100%
# PR pipeline fails if codecov falls with 1%

coverage:
  range: 70..100
  round: down
  precision: 1
  status:
    project:
      default:
        target: auto
        threshold: 1%

# Ignoring Paths
# --------------
# which folders/files to ignore
ignore:
  - "foo/bar.py"
```

If `codecov` is set to `false`, `pytest-cov` is not added to the development dependencies and the github actions won't produce a coverage report.
