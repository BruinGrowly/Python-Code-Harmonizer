# Contributing to the Python Code Harmonizer

First off, thank you for considering contributing! This project is a unique blend of philosophy and code, and your help is welcome in making it better.

## Getting Started

To get the project set up for local development, please follow these steps:

1.  **Fork and Clone:**
    *   Fork the repository on GitHub.
    *   Clone your fork to your local machine:
        ```sh
        git clone https://github.com/YOUR_USERNAME/Python-Code-Harmonizer.git
        cd Python-Code-Harmonizer
        ```

2.  **Set Up a Virtual Environment:**
    *   It is highly recommended to use a virtual environment to keep dependencies isolated.
        ```sh
        python -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install Dependencies:**
    *   The project and all its development dependencies can be installed with a single command. The `-e` flag installs the project in "editable" mode, which is essential for development.
        ```sh
        pip install -r requirements.txt
        pip install -e .
        ```

## Running the Tools

### Running the Harmonizer

Once installed, you can run the harmonizer on any Python file using the `harmonizer` command-line script:

```sh
harmonizer examples/test_code.py
```

### Running the Test Suite

This project uses `pytest` for testing. To run the full suite:

```sh
pytest
```

## Code Quality and Style

We use `black` for code formatting and `flake8` for linting to ensure a consistent and high-quality codebase.

### Formatting

Before you commit your changes, please run `black` to automatically format your code:

```sh
black harmonizer/ tests/
```

### Linting

You can check for any style issues or potential errors with `flake8`:

```sh
flake8 harmonizer/ tests/
```

Our Continuous Integration (CI) pipeline will automatically check for formatting and linting issues, so it's a good idea to run these tools locally before pushing your changes.

## Submitting a Pull Request

1.  Create a new branch for your feature or bug fix.
2.  Make your changes, and be sure to add tests if you are adding new functionality.
3.  Ensure your code is formatted with `black` and passes the `flake8` checks.
4.  Make sure the full test suite passes with `pytest`.
5.  Push your branch to your fork and open a pull request.

Thank you for your contributions!
