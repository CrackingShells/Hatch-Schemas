#!/bin/bash
# package_schemas.sh
#
# This script packages schema files for release, creating separate artifacts for
# both package and registry schemas
#
# Usage: ./package_schemas.sh [artifacts_dir] [pkg_versions_json] [registry_versions_json] [commit_sha]
#
# Example:
# ./package_schemas.sh ./artifacts '["v1","v2"]' '["v1"]' "abc123"

set -eo pipefail

# Get arguments
ARTIFACTS_DIR="${1:-./artifacts}"
PKG_VERSIONS_JSON="${2:-[]}"
REGISTRY_VERSIONS_JSON="${3:-[]}"
COMMIT_SHA="${4:-$(git rev-parse HEAD)}"

# Define schema types and their configurations
declare -A VERSIONS_JSON=(
  ["package"]="$PKG_VERSIONS_JSON"
  ["registry"]="$REGISTRY_VERSIONS_JSON"
)

# Create artifacts directory if it doesn't exist
mkdir -p "$ARTIFACTS_DIR"

echo "Packaging schemas to $ARTIFACTS_DIR"
echo "Package versions: $PKG_VERSIONS_JSON"
echo "Registry versions: $REGISTRY_VERSIONS_JSON"

# Process versions for a specific schema type
process_versions() {
    local schema_type=$1
    local versions_json=${VERSIONS_JSON[$schema_type]}
    
    # Convert JSON array to bash array
    local versions
    versions=$(echo "$versions_json" | jq -r '.[]')
    
    for VERSION in $versions; do
        echo "Processing ${schema_type} version: $VERSION"
        mkdir -p "$ARTIFACTS_DIR/${schema_type}/$VERSION"
        
        # Copy schemas to versioned directory
        cp -r "${schema_type}/$VERSION" "$ARTIFACTS_DIR/${schema_type}/"
        
        # Create metadata files for each version
        echo "{
            \"version\": \"$VERSION\",
            \"build_date\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
            \"commit\": \"$COMMIT_SHA\"
        }" > "$ARTIFACTS_DIR/${schema_type}/$VERSION/metadata.json"
        
        # Create version-specific zip for release
        echo "Creating zip archive for ${schema_type} version $VERSION"
        (cd "$ARTIFACTS_DIR/${schema_type}" && zip -r "schemas-${schema_type}-$VERSION.zip" "$VERSION")
        
        echo "${schema_type^} version $VERSION processed successfully"
    done
}

# Process each schema type
for schema_type in "${!VERSIONS_JSON[@]}"; do
    if [[ "${VERSIONS_JSON[$schema_type]}" != "[]" ]]; then
        process_versions "$schema_type"
        echo "All ${schema_type} versions processed successfully"
    else
        echo "No ${schema_type} versions to process"
    fi
done

echo "Schema packaging complete. Artifacts are available in $ARTIFACTS_DIR"