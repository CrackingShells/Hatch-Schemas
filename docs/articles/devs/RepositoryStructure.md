# Repository Structure

This article is about:
- Organization of files and directories in the Hatch Schemas repository
- Purpose and contents of each major directory
- Relationship between schemas, documentation, and examples

You will learn about:
- How the repository is organized
- Where to find specific types of files
- How schemas are versioned and distributed

Understanding the repository structure helps you navigate the codebase and contribute effectively.

## Directory Overview

```
Hatch-Schemas/
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       ├── schema-deployment.yml
│       ├── schema-validation.yml
│       └── manual-schema-test.yml
├── docs/                       # Documentation
│   └── articles/              # Structured documentation
│       ├── users/             # User-facing documentation
│       ├── devs/              # Developer documentation
│       └── appendices/        # Supporting information
├── examples/                   # Example scripts and utilities
│   └── schema_updater.py      # Schema loading utility
├── package/                    # Package schema versions
│   ├── v1/                    # Legacy version
│   ├── v1.1.0/               # Previous version
│   └── v1.2.0/               # Current version
│       └── hatch_pkg_metadata_schema.json
├── registry/                   # Registry schema versions
│   ├── v1/                    # Legacy version
│   ├── v1.1.0/               # Previous version
│   └── v1.2.0/               # Current version
│       └── hatch_all_pkg_metadata_schema.json
├── LICENSE                     # Project license
└── README.md                  # Project overview
```

## Schema Organization

### Package Schemas

Located in `package/` directory:

- **Current Version**: `package/v1.2.0/hatch_pkg_metadata_schema.json`
- **Previous Versions**: Maintained for backward compatibility
- **Deprecated Versions**: Marked but kept for reference

### Registry Schemas

Located in `registry/` directory:

- **Current Version**: `registry/v1.2.0/hatch_all_pkg_metadata_schema.json`
- **Previous Versions**: Maintained for backward compatibility
- **Deprecated Versions**: Marked but kept for reference

## Documentation Structure

The `docs/` directory follows a standardized structure:

### User Documentation (`docs/articles/users/`)

- **Getting Started**: Introduction and quick start guides
- **Schema Usage**: Access, validation, and programmatic usage
- **Schema References**: Detailed field documentation for each schema type

### Developer Documentation (`docs/articles/devs/`)

- **Contributing**: Guidelines for contributing to the project
- **Development Setup**: Environment setup and testing procedures
- **Architecture**: Repository structure and design decisions

### Appendices (`docs/articles/appendices/`)

- **Glossary**: Definitions of key terms and concepts
- **Reference Materials**: Supporting documentation

## CI/CD Infrastructure

### GitHub Actions (`.github/workflows/`)

- **schema-deployment.yml**: Automated release deployment
- **schema-validation.yml**: Schema validation and testing
- **manual-schema-test.yml**: Manual testing workflows

### Release Process

1. **Schema Changes**: Modifications to schema files trigger validation
2. **Automated Testing**: All schemas are validated against test data
3. **Release Creation**: Successful changes create GitHub releases
4. **Tag Format**: `schemas-{type}-{version}` (e.g., `schemas-package-v1.2.0`)

## Examples and Utilities

### Schema Updater (`examples/schema_updater.py`)

Provides programmatic access to schemas:

- **Schema Loading**: Automatic download and caching
- **Version Management**: Support for specific version requests
- **API Integration**: GitHub API integration for release discovery

## Design Patterns

### Versioning Strategy

- **Semantic Versioning**: Major.minor.patch format
- **Backward Compatibility**: Previous versions maintained
- **Deprecation Path**: Clear migration guidelines

### Distribution Method

- **GitHub Releases**: Primary distribution channel
- **Direct Access**: Raw file access via GitHub
- **API Discovery**: Programmatic version detection

## File Naming Conventions

- **Schema Files**: Descriptive names with clear purpose
- **Version Directories**: Semantic version format (v1.2.0)
- **Documentation**: Clear, hierarchical organization

## See Also

- [Contributing Guidelines](Contributing.md)
- [Development Setup](DevelopmentSetup.md)
- [Schema Versioning](SchemaVersioning.md)