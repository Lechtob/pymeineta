# Contributing to pymeineta

Thank you for your interest in contributing to **pymeineta**! We appreciate your help in making this project better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Style Guide](#style-guide)
- [Testing](#testing)
- [Questions](#questions)

---

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## How Can I Contribute?

### Reporting Bugs

If you find a bug in **pymeineta**, please open an [Issue](https://github.com/lechtob/pymeineta/issues) with detailed information about the problem.

### Suggesting Enhancements

We welcome suggestions for new features or improvements. Please open an [Issue](https://github.com/lechtob/pymeineta/issues) to discuss your ideas.

### Pull Requests

Contributions via pull requests are welcome! Follow these steps:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Implement your changes** and ensure they adhere to the project's style guide.
4. **Add corresponding tests** for your changes.
5. **Ensure all tests pass**:
    ```bash
    pytest
    ```
6. **Commit and push** your changes:
    ```bash
    git commit -m "Add feature: Your feature description"
    git push origin feature/your-feature-name
    ```
7. **Create a Pull Request** on GitHub, describing your changes in detail.

Please make sure your contributions are well-documented and tested.

## Style Guide

- Follow [PEP 8](https://pep8.org/) for Python code style.
- Use meaningful variable and function names.
- Write clear and concise docstrings for modules, classes, and functions using the [Google Style](https://google.github.io/styleguide/pyguide.html) or [NumPy Style](https://numpydoc.readthedocs.io/en/latest/format.html).
- Ensure code is formatted using `black`:
    ```bash
    black .
    ```

## Testing

- Write tests using `pytest`.
- Ensure all tests pass before submitting a pull request:
    ```bash
    pytest
    ```

## Questions

If you have any questions or need assistance, feel free to open an [Issue](https://github.com/lechtob/pymeineta/issues) or contact us directly at [tobiaslechenauer@gmail.com](mailto:tobiaslechenauer@gmail.com).
