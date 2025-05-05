#!/bin/bash
# validate_schemas.sh
#
# This script validates the schema files for both package and registry schemas
#
# Usage: ./validate_schemas.sh [pkg_version] [registry_version]
#   Where pkg_version and registry_version are optional
#   If not provided, the script will try to find them

# Set up environment
set -eo pipefail

# Define schema types and their configurations
declare -A SCHEMA_CONFIGS=(
  ["package"]="hatch_pkg_metadata_schema.json"
  ["registry"]="hatch_all_pkg_metadata_schema.json"
)

# Get versions from arguments or environment variables
VERSION_ARGS=("$@")
PKG_VERSION="${VERSION_ARGS[0]:-$HIGHEST_PKG_VERSION}"
REGISTRY_VERSION="${VERSION_ARGS[1]:-$HIGHEST_REGISTRY_VERSION}"

# Store versions in associative array for easier iteration
declare -A VERSIONS=(
  ["package"]="$PKG_VERSION"
  ["registry"]="$REGISTRY_VERSION"
)

# Check if ajv is available, install if needed
if ! command -v ajv &> /dev/null; then
    echo "AJV not found, installing..."
    npm install -g ajv-cli ajv-formats
fi

VALID=true

# Function to validate a schema
validate_schema() {
    local schema_type=$1
    local version=$2
    local file_name=${SCHEMA_CONFIGS[$schema_type]}
    
    echo "Validating ${schema_type} schema version: $version"
    local schema_path="${schema_type}/${version}/${file_name}"
    
    if [[ -f "$schema_path" ]]; then
        echo "${schema_type^} schema file found: $schema_path"
        if ajv compile -s "$schema_path" --spec=draft7 -c ajv-formats; then
            echo "✓ ${schema_type^} schema validation successful"
            return 0
        else
            echo "✗ ${schema_type^} schema validation failed"
            return 1
        fi
    else
        echo "Warning: ${schema_type^} schema file not found at $schema_path"
        return 0  # Not finding a file isn't a validation error
    fi
}

# Validate each schema type
for schema_type in "${!SCHEMA_CONFIGS[@]}"; do
    version="${VERSIONS[$schema_type]}"
    if [[ ! -z "$version" ]]; then
        if ! validate_schema "$schema_type" "$version"; then
            VALID=false
        fi
    else
        echo "No ${schema_type} schema version provided for validation"
    fi
done

# Final validation status
if $VALID; then
    echo "All schema validations passed"
    exit 0
else
    echo "One or more schema validations failed"
    exit 1
fi