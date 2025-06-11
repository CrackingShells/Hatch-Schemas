# Package Schema Documentation

## Overview

The Package Schema (`hatch_pkg_metadata_schema.json`) defines the structure for individual package metadata files in the Hatch ecosystem. This schema ensures consistency and validity of package metadata across the ecosystem.

## Current Version

The current version of the Package Schema is **v1.2.0**.

## Schema Structure

The Package Schema includes the following major sections:

- **Basic Package Information**: Schema version, name, version, description, and tags
- **Author Information**: Author details and optional contributors list
- **License Information**: License name and optional URI
- **Package Links**: Repository and documentation URLs
- **Dependencies**: Hatch, Python, system, and Docker dependencies
- **Compatibility Requirements**: Hatchling and Python version constraints
- **Entry Points and Tools**: Primary entry point and additional tools

For detailed field-by-field documentation including types, formats, and examples, see the [Package Schema Field Reference](fields.md).

### Compatibility

- **compatibility**: Object defining compatibility requirements (optional)
  - **hatchling**: Version constraint for Hatchling compatibility
  - **python**: Version constraint for Python compatibility

### Entry Points and Tools

- **entry_point**: Primary entry point for the package (required)
- **tools**: List of additional tools provided by the package (optional)

### Citations

- **citations**: Citation information for the package (optional)
  - **origin**: Citation for the original work
  - **mcp**: Citation for the MCP implementation

## Example

```json
{
  "package_schema_version": "1.2.0",
  "name": "example_package",
  "version": "1.0.0",
  "description": "An example Hatch package",
  "tags": ["example", "demo"],
  "author": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "license": {
    "name": "MIT",
    "uri": "https://opensource.org/licenses/MIT"
  },
  "entry_point": "server.py",
  "dependencies": {
    "hatch": [
      {
        "name": "base_package",
        "version_constraint": ">=1.0.0"
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
      }
    ]
  },
  "compatibility": {
    "python": ">=3.8"
  }
}
```

## See Also

- [Registry Schema](../registry/overview.md)
- [Schema Validation Guide](../usage/validation.md)
