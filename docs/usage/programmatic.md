# Programmatic Usage Guide

This guide explains how to use Hatch schemas programmatically in your applications.

## Simple Schema Loading

For basic usage, you can use the provided example utility:

```python
from examples.schema_updater import load_schema, configure_logger
import logging

# Optional: Configure logging
configure_logger(level=logging.INFO)

# Load the latest schemas (automatically downloads if needed)
package_schema = load_schema("package")      # Latest package schema
registry_schema = load_schema("registry")    # Latest registry schema

# Load specific version
package_v1_2_0 = load_schema("package", "v1.2.0")  # Specific version
```

## Manual Schema Retrieval

For more control over schema retrieval, you can implement your own functions:

```python
import requests
import json

def get_latest_schema_info():
    """Get latest schema version information from GitHub API."""
    api_url = "https://api.github.com/repos/crackingshells/Hatch-Schemas/releases"
    response = requests.get(api_url)
    releases = response.json()
    
    # Find latest package and registry schema releases
    latest_schemas = {}
    for release in releases:
        tag = release['tag_name']
        if tag.startswith('schemas-package-'):
            if 'package' not in latest_schemas:
                version = tag.replace('schemas-package-', '')
                latest_schemas['package'] = {
                    'version': version,
                    'url': f"https://github.com/crackingshells/Hatch-Schemas/releases/download/schemas-package-{version}/hatch_pkg_metadata_schema.json"
                }
        elif tag.startswith('schemas-registry-'):
            if 'registry' not in latest_schemas:
                version = tag.replace('schemas-registry-', '')
                latest_schemas['registry'] = {
                    'version': version,
                    'url': f"https://github.com/crackingshells/Hatch-Schemas/releases/download/schemas-registry-{version}/hatch_all_pkg_metadata_schema.json"
                }
    
    return latest_schemas

def load_schema(schema_type, version=None):
    """Load a specific schema or the latest version."""
    if version is None:
        # Get latest version
        latest_info = get_latest_schema_info()
        schema_url = latest_info[schema_type]['url']
    else:
        # Use specific version from release
        if schema_type == 'package':
            schema_url = f"https://github.com/crackingshells/Hatch-Schemas/releases/download/schemas-package-{version}/hatch_pkg_metadata_schema.json"
        else:
            schema_url = f"https://github.com/crackingshells/Hatch-Schemas/releases/download/schemas-registry-{version}/hatch_all_pkg_metadata_schema.json"
    
    response = requests.get(schema_url)
    return response.json()
```

## Basic Validation

```python
import jsonschema

# Load schema
schema = load_schema("package")

# Your package data
package_data = {
    "package_schema_version": "1.2.0",
    "name": "my_package",
    "version": "1.0.0",
    "description": "My awesome package",
    "tags": ["example"],
    "author": {"name": "John Doe"},
    "license": {"name": "MIT"},
    "entry_point": "server.py"
}

# Validate
try:
    jsonschema.validate(package_data, schema)
    print("Package metadata is valid")
except jsonschema.ValidationError as e:
    print(f"Validation error: {e.message}")
```

## Advanced Use Cases

An, implementation example is also [available](../../examples/schema_updater.py)

### Schema Caching

For performance and offline availability, implement a schema caching mechanism:

```python
import os
import json
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "hatch-schemas"

def cache_schema(schema_type, version, schema_data):
    """Cache a schema locally."""
    # Ensure cache directory exists
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Write schema to cache
    cache_file = CACHE_DIR / f"{schema_type}-{version}.json"
    with open(cache_file, 'w') as f:
        json.dump(schema_data, f)
    
    return cache_file

def get_cached_schema(schema_type, version):
    """Retrieve a schema from the local cache."""
    cache_file = CACHE_DIR / f"{schema_type}-{version}.json"
    
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    return None

def load_schema_with_cache(schema_type, version=None):
    """Load schema with caching support."""
    if version is None:
        # Get latest version info
        latest_info = get_latest_schema_info()
        version = latest_info[schema_type]['version']
    
    # Try to load from cache
    cached_schema = get_cached_schema(schema_type, version)
    if cached_schema:
        return cached_schema
    
    # If not in cache, download and cache
    schema_data = load_schema(schema_type, version)
    if schema_data:
        cache_schema(schema_type, version, schema_data)
    
    return schema_data
```

## See Also

- [Schema Access Guide](access.md)
- [Schema Validation Guide](validation.md)
