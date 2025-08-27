# Changelog

All notable changes to WorkflowForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0b4] - 2024-12-19

### Added
- TRUE dogfooding: WorkflowForge generates its own GitHub Actions workflows
- Professional CI/CD pipeline with Python 3.11, 3.12, 3.13 test matrix
- Security scanning integration with Bandit and Safety tools
- OIDC trusted publishing for PyPI deployment (no API tokens needed)
- Automated TestPyPI publishing on main branch merges

### Changed
- Enhanced publish workflow with comprehensive quality checks
- Integrated security scanning into CI/CD pipeline
- Improved project automation with self-generated workflows

### Fixed
- Removed generated diagram artifacts to maintain clean repository
- Eliminated image pollution in project structure

## [1.0b3] - 2024-12-19

### Added
- Strict mypy configuration with Pydantic plugin for enhanced type safety
- Professional quality badges in README (mypy, black, isort, ruamel.yaml)
- Comprehensive pre-commit hooks including yamllint for generated files
- GitHub Actions publish workflow with proper ruamel.yaml formatting

### Changed
- **BREAKING**: Migrated from PyYAML to ruamel.yaml for superior YAML generation
- **BREAKING**: Removed legacy import compatibility - use platform-specific modules only
- Translated all Spanish docstrings and comments to English for professional codebase
- Improved YAML formatting with precise indentation (mapping=2, sequence=4, offset=2)
- Enhanced code quality with flake8, black, and isort integration
- Streamlined module exports to platform-specific imports only

### Fixed
- All flake8 code style issues resolved (F541, E501, E712, E999)
- YAML validation now passes with proper indentation and formatting
- Boolean comparisons in tests simplified to Pythonic style
- Line length violations fixed across entire codebase
- Pre-commit hooks now pass successfully on all files

### Removed
- Legacy backwards compatibility imports from __init__.py
- Spanish language docstrings and comments
- PyYAML dependency in favor of ruamel.yaml
- npm-groovy-lint from pre-commit (simplified validation)

## [1.0b2] - 2024-12-18

### Added
- Initial release with GitHub Actions, Jenkins, and AWS CodeBuild support
- Pydantic-based models for type safety and validation
- AI-powered documentation generation with Ollama
- Pipeline visualization with Graphviz
- Comprehensive examples and templates
- Pre-commit hooks for code quality

### Features
- Platform-specific modules: github_actions, jenkins_platform, aws_codebuild
- Type-safe pipeline generation with IDE autocompletion
- YAML/Groovy output with validation
- Modular architecture with clean API design
