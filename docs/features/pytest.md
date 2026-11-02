# Unittesting with Pytest

[pytest](https://docs.pytest.org/en/stable/) is automatically added to
the environment. There will be a template unittest in the `tests`
directory upon creation of the project, which can be run with

```bash
make test
```

pytest runs in strict mode, so typos in markers or config options and unexpectedly passing
`xfail` tests fail the run instead of being silently ignored. With a minimum Python of 3.10 or newer
the template uses pytest 9's single `strict = true` option:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
strict = true
```

pytest 9 requires Python 3.10, so projects with a 3.9 minimum get the equivalent pytest 8 options:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--strict-markers", "--strict-config"]
xfail_strict = true
```

If `include_github_actions` is set to `true`, the tests are automatically
run for every merge request, every merge to main, and every release.
