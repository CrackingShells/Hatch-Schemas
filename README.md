# Hatch-Schemas

JSON schemas for the CrackingShells organization package ecosystem.

## Available Schemas

This repository contains JSON schemas for validating Hatch metadata:

- **Package Schema**: Validates individual package metadata
  - Latest: `package/v1/hatch_pkg_metadata_schema.json`
  - Versioned: `package/v1/hatch_pkg_metadata_schema.json`

- **Registry Schema**: Validates the central package registry
  - Latest: `registry/v1/hatch_all_pkg_metadata_schema.json`
  - Versioned: `registry/v1/hatch_all_pkg_metadata_schema.json`

## Schema Details

### Package Schema

The Package Schema (`hatch_pkg_metadata_schema.json`) defines the structure for individual package metadata files and includes:

- Basic package identification (name, version, description)
- Author and contributor information
- Package dependencies (both Hatch packages and Python dependencies)
- Compatibility requirements
- Entry points and tools
- Citation information

### Registry Schema

The Registry Schema (`hatch_all_pkg_metadata_schema.json`) defines the structure for the central package registry and includes:

- Repository listings
- Package versioning and dependency tracking
- Artifact references and verification data
- Repository-wide statistics
- Change tracking between versions

## Using These Schemas

### Distribution Method

These schemas are distributed through:

1. **GitHub Releases** - Each version is packaged as a zip file attached to a release
2. **GitHub Pages** - Provides a "latest" pointer that redirects to the most recent version
3. **Raw GitHub Content** - Direct access to schema files in the repository

### URL Format

```
# For the latest version info (JSON format):
https://crackingshells.github.io/Hatch-Schemas/latest.json

# For direct download of the latest schema package:
https://crackingshells.github.io/Hatch-Schemas/ (redirects to latest release)

# For a specific version package:
https://github.com/crackingshells/Hatch-Schemas/releases/download/schemas-package-v1/schemas-package-v1.zip
https://github.com/crackingshells/Hatch-Schemas/releases/download/schemas-registry-v1/schemas-registry-v1.zip

# For direct access to schema files:
https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1/hatch_pkg_metadata_schema.json
https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/registry/v1/hatch_all_pkg_metadata_schema.json
```

### Referencing in Your JSON Files

You can reference these schemas in your JSON files using the `$schema` property:

```json
{
  "$schema": "https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1/hatch_pkg_metadata_schema.json",
  "name": "my_package",
  "version": "1.0.0",
  ...
}
```

### Programmatic Usage

#### Basic Validation

To validate against these schemas programmatically:

```python
import requests
import jsonschema

# Fetch the schema
schema_url = "https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1/hatch_pkg_metadata_schema.json"
schema = requests.get(schema_url).json()

# Your package data
package_data = {
    "name": "my_package",
    "version": "1.0.0",
    # ...other required fields
}

# Validate
jsonschema.validate(package_data, schema)
```

#### Automatic Schema Updates

We provide a helper utility (`schema_updater.py` in the examples directory) that manages schema caching and updates:

```python
from examples.schema_updater import load_schema, configure_logger
import logging

# Optional: Configure logging
configure_logger(level=logging.INFO)

# Load the latest schema (automatically downloads if needed)
package_schema = load_schema("package")
registry_schema = load_schema("registry")

# Use the schemas
import jsonschema
jsonschema.validate(my_package_data, package_schema)
```

## Schema Versioning

New schema versions are published automatically when changes to versioned schema folders (e.g., `package/v1/`, `registry/v1/`) are merged to `main`. The workflow:

1. Detects which versions were modified
2. Creates GitHub Releases for each modified version
3. Updates the "latest" pointer to the highest version number
4. Generates a `latest.json` file with metadata about the release

The `latest` alias always points to the most recently published schema version.

## License

See the [LICENSE](LICENSE) file for details.
