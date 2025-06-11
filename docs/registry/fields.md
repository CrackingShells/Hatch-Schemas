# Registry Schema Field Reference

This document provides detailed information about each field in the Registry Schema.

## Required Fields

### registry_schema_version

- **Type**: String
- **Pattern**: `^\d+(\.\d+)*$`
- **Description**: Version of this registry schema
- **Example**: `"1.2.0"`

### last_updated

- **Type**: String
- **Format**: date-time
- **Description**: Timestamp of when the registry was last updated
- **Example**: `"2024-06-01T12:00:00Z"`

### repositories

- **Type**: Array of objects
- **Description**: List of repositories containing packages
- **Each Repository**: See [Repository Object](#repository-object)

### stats

- **Type**: Object
- **Description**: Registry-wide statistics
- **Properties**:
  - **total_packages** (Integer): Total number of unique packages
  - **total_versions** (Integer): Total number of package versions
- **Example**:
  ```json
  "stats": {
    "total_packages": 10,
    "total_versions": 25
  }
  ```

## Object Definitions

### Repository Object

- **Type**: Object
- **Description**: Repository containing packages
- **Required Properties**:
  - **name** (String): Repository name (e.g., 'Hatch-Dev')
  - **url** (String, format: URI): URL to the repository
  - **packages** (Array): List of packages in this repository (see [Package Object](#package-object))
  - **last_indexed** (String, format: date-time): When this repository was last indexed
- **Example**:
  ```json
  {
    "name": "Hatch-Dev",
    "url": "https://github.com/crackingshells/Hatch-Dev",
    "last_indexed": "2024-06-01T12:00:00Z",
    "packages": [...]
  }
  ```

### Package Object

- **Type**: Object
- **Description**: Package within a repository
- **Required Properties**:
  - **name** (String): Package identifier (pattern: `^[a-z0-9_]+$`)
  - **description** (String): Human-readable description of the package
  - **tags** (Array of strings): Keywords for discovery
  - **versions** (Array of objects): Available versions of this package (see [Version Object](#version-object))
  - **latest_version** (String): Latest version of the package (pattern: `^\d+(\.\d+)*$`)
- **Example**:
  ```json
  {
    "name": "example_package",
    "description": "An example Hatch package",
    "tags": ["example", "demo"],
    "latest_version": "1.2.0",
    "versions": [...]
  }
  ```

### Version Object

- **Type**: Object
- **Description**: Version of a package
- **Required Properties**:
  - **version** (String): Semantic version of the package (pattern: `^\d+(\.\d+)*$`)
  - **author** (Object): Author of the submission of this version
    - **GitHubID** (String): GitHub username of the author
    - **email** (String, format: email): Email of the author
  - **release_uri** (String, format: URI): URI to the release page for this version
  - **added_date** (String, format: date-time): When this version was added to the registry
- **Optional Properties**:
  - **base_version** (String): Version this differential is based on (null for first version)
  - **dependency_changes** (Object): Changes to dependencies since base_version
  - **compatibility_changes** (Object): Changed compatibility constraints since base_version
  - **verification** (Object): Verification status and metadata
- **Example**:
  ```json
  {
    "version": "1.2.0",
    "author": {
      "GitHubID": "johndoe",
      "email": "john.doe@example.com"
    },
    "release_uri": "https://github.com/crackingshells/Hatch-Dev/releases/tag/example_package-v1.2.0",
    "base_version": "1.1.0",
    "added_date": "2024-05-15T10:30:00Z",
    "verification": {
      "status": "verified",
      "timestamp": "2024-05-16T14:20:00Z",
      "verifier": {
        "GitHubID": "packagereviewer",
        "email": "reviewer@example.com"
      },
      "notes": "All tests passed"
    }
  }
  ```

### Dependency Changes Object

- **Type**: Object
- **Description**: Changes to dependencies since base_version
- **Properties**:
  - **hatch** (Object): Changes to Hatch dependencies
  - **python** (Object): Changes to Python dependencies
  - **system** (Object): Changes to system dependencies
  - **docker** (Object): Changes to Docker dependencies
- **Each Dependency Type**:
  - **added** (Array): Dependencies added since base_version
  - **removed** (Array): Names of dependencies removed since base_version
  - **modified** (Array): Dependencies with modified version constraints
- **Example**:
  ```json
  "dependency_changes": {
    "hatch": {
      "added": [
        {
          "name": "new_dependency",
          "version_constraint": ">=1.0.0"
        }
      ],
      "removed": ["old_dependency"],
      "modified": [
        {
          "name": "existing_dependency",
          "old_version_constraint": ">=1.0.0",
          "new_version_constraint": ">=1.2.0"
        }
      ]
    }
  }
  ```

### Compatibility Changes Object

- **Type**: Object
- **Description**: Changed compatibility constraints since base_version
- **Properties**:
  - **hatchling** (String): Changed version constraint for Hatchling compatibility
  - **python** (String): Changed version constraint for Python compatibility
- **Example**:
  ```json
  "compatibility_changes": {
    "hatchling": ">=0.2.0",
    "python": ">=3.9"
  }
  ```

### Verification Object

- **Type**: Object
- **Description**: Verification metadata for a package version
- **Required Properties**:
  - **status** (String, enum): Verification status
    - Values: "unverified", "validated", "reviewed", "verified", "deprecated"
    - Default: "unverified"
- **Optional Properties**:
  - **timestamp** (String, format: date-time): When this verification status was last updated
  - **verifier** (Object): Entity that performed the verification
    - **GitHubID** (String): GitHub username of the verifier
    - **email** (String, format: email): Email of the verifier
    - **name** (String): Name of the verifier
  - **notes** (String): Additional information about verification status
- **Example**:
  ```json
  "verification": {
    "status": "verified",
    "timestamp": "2024-05-16T14:20:00Z",
    "verifier": {
      "GitHubID": "packagereviewer",
      "email": "reviewer@example.com",
      "name": "Package Reviewer"
    },
    "notes": "All tests passed, code review completed"
  }
  ```
