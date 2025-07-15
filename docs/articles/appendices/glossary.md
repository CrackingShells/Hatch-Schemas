# Glossary

This article is about:
- Key terms and concepts used in Hatch Schemas documentation
- Definitions for technical terminology

You will learn about:
- The meaning of important terms in the Hatch ecosystem
- Context for technical concepts used throughout the documentation

## Core Concepts

**Hatch Schema**
: A JSON schema that defines the structure and validation rules for metadata in the CrackingShells package ecosystem.

**JSON Schema**
: A vocabulary that allows you to annotate and validate JSON documents. Uses JSON format to describe the structure, data types, and validation rules.

**Package Metadata**
: Structured information about a package including name, version, dependencies, author information, and other descriptive data.

**Registry**
: The central catalog of all available packages in the Hatch ecosystem, maintained as a searchable database.

## Schema Types

**Package Schema**
: Schema for validating individual package metadata files (`hatch_pkg_metadata_schema.json`).

**Registry Schema**
: Schema for validating the central package registry structure (`hatch_all_pkg_metadata_schema.json`).

## Validation Terms

**Schema Validation**
: The process of checking that a JSON document conforms to the rules defined in a JSON schema.

**Version Constraint**
: A specification defining which versions of a dependency are acceptable (e.g., `>=1.0.0`, `^2.1.0`).

**Entry Point**
: The main executable file or script that serves as the primary interface for a package.

## Technical Terms

**URI**
: Uniform Resource Identifier - a string that identifies a resource, typically a URL.

**Semantic Versioning**
: A versioning scheme using three numbers (major.minor.patch) to indicate backwards compatibility.

**Dependency**
: An external package or component that a package requires to function properly.

## Ecosystem Terms

**CrackingShells**
: The GitHub organization that maintains the Hatch package ecosystem.

**Hatchling**
: The build system and package manager for the Hatch ecosystem.

**Package Manager**
: A tool for installing, updating, and managing software packages (e.g., pip, apt, npm).