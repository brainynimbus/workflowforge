"""Tests for workflow templates."""

import yaml

from workflowforge.templates import (
    docker_build_template,
    node_ci_template,
    python_ci_template,
)


def test_python_ci_template():
    """Test Python CI template."""
    workflow = python_ci_template(python_versions=["3.11", "3.12"])
    yaml_output = workflow.to_yaml()

    parsed = yaml.safe_load(yaml_output)
    assert parsed["name"] == "Python CI"
    assert "test" in parsed["jobs"]
    assert "strategy" in parsed["jobs"]["test"]
    # Ensure matrix variable name matches the matrix key (python_version)
    steps = parsed["jobs"]["test"]["steps"]
    setup_step = next(
        (step for step in steps if step.get("uses") == "actions/setup-python@v5"),
        None,
    )
    assert setup_step, "Missing actions/setup-python@v5 step"
    assert setup_step["with"]["python-version"] == "${{ matrix.python_version }}"


def test_docker_build_template():
    """Test Docker build template."""
    workflow = docker_build_template(image_name="my-app")
    yaml_output = workflow.to_yaml()

    parsed = yaml.safe_load(yaml_output)
    assert parsed["name"] == "Docker Build"
    assert "build" in parsed["jobs"]


def test_node_ci_template():
    """Test Node.js CI template."""
    workflow = node_ci_template(node_versions=["18", "20"])
    yaml_output = workflow.to_yaml()

    parsed = yaml.safe_load(yaml_output)
    assert parsed["name"] == "Node.js CI"
    assert "test" in parsed["jobs"]
    # Ensure matrix variable name matches the matrix key (node_version)
    steps = parsed["jobs"]["test"]["steps"]
    setup_step = next(
        (step for step in steps if step.get("uses") == "actions/setup-node@v4"),
        None,
    )
    assert setup_step, "Missing actions/setup-node@v4 step"
    assert setup_step["with"]["node-version"] == "${{ matrix.node_version }}"
