#!/usr/bin/env python3
"""
Dogfood generator: create the GitHub Actions workflow to publish to PyPI/TestPyPI
using the WorkflowForge library itself.

Generates: .github/workflows/publish.yml

Adds a release guard to ensure the tag version matches pyproject.toml version
before publishing to PyPI.
"""

from workflowforge import github_actions as gh
from workflowforge.environment import environment


def build_workflow() -> gh.Workflow:
    wf = gh.workflow(
        name="Publish WorkflowForge to PyPI",
        on=[
            gh.on_push(branches=["main"]),
            gh.on_pull_request(branches=["main"]),
            gh.on_release(types=["published"]),
        ],
    )

    # -------------------- test (matrix) --------------------
    test_job = gh.job(
        runs_on="ubuntu-latest",
        strategy=gh.strategy(matrix=gh.matrix(python_version=["3.11", "3.12", "3.13"])),
    )
    test_job.add_step(gh.action("actions/checkout@v4", name="Checkout code"))
    test_job.add_step(
        gh.action(
            "actions/setup-python@v5",
            name="Set up Python ${{ matrix.python_version }}",
            with_={"python-version": "${{ matrix.python_version }}"},
        )
    )
    test_job.add_step(gh.run("python -m pip install --upgrade pip", name="Install pip"))
    test_job.add_step(gh.run("pip install -e .[dev]", name="Install dependencies"))
    test_job.add_step(gh.run("black --check src/ tests/", name="Check code formatting"))
    test_job.add_step(
        gh.run("isort --check-only src/ tests/", name="Check import sorting")
    )
    test_job.add_step(gh.run("flake8 src/ tests/ examples/", name="Lint with flake8"))
    test_job.add_step(
        gh.run(
            "mypy --install-types --non-interactive src/", name="Type check with mypy"
        )
    )
    test_job.add_step(
        gh.run(
            "pytest tests/ --cov=workflowforge --cov-report=xml",
            name="Run tests with coverage",
        )
    )
    wf.add_job("test", test_job)

    # -------------------- security --------------------
    sec_job = gh.job(runs_on="ubuntu-latest")
    sec_job.add_step(gh.action("actions/checkout@v4", name="Checkout code"))
    sec_job.add_step(
        gh.action(
            "actions/setup-python@v5",
            name="Set up Python",
            with_={"python-version": "3.11"},
        )
    )
    sec_job.add_step(
        gh.run(
            "pip install bandit safety",
            name="Install security tools",
        )
    )
    sec_job.add_step(gh.run("bandit -r src/", name="Security scan with Bandit"))
    sec_job.add_step(
        gh.run(
            "safety check --ignore-unpinned"
            " || echo 'Safety check completed with warnings'",
            name="Check dependencies for vulnerabilities",
        )
    )
    wf.add_job("security", sec_job)

    # -------------------- build --------------------
    build_job = gh.job(runs_on="ubuntu-latest")
    build_job.set_needs("test", "security")
    build_job.add_step(gh.action("actions/checkout@v4", name="Checkout code"))
    build_job.add_step(
        gh.action(
            "actions/setup-python@v5",
            name="Set up Python",
            with_={"python-version": "3.11"},
        )
    )
    build_job.add_step(
        gh.run(
            "python -m pip install --upgrade pip build twine",
            name="Install build tools",
        )
    )
    build_job.add_step(gh.run("python -m build", name="Build package"))

    # Version guard for release events (tag vs pyproject version)
    guard_script = (
        'echo "Verifying tag matches pyproject version for release runs..."\n'
        "PYPROJECT_VERSION=$(python - <<'PY'\n"
        "import tomllib\n"
        "with open('pyproject.toml', 'rb') as f:\n"
        "    data = tomllib.load(f)\n"
        "print(data['project']['version'])\n"
        "PY\n"
        ")\n"
        "TAG_NAME=${GITHUB_REF_NAME#v}\n"
        'echo "pyproject version: ${PYPROJECT_VERSION}"\n'
        'echo "tag version     : ${TAG_NAME}"\n'
        'if [ "${{ github.event_name }}" = "release" ] && '
        ' [ "$PYPROJECT_VERSION" != "$TAG_NAME" ]; then\n'
        '  echo "ERROR: Version mismatch '
        ' (pyproject=$PYPROJECT_VERSION tag=$TAG_NAME). Aborting." >&2\n'
        "  exit 1\n"
        "fi\n"
    )
    build_job.add_step(
        gh.run(guard_script, name="Verify tag and project version match")
    )
    build_job.add_step(gh.run("twine check dist/*", name="Verify package metadata"))
    build_job.add_step(
        gh.action(
            "actions/upload-artifact@v4",
            name="Upload build artifacts",
            with_={"name": "dist", "path": "dist/"},
        )
    )
    wf.add_job("build", build_job)

    # -------------------- publish to TestPyPI on push to main --------------------
    testpypi = gh.job(
        runs_on="ubuntu-latest",
        environment=environment("testpypi", "https://test.pypi.org/p/workflowforge"),
        permissions={"id-token": "write"},
    )
    testpypi.set_needs("build")
    testpypi.set_condition(
        "github.ref == 'refs/heads/main' && github.event_name == 'push'"
    )
    testpypi.add_step(
        gh.action(
            "actions/download-artifact@v4",
            name="Download build artifacts",
            with_={"name": "dist", "path": "dist/"},
        )
    )
    testpypi.add_step(
        gh.action(
            "pypa/gh-action-pypi-publish@release/v1",
            name="Publish to TestPyPI",
            with_={
                "repository-url": "https://test.pypi.org/legacy/",
                "skip-existing": "true",
                "verify-metadata": "true",
                "print-hash": "true",
            },
        )
    )
    wf.add_job("publish-testpypi", testpypi)

    # -------------------- publish to PyPI on release --------------------
    pypi = gh.job(
        runs_on="ubuntu-latest",
        environment=environment("pypi", "https://pypi.org/p/workflowforge"),
        permissions={"id-token": "write"},
    )
    pypi.set_needs("build")
    pypi.set_condition("github.event_name == 'release'")
    pypi.add_step(
        gh.action(
            "actions/download-artifact@v4",
            name="Download build artifacts",
            with_={"name": "dist", "path": "dist/"},
        )
    )
    pypi.add_step(
        gh.action(
            "pypa/gh-action-pypi-publish@release/v1",
            name="Publish to PyPI",
            with_={
                "skip-existing": "true",
                "verify-metadata": "true",
                "print-hash": "true",
            },
        )
    )
    wf.add_job("publish-pypi", pypi)

    return wf


def main() -> None:
    wf = build_workflow()
    wf.save(
        ".github/workflows/publish.yml", generate_readme=False, generate_diagram=False
    )
    print("✅ Generated .github/workflows/publish.yml")


if __name__ == "__main__":
    main()
