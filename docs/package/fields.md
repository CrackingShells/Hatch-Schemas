# Package Schema Field Reference

This document provides detailed information about each field in the Package Schema.

## Required Fields

### package_schema_version

- **Type**: String
- **Pattern**: `^\d+\.\d+\.\d+$`
- **Description**: Version of the schema used for this package metadata
- **Example**: `"1.2.0"`

### name

- **Type**: String
- **Pattern**: `^[a-z0-9_]+$`
- **Description**: Package identifier. Must be lowercase alphanumeric with underscores.
- **Example**: `"my_package"` or `"image_classifier"`

### version

- **Type**: String
- **Pattern**: `^\d+(\.\d+)*$`
- **Description**: Semantic version of the package
- **Example**: `"1.0.0"` or `"2.1.3"`

### description

- **Type**: String
- **Description**: Human-readable description of the package
- **Example**: `"A package for image classification using deep learning"`

### tags

- **Type**: Array of strings
- **Description**: Keywords for package discovery
- **Example**: `["machine learning", "image", "classification"]`

### author

- **Type**: Object
- **Description**: Information about the package author
- **Required Properties**:
  - **name** (String): The name of the author
- **Optional Properties**:
  - **email** (String): The email address of the author (format: email)
- **Example**:
  ```json
  "author": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
  ```

### license

- **Type**: Object
- **Description**: License information for the package
- **Required Properties**:
  - **name** (String): The name of the license
- **Optional Properties**:
  - **uri** (String): URL to the license text (format: URI)
- **Example**:
  ```json
  "license": {
    "name": "MIT",
    "uri": "https://opensource.org/licenses/MIT"
  }
  ```

### entry_point

- **Type**: String
- **Description**: Primary entry point for the package
- **Example**: `"server.py"` or `"main.py"`

## Optional Fields

### contributors

- **Type**: Array of objects
- **Description**: List of additional contributors
- **Each Contributor**:
  - **Required Properties**:
    - **name** (String): The name of the contributor
  - **Optional Properties**:
    - **email** (String): The email address of the contributor (format: email)
- **Example**:
  ```json
  "contributors": [
    {
      "name": "Jane Smith",
      "email": "jane.smith@example.com"
    },
    {
      "name": "Bob Johnson"
    }
  ]
  ```

### repository

- **Type**: String
- **Format**: URI
- **Description**: URL to the source code repository
- **Example**: `"https://github.com/username/repository"`

### documentation

- **Type**: String
- **Format**: URI
- **Description**: URL to the package documentation
- **Example**: `"https://docs.example.com/my_package"`

### dependencies

- **Type**: Object
- **Description**: Dependencies required by the package
- **Properties**:
  - **hatch** (Array): Hatch package dependencies
  - **python** (Array): Python package dependencies
  - **system** (Array): System package dependencies
  - **docker** (Array): Docker image dependencies

#### hatch dependencies

- **Type**: Array of objects
- **Description**: Hatch packages required by this package
- **Each Dependency**:
  - **name** (String): Name of the Hatch package
  - **version_constraint** (String): Version constraint (e.g., ">=1.0.0")
- **Example**:
  ```json
  "hatch": [
    {
      "name": "base_package",
      "version_constraint": ">=1.0.0"
    }
  ]
  ```

#### python dependencies

- **Type**: Array of objects
- **Description**: Python packages required by this package
- **Each Dependency**:
  - **name** (String): Name of the Python package
  - **version_constraint** (String): Version constraint (e.g., ">=1.0.0")
  - **package_manager** (String, default: "pip"): Package manager to use
- **Example**:
  ```json
  "python": [
    {
      "name": "numpy",
      "version_constraint": ">=1.20.0"
    },
    {
      "name": "pandas",
      "version_constraint": ">=1.3.0"
    }
  ]
  ```

#### system dependencies

- **Type**: Array of objects
- **Description**: System packages required by this package
- **Each Dependency**:
  - **name** (String): Name of the system package
  - **version_constraint** (String): Version constraint
  - **package_manager** (String, default: "apt"): Package manager to use
- **Example**:
  ```json
  "system": [
    {
      "name": "libopencv-dev",
      "version_constraint": ">=4.0.0"
    }
  ]
  ```

#### docker dependencies

- **Type**: Array of objects
- **Description**: Docker images required by this package
- **Each Dependency**:
  - **name** (String): Name of the Docker image
  - **version_constraint** (String): Version constraint
  - **registry** (String, default: "dockerhub"): Registry to pull from
- **Example**:
  ```json
  "docker": [
    {
      "name": "postgres",
      "version_constraint": ">=13.0.0"
    }
  ]
  ```

### compatibility

- **Type**: Object
- **Description**: Compatibility requirements
- **Properties**:
  - **hatchling** (String): Version constraint for Hatchling
  - **python** (String): Version constraint for Python
- **Example**:
  ```json
  "compatibility": {
    "hatchling": ">=0.1.0",
    "python": ">=3.8"
  }
  ```

### tools

- **Type**: Array of objects
- **Description**: Additional tools provided by the package
- **Each Tool**:
  - **name** (String): Name of the tool
  - **description** (String): Description of the tool
- **Example**:
  ```json
  "tools": [
    {
      "name": "data_preprocessor",
      "description": "Preprocesses input data for the model"
    },
    {
      "name": "model_evaluator",
      "description": "Evaluates model performance on test data"
    }
  ]
  ```

### citations

- **Type**: Object
- **Description**: Citation information for the package.
- **Properties**:
  - **origin** (String): Citation for the original work. Free format.
  - **mcp** (String): Citation for the MCP implementation. Free format.
- **Example**:
  ```json
  "citations": {
    "origin": "Doe, J. et al. (2023). Novel image classification approach. Journal of AI Research, 45(2), 123-145.",
    "mcp": "Smith, J. (2023). MCP implementation of Doe's image classifier. https://doi.org/10.xxxx/xxxxx"
  }
  ```
