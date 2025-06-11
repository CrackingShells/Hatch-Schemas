# Hatch-Schemas

JSON schemas for the CrackingShells organization package ecosystem.

## Available Schemas

This repository contains JSON schemas for validating Hatch metadata:

- **Package Schema**: Validates individual package metadata. [Learn More](docs/package/overview.md)
  - Latest: `package/v1.2.0/hatch_pkg_metadata_schema.json`
  - Versioned: `package/v1.2.0/hatch_pkg_metadata_schema.json`
  - Deprecated: `package/v1.0/hatch_pkg_metadata_schema.json`, `package/v1.1.0/hatch_pkg_metadata_schema.json`

- **Registry Schema**: Validates the central package registry. [Learn More](docs/registry/overview.md)
  - Latest: `registry/v1.2.0/hatch_all_pkg_metadata_schema.json`
  - Versioned: `registry/v1.2.0/hatch_all_pkg_metadata_schema.json`
  - Deprecated: `registry/v1.0/hatch_all_pkg_metadata_schema.json`, `registry/v1.1.0/hatch_all_pkg_metadata_schema.json`

## Documentation

For detailed information on schemas, usage guides, and examples, please refer to our [Documentation](docs/index.md):

- [Schema Details](docs/index.md#overview)
- [Package Schema Reference](docs/package/overview.md)
- [Registry Schema Reference](docs/registry/overview.md)
- [Usage Guides](docs/usage/index.md)
- [Schema Versioning](docs/versions.md)
- [Migration Guide](docs/migration.md)

## Schema Access

### Distribution Method

These schemas are distributed through **GitHub Releases** with direct file attachments, providing multiple access patterns:

1. **Direct Raw Access** - Immediate access to schema files via raw.githubusercontent.com
2. **GitHub Releases** - Versioned releases with metadata and direct downloads
3. **GitHub API** - Programmatic discovery of latest versions and releases

See the [Schema Access Guide](docs/usage/access.md) for detailed instructions.

### Programmatic Usage

A simple schema loading example:

```python
from examples.schema_updater import load_schema

# Load the latest schemas 
package_schema = load_schema("package")      # Latest package schema
registry_schema = load_schema("registry")    # Latest registry schema

# Load specific version
package_v1 = load_schema("package", "v1.2.0")  # Specific version
```

For more detailed examples, including manual schema retrieval, validation, caching, and advanced use cases, see the [Programmatic Usage Guide](docs/usage/programmatic.md).

## Schema Versioning

New schema versions are published automatically when changes to versioned schema folders are merged to `main`. Each release is tagged with the format `schemas-{type}-{version}` (e.g., `schemas-package-v1.2.0`).

## Contribution Guidelines

To propose revisions to the schemas, please open an issue in this repository describing the proposed changes.

## License

See the [LICENSE](LICENSE) file for details.
