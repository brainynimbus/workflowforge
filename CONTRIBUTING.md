# Contributing to WorkflowForge

We welcome contributions that improve WorkflowForge's developer experience, platform support, and documentation. This guide explains how to get started, follow our coding conventions, and submit high-quality pull requests.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Checklist](#pull-request-checklist)
- [Release Process](#release-process)

## Code of Conduct

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it carefully and report any concerns at once.

## Getting Started

- Fork the repository and clone your fork.
- Create and activate a Python 3.11+ virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
- Install development dependencies:
    ```bash
    pip install -e .[dev]
    pre-commit install
    ```

## Development Workflow

- Use feature branches named after the work you are doing (e.g., `feature/github-actions-schedules`).
- Keep commits small, focused, and rebased on the latest `main` branch.
- Follow the Conventional Commit format **with mandatory scopes**. Examples:
    - `feat(github-actions): support reusable workflows`
    - `fix(templates): correct matrix variable references`
    - `docs(readme): clarify setup instructions`
- Open a pull request for your branch and fully complete the pull request template before requesting review.

## Coding Standards

- **Formatting**: Use `black` (line length 88) and `isort` with the `black` profile.
- **Linting**: Run `flake8`, `ruff format`, and `ruff check` if available.
- **Typing**: Enforce `mypy --install-types --non-interactive src/`.
- **Security**: Execute `bandit -r src/` and `safety check --ignore-unpinned-requirements` for dependency audits.
- **Documentation**: Keep docstrings in English and favour concise, explanatory comments when needed.

## Testing Requirements

Before opening a pull request, ensure the following pass locally:

```bash
black --check src/ tests/
isort --check-only src/ tests/
flake8 src/ tests/ examples/
mypy --install-types --non-interactive src/
pytest tests/ --cov=workflowforge --cov-report=xml
bandit -r src/
safety check --ignore-unpinned-requirements
python -m build
python -m twine check dist/*
```

Execute the runnable examples under `examples/` relevant to your change, especially when modifying templates or generators.

## Pull Request Checklist

Include the completed pull request template to help reviewers understand scope and validation. Double-check that:

- [ ] The branch merges cleanly into `main`.
- [ ] All CI checks pass.
- [ ] Tests and linters were executed as listed above.
- [ ] Documentation (README, CHANGELOG, examples) was updated when behaviour changes.
- [ ] Commits follow `type(scope): description`.

## Release Process

Maintainers: when preparing a release, update `pyproject.toml`, `src/workflowforge/__init__.py`, and `CHANGELOG.md` together. Tag releases with the `vX.Y.Z` format and verify the tag guard in `.github/workflows/publish.yml` passes before publishing.

Thank you for helping make WorkflowForge better!
