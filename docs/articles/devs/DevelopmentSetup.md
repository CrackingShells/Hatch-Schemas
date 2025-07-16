# Development Setup

This article is about:
- Setting up a development environment for Hatch Schemas
- Required tools and dependencies
- Testing and validation workflows

You will learn about:
- How to set up your development environment
- How to run tests and validation
- How to test schema changes locally

Setting up a proper development environment ensures you can contribute effectively to the Hatch Schemas project.

## Prerequisites

- **Git**: For version control
- **Python 3.8+**: For running validation scripts
- **Node.js** (optional): For additional JSON schema tools

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/CrackingShells/Hatch-Schemas.git
cd Hatch-Schemas
```

### 2. Install Python Dependencies

```bash
# Install required packages for validation
pip install jsonschema requests
```

### 3. Verify Setup

```bash
# Test schema loading
python examples/schema_updater.py
```

## Development Workflow

### Schema Validation

Test your schema changes:

```bash
# Validate package schema
python -c "
import jsonschema
import json

# Load schema
with open('package/v1.2.0/hatch_pkg_metadata_schema.json') as f:
    schema = json.load(f)

# Test with example data
test_data = {
    'package_schema_version': '1.2.0',
    'name': 'test_package',
    'version': '1.0.0',
    'description': 'Test package',
    'tags': ['test'],
    'author': {'name': 'Test User'},
    'license': {'name': 'MIT'},
    'entry_point': 'main.py'
}

jsonschema.validate(test_data, schema)
print('Schema validation passed!')
"
```

### Testing Changes

Before submitting changes:

1. **Validate All Schemas**: Ensure JSON schema syntax is correct
2. **Test Examples**: Verify example data validates against schemas
3. **Update Documentation**: Keep documentation in sync with schema changes
4. **Check CI**: Ensure automated tests pass

### Local Testing

Create test files to validate your changes:

```bash
# Create test package metadata
cat > test_package.json << 'EOF'
{
  "$schema": "./package/v1.2.0/hatch_pkg_metadata_schema.json",
  "package_schema_version": "1.2.0",
  "name": "test_package",
  "version": "1.0.0",
  "description": "Test package for development",
  "tags": ["test", "development"],
  "author": {
    "name": "Developer",
    "email": "dev@example.com"
  },
  "license": {
    "name": "MIT"
  },
  "entry_point": "main.py"
}
EOF

# Validate with jsonschema
python -c "
import jsonschema
import json

with open('test_package.json') as f:
    data = json.load(f)
with open('package/v1.2.0/hatch_pkg_metadata_schema.json') as f:
    schema = json.load(f)

jsonschema.validate(data, schema)
print('Validation successful!')
"
```

## CI/CD Pipeline

The project uses GitHub Actions for:

- **Schema Validation**: Ensuring all schemas are valid JSON Schema documents
- **Documentation Building**: Verifying documentation builds correctly
- **Release Automation**: Publishing versioned releases

## Debugging Tips

- Use online JSON Schema validators for quick testing
- Check schema syntax with JSON linters
- Validate against multiple example files
- Test both valid and invalid data

## See Also

- [Contributing Guidelines](Contributing.md)
- [Repository Structure](RepositoryStructure.md)
- [Schema Versioning](SchemaVersioning.md)