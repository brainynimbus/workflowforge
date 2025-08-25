"""
WorkflowForge - A robust and flexible library for creating GitHub Actions workflows.

This library allows you to create GitHub Actions workflows programmatically,
with type validation, autocompletion, and an intuitive API.
"""

from .workflow import Workflow
from .job import Job
from .step import Step, ActionStep, RunStep, action, run
from .triggers import (
    PushTrigger,
    PullRequestTrigger,
    ScheduleTrigger,
    WorkflowDispatchTrigger,
    ReleaseTrigger,
    on_push,
    on_pull_request,
    on_schedule,
    on_workflow_dispatch,
    on_release,
)
from .strategy import Strategy, Matrix, matrix, strategy
from .environment import Environment, environment
from .jenkins import (
    JenkinsPipeline,
    JenkinsStage,
    JenkinsAgent,
    agent_any,
    agent_docker,
    agent_label,
    stage,
    pipeline,
)
from .jenkins_plugins import (
    GitCheckout,
    DockerPlugin,
    SlackNotification,
    EmailNotification,
    ArtifactArchiver,
    JUnitPublisher,
    git_checkout,
    docker_run,
    slack_notify,
    email_notify,
    archive_artifacts,
    publish_junit,
)
from .codebuild import (
    BuildSpec,
    BuildPhase,
    BuildEnvironment,
    BuildArtifacts,
    BuildCache,
    buildspec,
    phase,
    environment,
    artifacts,
    cache,
)
from .secrets import (
    # GitHub Actions
    Secret,
    Variable,
    GitHubContext,
    secret,
    variable,
    github_context,
    # Jenkins
    JenkinsCredential,
    JenkinsEnvVar,
    JenkinsParam,
    jenkins_credential,
    jenkins_env,
    jenkins_param,
    # AWS CodeBuild
    CodeBuildSecret,
    CodeBuildParameter,
    CodeBuildEnvVar,
    codebuild_secret,
    codebuild_parameter,
    codebuild_env,
)
from .ai_documentation import (
    OllamaClient,
    generate_workflow_readme,
    ai_documentation_client,
)
from .visualization import (
    PipelineVisualizer,
    visualizer,
)
from .validation import (
    validate_job_name,
    validate_step_name,
    validate_secret_name,
    ValidationError,
)
from .templates import (
    python_ci_template,
    docker_build_template,
    node_ci_template,
    release_template,
)
from .schema_validation import (
    validate_github_actions_schema,
    validate_workflow_yaml,
)

__version__ = "1.0b1"
__all__ = [
    "Workflow",
    "Job",
    "Step",
    "ActionStep", 
    "RunStep",
    "action",
    "run",
    "PushTrigger",
    "PullRequestTrigger",
    "ScheduleTrigger",
    "WorkflowDispatchTrigger",
    "ReleaseTrigger",
    "on_push",
    "on_pull_request",
    "on_schedule",
    "on_workflow_dispatch",
    "on_release",
    "Strategy",
    "Matrix",
    "matrix",
    "strategy",
    "Environment",
    "environment",
    "JenkinsPipeline",
    "JenkinsStage",
    "JenkinsAgent",
    "agent_any",
    "agent_docker",
    "agent_label",
    "stage",
    "pipeline",
    "GitCheckout",
    "DockerPlugin",
    "SlackNotification",
    "EmailNotification",
    "ArtifactArchiver",
    "JUnitPublisher",
    "git_checkout",
    "docker_run",
    "slack_notify",
    "email_notify",
    "archive_artifacts",
    "publish_junit",
    "BuildSpec",
    "BuildPhase",
    "BuildEnvironment",
    "BuildArtifacts",
    "BuildCache",
    "buildspec",
    "phase",
    "environment",
    "artifacts",
    "cache",
    # Secrets and variables
    "Secret",
    "Variable",
    "GitHubContext",
    "secret",
    "variable",
    "github_context",
    "JenkinsCredential",
    "JenkinsEnvVar",
    "JenkinsParam",
    "jenkins_credential",
    "jenkins_env",
    "jenkins_param",
    "CodeBuildSecret",
    "CodeBuildParameter",
    "CodeBuildEnvVar",
    "codebuild_secret",
    "codebuild_parameter",
    "codebuild_env",
    # AI Documentation
    "OllamaClient",
    "generate_workflow_readme",
    "ai_documentation_client",
    # Visualization
    "PipelineVisualizer",
    "visualizer",
    # Validation
    "validate_job_name",
    "validate_step_name",
    "validate_secret_name",
    "ValidationError",
    # Templates
    "python_ci_template",
    "docker_build_template",
    "node_ci_template",
    "release_template",
    # Schema validation
    "validate_github_actions_schema",
    "validate_workflow_yaml",
]