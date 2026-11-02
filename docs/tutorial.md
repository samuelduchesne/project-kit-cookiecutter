# Tutorial

This page contains a complete tutorial on how to create your project.

## Before You Begin

Make sure you have the following set up:

- [ ] A [GitHub account](https://github.com/signup)
- [ ] [Git installed](https://git-scm.com/downloads) on your machine
- [ ] SSH keys set up for GitHub ([guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh))
- [ ] A code editor (we recommend [VS Code](https://code.visualstudio.com/))
- [ ] Basic familiarity with the command line

Don't have these yet? No problem! Click the links above to get set up.

## Step 1: Install uv

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that replaces pip, virtualenv, and more. This template uses uv to manage dependencies and virtual environments.

To install uv, follow the instructions [here](https://docs.astral.sh/uv/#getting-started) or use the commands below:

=== "macOS / Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows (PowerShell)"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

## Step 2: Generate your project

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

=== "macOS / Linux"

    ```bash
    uvx cookiecutter https://github.com/samuelduchesne/cookiecutter-project-kit.git
    ```

=== "Windows (PowerShell)"

    ```powershell
    uvx cookiecutter https://github.com/samuelduchesne/cookiecutter-project-kit.git
    ```

For an explanation of the prompt arguments, see
[Prompt Arguments](./prompt_arguments.md).

## Step 3: Set up your Github repository

Create an empty [new repository](https://github.com/new) on Github. Give
it a name that only contains alphanumeric characters and optionally `-`.
DO NOT check any boxes under the option `Initialize this repository
with`.

## Step 4: Upload your project to Github

Run the following commands, replacing `<project-name>` with the name
that you also gave the Github repository and `<github_author_handle>`
with your Github username.

=== "macOS / Linux"

    ```bash
    cd <project_name>
    git init -b main
    git add .
    git commit -m "Init commit"
    git remote add origin git@github.com:<github_author_handle>/<project_name>.git
    git push -u origin main
    ```

=== "Windows (PowerShell)"

    ```powershell
    cd <project_name>
    git init -b main
    git add .
    git commit -m "Init commit"
    git remote add origin git@github.com:<github_author_handle>/<project_name>.git
    git push -u origin main
    ```

## Step 5: Set Up Your Development Environment

Initially, the CI/CD pipeline will fail for two reasons:

- The project does not yet contain a `uv.lock` file
- There are a few formatting issues in the project

To fix that, we first install the environment and the pre-commit hooks:

=== "macOS / Linux"

    ```bash
    make install
    ```

=== "Windows (PowerShell)"

    Windows does not include `make` by default. You can either [install make](#windows-installing-make) or run the commands directly:

    ```powershell
    uv sync
    uv run pre-commit install
    ```

This will generate the `uv.lock` file.

## Step 6: Run the pre-commit hooks

Now, to resolve the formatting issues, stage your files and run the pre-commit hooks:

=== "macOS / Linux"

    ```bash
    git add .
    uv run pre-commit run -a
    ```

=== "Windows (PowerShell)"

    ```powershell
    git add .
    uv run pre-commit run -a
    ```

> **Note:** Pre-commit only checks staged files. Without `git add .` first, you'll see "no files to check".

You may see some hooks show "Failed" with "files were modified by this hook" — **this is normal!** It means the hooks automatically fixed formatting issues. The files have been updated and are ready to commit.

## Step 7: Commit the changes

Now we commit the changes made by the two steps above to the repository:

=== "macOS / Linux"

    ```bash
    git add .
    git commit -m 'Fix formatting issues'
    git push origin main
    ```

=== "Windows (PowerShell)"

    ```powershell
    git add .
    git commit -m "Fix formatting issues"
    git push origin main
    ```

## Step 8: Set up Codecov (optional)

If you enabled codecov for your project:

1. Sign up at [codecov.io](https://about.codecov.io/) with your GitHub account
2. For private repositories, you'll need to add a `CODECOV_TOKEN` secret:
    - Go to [app.codecov.io](https://app.codecov.io/) and find your repository
    - Copy the repository upload token
    - In GitHub, go to `Settings > Secrets and variables > Actions`
    - Add a new secret named `CODECOV_TOKEN` with the token value

For more details, see [Codecov setup](./features/codecov.md).

## Step 9: Configure PyPI publishing (optional)

If you want to publish your package to PyPI, see [Publishing to PyPI](./features/publishing.md#set-up-pypi-token).

## Step 10: Enable documentation

To deploy your documentation to GitHub Pages:

**1. Create a release** to trigger the documentation build:

- Go to your repository on GitHub
- Click `Releases` on the right sidebar
- Click `Draft a new release`
- Enter a tag using semantic version format (e.g., `0.1.0`, `1.0.0`)
- Add a title and click `Publish release`

**2. Enable GitHub Pages** (after the release workflow completes):

- Go to `Settings > Pages`
- Under `Source`, select the `gh-pages` branch
- Your docs will be available at `https://<username>.github.io/<project-name>/`

## Step 11: You're all set!

That's it! I hope this repository saved you a lot of manual configuration. If you have any improvement suggestions, feel
free to raise an issue or open a PR on Github!

---

## Windows: Installing Make

If you prefer using `make` commands on Windows, you can install it via:

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

---

## Troubleshooting

### "Not a git repository" error

If you see this when running `make install`:

    ❌ Error: Not a git repository. Run 'git init -b main' first.

**Solution:** Run `git init -b main` before `make install`. See Step 4 above.

---

### "Permission denied (publickey)" when pushing

If `git push` fails with a permission error:

    git@github.com: Permission denied (publickey).

**Solution:** Your SSH keys aren't set up correctly. Follow [GitHub's SSH guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) to configure them.

---

### Pre-commit shows "no files to check"

If you see `(no files to check)Skipped` for all hooks:

**Solution:** Stage your files first with `git add .`, then run pre-commit again.

---

### "uv: command not found"

If your terminal doesn't recognize `uv`:

**Solution:**

1. Close and reopen your terminal
2. If still not working, check that uv is in your PATH (see [uv installation docs](https://docs.astral.sh/uv/#getting-started))

---

### CI/CD pipeline fails on first push

This is expected! The pipeline fails because:

1. `uv.lock` wasn't committed yet
2. Pre-commit hooks haven't run to fix formatting

**Solution:** Follow Steps 5-7 in this tutorial to fix formatting and commit the lock file.

---

### Copilot Setup Steps workflow fails

If you see the "Copilot Setup Steps" workflow fail on your first push:

**This is expected!** This workflow is used by GitHub Copilot to set up the development environment. Like the Main workflow, it fails initially because `uv.lock` doesn't exist yet.

**Solution:** After completing Steps 5-7 (installing dependencies and committing the lock file), this workflow will pass on subsequent runs.

> **What is Copilot Setup Steps?** This workflow configures the environment for [GitHub Copilot Workspace](https://githubnext.com/projects/copilot-workspace/). If you don't use Copilot, you can safely ignore this workflow or delete `.github/workflows/copilot-setup-steps.yml`.
