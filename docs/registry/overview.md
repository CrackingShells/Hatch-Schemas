# Registry Schema Documentation

## Overview

The Registry Schema (`hatch_all_pkg_metadata_schema.json`) defines the structure for the central package registry in the Hatch ecosystem. This schema is used to maintain a comprehensive, searchable catalog of all available packages across CrackingShells repositories.

> [!Note]
> The registry is being maintained internally. It is modified by specific functions, and updated during package submission process. In principle, there **MUST NOT** be any manual modification of the registry to add a package. Although, highly discouraged, there **MAY** be manual modification by core members of the organization in case of errors.

## Current Version

The current version of the Registry Schema is **v1.2.0**.

## Schema Structure

The Registry Schema includes the following major sections:

- **Registry Metadata**: Schema version, last updated timestamp, and global statistics
- **Repositories**: List of repositories with their metadata and packages
- **Packages**: Package information including name, description, tags, and versions
- **Version Information**: Details about each version of a package, including author, release location, and verification status

For detailed field-by-field documentation including types, formats, and examples, see the [Registry Schema Field Reference](fields.md).
- **verification**: Verification status and metadata
- **dependency_changes**: Changes to dependencies since the base version
- **compatibility_changes**: Changes to compatibility requirements

## Example

```json
{
  "registry_schema_version": "1.2.0",
  "last_updated": "2024-06-01T12:00:00Z",
  "repositories": [
    {
      "name": "Hatch-Dev",
      "url": "https://github.com/crackingshells/Hatch-Dev",
      "last_indexed": "2024-06-01T12:00:00Z",
      "packages": [
        {
          "name": "example_package",
          "description": "An example Hatch package",
          "tags": ["example", "demo"],
          "latest_version": "1.2.0",
          "versions": [
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
          ]
        }
      ]
    }
  ],
  "stats": {
    "total_packages": 1,
    "total_versions": 1
  }
}
```

## See Also

- [Package Schema](../package/overview.md)
- [Schema Validation Guide](../usage/validation.md)
