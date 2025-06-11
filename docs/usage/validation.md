# Schema Validation Guide

This document explains how to validate your JSON data against Hatch schemas.

## Validation Overview

Schema validation ensures that your metadata files comply with the expected structure. This helps catch errors early and ensures compatibility across the ecosystem.

## Validation Tools

### Using Python's jsonschema

The `jsonschema` package is a popular choice for schema validation in Python:

```python
import jsonschema
import json
from examples.schema_updater import load_schema

# Load your data
with open('my_package_metadata.json') as f:
    data = json.load(f)

# Load the schema
schema = load_schema("package")

# Validate
try:
    jsonschema.validate(data, schema)
    print("Package metadata is valid")
except jsonschema.ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"At path: {' > '.join([str(x) for x in e.path])}")
```

### Using Hatch Validator

The [Hatch-Validator](https://github.com/CrackingShells/Hatch-Validator) project provides a dedicated tool for validating Hatch metadata:

```bash
# Install directly from GitHub
pip install git+https://github.com/CrackingShells/Hatch-Validator.git

# Validate a package
hatch-validator validate-package path/to/hatch_metadata.json

# Validate a registry
hatch-validator validate-registry path/to/registry.json
```

### Using Online Validation

You can also use online JSON Schema validators like:

1. [JSONSchemaValidator.net](https://www.jsonschemavalidator.net/)
2. [JSON Schema Validator by Newtonsoft](https://jsonschema.net/)

Simply paste your schema and data to validate.

## Common Validation Issues

### Required Fields Missing

All required fields must be present. For package metadata, these include:
- package_schema_version
- name
- version
- entry_point
- description
- tags
- author
- license

### Format Errors

Some fields require specific formats:
- `name` must match pattern `^[a-z0-9_]+$` (lowercase alphanumeric + underscore)
- `version` must match pattern `^\d+(\.\d+)*$` (semantic versioning)
- URLs must be valid URIs
- Emails must be valid email addresses

### Dependency Constraints

Dependency version constraints must follow the specified pattern, e.g., `>=1.0.0`

## Advanced Validation

### Custom Validation Logic

For more complex validation requirements beyond JSON Schema:

```python
def validate_dependencies(data):
    """Custom validation for dependencies."""
    if 'dependencies' not in data:
        return True
        
    # Check for circular dependencies
    deps = data.get('dependencies', {}).get('hatch', [])
    dep_names = [d['name'] for d in deps]
    
    # Add your custom checks here
    
    return True
```

## See Also

- [Schema Access Guide](access.md)
- [Programmatic Usage Guide](programmatic.md)
