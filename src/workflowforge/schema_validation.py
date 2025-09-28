"""GitHub Actions workflow validation helpers."""

from typing import Any

from ruamel.yaml import YAML

# GitHub Actions allows a long tail of events and fields. The goal here is to
# cover the most common ones while keeping the validator lightweight.
GITHUB_ACTIONS_SCHEMA = {
    "required_fields": ["name", "on", "jobs"],
    "valid_triggers": [
        "branch_protection_rule",
        "check_run",
        "check_suite",
        "create",
        "delete",
        "deployment",
        "deployment_status",
        "discussion",
        "discussion_comment",
        "fork",
        "gollum",
        "issues",
        "issue_comment",
        "label",
        "merge_group",
        "milestone",
        "page_build",
        "project",
        "project_card",
        "project_column",
        "public",
        "pull_request",
        "pull_request_comment",
        "pull_request_review",
        "pull_request_review_comment",
        "pull_request_target",
        "push",
        "registry_package",
        "release",
        "repository_dispatch",
        "schedule",
        "status",
        "watch",
        "workflow_call",
        "workflow_dispatch",
        "workflow_run",
    ],
    "valid_job_fields": [
        "concurrency",
        "container",
        "continue-on-error",
        "defaults",
        "environment",
        "env",
        "if",
        "name",
        "needs",
        "outputs",
        "permissions",
        "runs-on",
        "secrets",
        "services",
        "steps",
        "strategy",
        "timeout-minutes",
        "uses",
        "with",
    ],
    "valid_step_fields": [
        "continue-on-error",
        "env",
        "id",
        "if",
        "name",
        "run",
        "shell",
        "timeout-minutes",
        "uses",
        "with",
        "working-directory",
    ],
}


def validate_github_actions_schema(workflow_dict: dict[str, Any]) -> list[str]:
    """Validate a workflow dictionary against a curated GitHub Actions schema."""

    errors: list[str] = []

    if not isinstance(workflow_dict, dict):
        return ["Workflow definition must be a mapping at the top level"]

    # Ensure the top-level required fields are present.
    for field in GITHUB_ACTIONS_SCHEMA["required_fields"]:
        if field not in workflow_dict:
            errors.append(f"Missing required field: {field}")

    # Validate triggers and highlight unknown events.
    on_value = workflow_dict.get("on")
    if isinstance(on_value, str):
        if on_value not in GITHUB_ACTIONS_SCHEMA["valid_triggers"]:
            errors.append(f"Invalid trigger: {on_value}")
    elif isinstance(on_value, dict):
        for trigger in on_value.keys():
            if trigger not in GITHUB_ACTIONS_SCHEMA["valid_triggers"]:
                errors.append(f"Invalid trigger: {trigger}")

    jobs = workflow_dict.get("jobs")
    if not isinstance(jobs, dict):
        if jobs is not None:
            errors.append("'jobs' must be a mapping of job definitions")
        return errors

    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            errors.append(f"Job '{job_name}' must be an object")
            continue

        if "runs-on" not in job_config and "uses" not in job_config:
            errors.append(
                f"Job '{job_name}' must define either 'runs-on' or 'uses' for reusable workflows"
            )

        for field in job_config.keys():
            if field not in GITHUB_ACTIONS_SCHEMA["valid_job_fields"]:
                errors.append(f"Invalid job field in '{job_name}': {field}")

        steps = job_config.get("steps")
        if steps is None:
            # Reusable workflows are valid without explicit steps.
            continue

        if not isinstance(steps, list):
            errors.append(f"Job '{job_name}' steps must be provided as a list")
            continue

        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                errors.append(f"Step {index} in job '{job_name}' must be an object")
                continue

            if "uses" not in step and "run" not in step:
                errors.append(
                    f"Step {index} in job '{job_name}' must include either 'uses' or 'run'"
                )

            for field in step.keys():
                if field not in GITHUB_ACTIONS_SCHEMA["valid_step_fields"]:
                    errors.append(
                        f"Invalid step field in job '{job_name}', step {index}: {field}"
                    )

    return errors


def validate_yaml_syntax(yaml_content: str) -> list[str]:
    """Validate YAML syntax."""
    errors = []
    try:
        yaml = YAML(typ="safe")
        yaml.load(yaml_content)
    except Exception as e:
        errors.append(f"YAML syntax error: {str(e)}")
    return errors


def validate_workflow_yaml(yaml_content: str) -> list[str]:
    """Complete workflow validation."""
    errors = []

    # First validate YAML syntax
    yaml_errors = validate_yaml_syntax(yaml_content)
    if yaml_errors:
        return yaml_errors

    # Parse and validate structure
    try:
        yaml = YAML(typ="safe")
        workflow_dict = yaml.load(yaml_content)
        schema_errors = validate_github_actions_schema(workflow_dict)
        errors.extend(schema_errors)
    except Exception as e:
        errors.append(f"Validation error: {str(e)}")

    return errors
