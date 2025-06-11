# Package Schema Examples

This document provides examples of valid package metadata files compliant with the Hatch Package Schema.

## Basic Example

```json
{
  "$schema": "https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1.2.0/hatch_pkg_metadata_schema.json",
  "package_schema_version": "1.2.0",
  "name": "simple_package",
  "version": "1.0.0",
  "description": "A simple example package",
  "tags": ["example", "simple"],
  "author": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "license": {
    "name": "MIT"
  },
  "entry_point": "server.py"
}
```

## Complete Example

```json
{
  "$schema": "https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1.2.0/hatch_pkg_metadata_schema.json",
  "package_schema_version": "1.2.0",
  "name": "complete_package",
  "version": "1.2.0",
  "description": "A comprehensive example with all possible fields",
  "tags": ["example", "complete", "reference"],
  "author": {
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  },
  "contributors": [
    {
      "name": "John Doe",
      "email": "john.doe@example.com"
    },
    {
      "name": "Alice Johnson"
    }
  ],
  "license": {
    "name": "MIT",
    "uri": "https://opensource.org/licenses/MIT"
  },
  "repository": "https://github.com/crackingshells/example-package",
  "documentation": "https://docs.example.com/package",
  "dependencies": {
    "hatch": [
      {
        "name": "base_package",
        "version_constraint": ">=1.0.0"
      },
      {
        "name": "utils_package",
        "version_constraint": "==1.2.0"
      }
    ],
    "python": [
      {
        "name": "numpy",
        "version_constraint": ">=1.20.0"
      },
      {
        "name": "pandas",
        "version_constraint": ">=1.3.0"
      },
      {
        "name": "scikit-learn",
        "version_constraint": ">=1.0.0"
      }
    ],
    "system": [
      {
        "name": "libopencv-dev",
        "version_constraint": ">=4.0.0",
        "package_manager": "apt"
      }
    ],
    "docker": [
      {
        "name": "postgres",
        "version_constraint": ">=13.0.0",
        "registry": "dockerhub"
      }
    ]
  },
  "compatibility": {
    "hatchling": ">=0.1.0",
    "python": ">=3.8"
  },
  "entry_point": "server.py",
  "tools": [
    {
      "name": "data_preprocessor",
      "description": "Preprocesses input data for the model"
    },
    {
      "name": "model_evaluator",
      "description": "Evaluates model performance on test data"
    }
  ],
  "citations": {
    "origin": "Smith, J. et al. (2023). Advanced machine learning techniques. Journal of AI Research, 45(2), 123-145.",
    "mcp": "Doe, J. (2023). MCP implementation of Smith's algorithms. https://doi.org/10.xxxx/xxxxx"
  }
}
```

## See Also

- [Package Schema Field Reference](fields.md)
- [Registry Schema Examples](../registry/examples.md)
