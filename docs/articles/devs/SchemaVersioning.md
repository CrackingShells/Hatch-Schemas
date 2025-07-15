# Schema Versioning

This article is about:
- Versioning strategy for Hatch Schemas
- Release processes and compatibility management
- Migration guidelines for schema updates

You will learn about:
- How schema versions are managed
- How to handle schema migrations
- Release automation and distribution processes

Proper schema versioning ensures stability and provides clear upgrade paths for the Hatch ecosystem.

## Versioning Strategy

### Semantic Versioning

Hatch Schemas follow semantic versioning (semver) principles:

- **Major Version** (X.0.0): Breaking changes that require migration
- **Minor Version** (0.X.0): New features that maintain backward compatibility
- **Patch Version** (0.0.X): Bug fixes and clarifications

### Version Format

Schema versions use the format: `vX.Y.Z`

Examples:
- `v1.2.0` - Current package and registry schema version
- `v1.1.0` - Previous minor version
- `v1.0.0` - Initial major version

## Release Process

### Automated Releases

Schema releases are automated through GitHub Actions:

1. **Change Detection**: Commits to versioned schema folders trigger releases
2. **Validation**: All schemas are validated before release
3. **Tag Creation**: Releases are tagged with format `schemas-{type}-{version}`
4. **Asset Publication**: Schema files are attached to GitHub releases

### Release Tags

- **Package Schema**: `schemas-package-v1.2.0`
- **Registry Schema**: `schemas-registry-v1.2.0`

### Distribution Channels

Released schemas are available through:

1. **GitHub Releases**: Direct file downloads
2. **Raw URLs**: Direct access via raw.githubusercontent.com
3. **API Discovery**: Programmatic version detection

## Compatibility Management

### Backward Compatibility

- **Minor Versions**: Must be backward compatible
- **Optional Fields**: New fields should be optional when possible
- **Deprecation**: Clear deprecation warnings before removal

### Breaking Changes

When breaking changes are necessary:

1. **Major Version Bump**: Increment major version number
2. **Migration Guide**: Provide clear migration instructions
3. **Legacy Support**: Maintain previous version for transition period

### Deprecation Process

1. **Mark as Deprecated**: Add deprecation notices
2. **Provide Alternatives**: Document replacement approaches
3. **Sunset Timeline**: Communicate removal schedule
4. **Remove After Grace Period**: Remove after reasonable transition time

## Migration Guidelines

### Schema Updates

When migrating to a new schema version:

1. **Review Changes**: Check release notes for breaking changes
2. **Update References**: Update `$schema` references in JSON files
3. **Validate Data**: Ensure existing data validates against new schema
4. **Test Applications**: Verify application compatibility

### Example Migration

Migrating from v1.1.0 to v1.2.0:

```json
// Old schema reference
{
  "$schema": "https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1.1.0/hatch_pkg_metadata_schema.json",
  // ... package data
}

// New schema reference
{
  "$schema": "https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1.2.0/hatch_pkg_metadata_schema.json",
  // ... package data (may need updates for new requirements)
}
```

## Version Discovery

### Programmatic Discovery

Use the GitHub API to discover latest versions:

```python
import requests

def get_latest_schema_version(schema_type):
    """Get the latest version for a schema type."""
    api_url = "https://api.github.com/repos/crackingshells/Hatch-Schemas/releases"
    response = requests.get(api_url)
    releases = response.json()
    
    for release in releases:
        tag = release['tag_name']
        if tag.startswith(f'schemas-{schema_type}-'):
            return tag.replace(f'schemas-{schema_type}-', '')
    
    return None

# Get latest package schema version
latest_package_version = get_latest_schema_version("package")
print(f"Latest package schema: {latest_package_version}")
```

### Manual Discovery

Visit the releases page to see all available versions:
https://github.com/CrackingShells/Hatch-Schemas/releases

## Best Practices

### For Schema Maintainers

- **Test Thoroughly**: Validate against real-world data
- **Document Changes**: Provide clear release notes
- **Gradual Rollouts**: Consider phased releases for major changes
- **Community Input**: Gather feedback before breaking changes

### For Schema Consumers

- **Pin Versions**: Use specific versions in production
- **Monitor Releases**: Stay informed about new versions
- **Test Updates**: Validate compatibility before upgrading
- **Provide Feedback**: Report issues and suggestions

## See Also

- [Contributing Guidelines](Contributing.md)
- [Development Setup](DevelopmentSetup.md)
- [Repository Structure](RepositoryStructure.md)