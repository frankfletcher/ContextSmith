# Contributing to ContextSmith

Thank you for your interest in contributing to ContextSmith! This document provides guidelines and instructions for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug, have a feature request, or notice a documentation issue, please open an issue on the [GitHub Issues](https://github.com/anomalyco/opencode/issues) page.

When reporting an issue, please include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)

### Pull Requests

We welcome pull requests for bug fixes, new features, and documentation improvements.

1. **Fork the repository** and create your branch from `main`.
2. **Clone your fork** locally.
3. **Create a feature branch** for your changes.
4. **Make your changes** following the coding standards below.
5. **Test your changes** thoroughly.
6. **Commit your changes** with a clear commit message.
7. **Push to your fork** and submit a pull request to the `main` branch.

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/anomalyco/opencode.git
   cd opencode
   ```

2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

3. Run the validation script to ensure everything is set up correctly:
   ```bash
   python scripts/validate_skills.py
   ```

### Coding Standards

- **Python**: Follow PEP 8 style guidelines.
- **Documentation**: Use clear, concise language. Avoid jargon when possible.
- **Commit Messages**: Use the conventional commits format.
- **Testing**: Write tests for new functionality. Ensure all tests pass before submitting.

### Validation and Testing

Before submitting a pull request, please run the following commands:

1. **Validate skills**:
   ```bash
   python scripts/validate_skills.py
   ```

2. **Sync references** (if you modified shared files):
   ```bash
   python scripts/sync_shared_refs.py --verbose
   ```

3. **Package a skill** (if you modified a skill):
   ```bash
   ./scripts/package_skill.sh <skill-name>
   ```

### Documentation Standards

- Keep documentation concise and actionable.
- Use the project's voice: practical, warm, and explanatory.
- Avoid generic AI-sounding contrast patterns.

### Code Review Process

All pull requests undergo review:
1. **Automated checks**: CI runs validation, linting, and tests.
2. **Human review**: Maintainers review for correctness, style, and security.
3. **Feedback**: Reviewers may request changes or provide suggestions.
4. **Approval**: Once approved, the PR will be merged.

### Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful, constructive, and patient in all interactions.

### License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions, please open an issue or contact the maintainers.
