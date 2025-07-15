# Getting Started with Hatch Schemas

This article is about:
- Introduction to Hatch Schemas
- Basic concepts and usage patterns
- First steps for new users

You will learn about:
- What Hatch Schemas are and their purpose
- How to access and use schemas in your projects
- Basic validation workflows

Hatch Schemas provide standardized JSON schemas for validating metadata in the CrackingShells package ecosystem.

## What are Hatch Schemas?

Hatch Schemas define the structure and validation rules for two key components:

- **Package Schema**: Validates individual package metadata files
- **Registry Schema**: Validates the central package registry

## Quick Start

### 1. Choose Your Schema

Determine which schema you need:
- Use the **Package Schema** when creating or validating individual package metadata
- Use the **Registry Schema** when working with the central package registry

### 2. Access the Schema

The simplest way to access schemas is through direct URLs:

```bash
# Package Schema (latest)
https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1.2.0/hatch_pkg_metadata_schema.json

# Registry Schema (latest)
https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/registry/v1.2.0/hatch_all_pkg_metadata_schema.json
```

### 3. Reference in Your JSON

Add a `$schema` reference to your JSON files:

```json
{
  "$schema": "https://raw.githubusercontent.com/crackingshells/Hatch-Schemas/main/package/v1.2.0/hatch_pkg_metadata_schema.json",
  "package_schema_version": "1.2.0",
  "name": "my_package",
  "version": "1.0.0",
  "description": "My awesome package",
  "tags": ["example"],
  "author": {"name": "John Doe"},
  "license": {"name": "MIT"},
  "entry_point": "server.py"
}
```

## Next Steps

- Learn more about [Schema Access](SchemaAccess.md) methods
- Understand [Schema Validation](SchemaValidation.md) techniques
- Explore [Programmatic Usage](ProgrammaticUsage.md) patterns
- Review detailed schema documentation for [Package Schema](PackageSchema/Overview.md) or [Registry Schema](RegistrySchema/Overview.md)

## Need Help?

Check the [Glossary](../appendices/glossary.md) for definitions of key terms.