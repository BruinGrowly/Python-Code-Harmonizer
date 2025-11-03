# Configuration

The Python Code Harmonizer can be configured to better suit your project's needs using a `.harmonizer.yml` file placed in your project's root directory.

This file allows you to customize file exclusion patterns and extend the Harmonizer's semantic vocabulary with your own domain-specific terms.

## Configuration File Structure

Here is an example of a `.harmonizer.yml` file with all available options:

```yaml
# .harmonizer.yml

# File and Directory Exclusion
exclude:
  - 'venv/'
  - 'tests/'
  - '**/test_*.py'
  - 'docs/'
  - 'build/'
  - '*.md'

# Custom Semantic Vocabulary
custom_vocabulary:
  invoice: justice
  payment: power
  ledger: justice
  audit: wisdom
  receipt: love
```

## `exclude`

The `exclude` key takes a list of glob patterns. Any file or directory matching these patterns will be ignored during analysis. This is useful for excluding virtual environments, test suites, documentation, or generated code.

**Common Patterns:**

-   `'venv/'`: Excludes a virtual environment directory.
-   `'tests/'`: Excludes the main test directory.
-   `'**/test_*.py'`: Excludes any file starting with `test_`.
-   `'build/'`: Excludes build artifacts.
-   `'*.md'`: Excludes all Markdown files.

## `custom_vocabulary`

The `custom_vocabulary` key allows you to extend the Harmonizer's built-in vocabulary with your own domain-specific terms. This is a powerful feature that lets you teach the Harmonizer the unique language of your project, making its analysis more accurate and relevant.

Map your custom keywords to one of the four core dimensions:

-   **`love`**: Connection, communication, sharing, community.
-   **`justice`**: Order, rules, validation, enforcement, structure.
-   **`power`**: Action, execution, modification, creation, deletion.
-   **`wisdom`**: Analysis, calculation, information retrieval, knowledge.

This is especially useful for business logic or scientific applications.

**Examples:**

-   **Financial Application:**
    -   `invoice: justice`
    -   `payment: power`
    -   `ledger: justice`
-   **Data Science Application:**
    -   `dataset: wisdom`
    -   `train_model: power`
    -   `predict: wisdom`
-   **Web Application:**
    -   `user_profile: wisdom`
    -   `session: love`
    -   `render_template: power`
