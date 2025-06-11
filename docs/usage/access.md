# Schema Access Guide

This guide explains how to access and use the Hatch Schemas in your projects.

## Distribution Methods

Hatch Schemas are distributed through multiple channels:

1. **GitHub Repository** - Direct access to schema files via raw.githubusercontent.com
2. **GitHub Releases** - Versioned releases with metadata and direct downloads
3. **GitHub API** - Programmatic discovery of latest versions and releases

## Accessing Schemas

### Manual Discovery

You can visit the release page: https://github.com/CrackingShells/Hatch-Schemas/releases

### Release Downloads

Download schema files from specific GitHub releases:

```bash
# Download schema files from specific releases
https://github.com/crackingshells/Hatch-Schemas/releases/download/schemas-package-v1.2.0/hatch_pkg_metadata_schema.json
https://github.com/crackingshells/Hatch-Schemas/releases/download/schemas-registry-v1.2.0/hatch_all_pkg_metadata_schema.json
```

### Direct Schema Access

Access schema files directly from the GitHub repository:

```bash
# Direct access to schema files (always current from main branch)
https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1.2.0/hatch_pkg_metadata_schema.json
https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/registry/v1.2.0/hatch_all_pkg_metadata_schema.json
```


## Using Schemas in Your Project

### Referencing in JSON Files

You can reference these schemas in your JSON files using the `$schema` property:

```json
{
  "$schema": "https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1.2.0/hatch_pkg_metadata_schema.json",
  "name": "my_package",
  "version": "1.0.0",
  "description": "My awesome package",
  "tags": ["example"],
  "author": {"name": "John Doe"},
  "license": {"name": "MIT"},
  "entry_point": "server.py"
}
```

This reference:
1. Provides editors with schema information for autocompletion and validation
2. Documents which schema version the file adheres to
3. Creates a clear contract for validation tools

### Local Cache Management

Consider implementing local caching of schemas. The `examples/schema_updater.py` utility provides this functionality:

```python
from examples.schema_updater import configure_cache, update_schemas

# Configure local cache location (optional)
configure_cache(cache_dir="./schemas_cache")

# Update local schema cache
update_schemas()
```

## See Also

- [Schema Validation](validation.md)
- [Programmatic Usage](programmatic.md)
