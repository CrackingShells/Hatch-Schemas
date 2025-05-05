#!/bin/bash
# create_releases.sh
#
# This script creates GitHub releases for both package and registry schemas
#
# Usage: ./create_releases.sh [artifacts_dir] [pkg_versions_json] [registry_versions_json]
#
# Environment variables required:
# - GITHUB_TOKEN: GitHub token for authentication

set -eo pipefail

# Get arguments
ARTIFACTS_DIR="${1:-./artifacts}"
PKG_VERSIONS_JSON="${2:-[]}"
REGISTRY_VERSIONS_JSON="${3:-[]}"

# Define schema types and their configurations
declare -A VERSIONS_JSON=(
  ["package"]="$PKG_VERSIONS_JSON"
  ["registry"]="$REGISTRY_VERSIONS_JSON"
)

# Ensure GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI not found. Please install it first."
    exit 1
fi

# Check if GITHUB_TOKEN is set
if [[ -z "$GITHUB_TOKEN" ]]; then
    echo "Warning: GITHUB_TOKEN environment variable not set."
    echo "You may need to authenticate with GitHub CLI manually."
fi

# Create releases for a specific schema type
create_releases() {
    local schema_type=$1
    local versions_json=${VERSIONS_JSON[$schema_type]}
    
    # Convert JSON array to bash array
    local versions
    versions=$(echo "$versions_json" | jq -r '.[]')
    
    for VERSION in $versions; do
        echo "Creating release for ${schema_type} version: $VERSION"
        
        # Get release asset path
        ASSET_PATH="$ARTIFACTS_DIR/${schema_type}/schemas-${schema_type}-$VERSION.zip"
        
        if [[ ! -f "$ASSET_PATH" ]]; then
            echo "Warning: Asset file not found at $ASSET_PATH"
            continue
        fi
        
        # Create release notes
        RELEASE_NOTES="${schema_type^} schema version $VERSION released on $(date -u +"%Y-%m-%d")"
        
        # Create a GitHub release using GitHub CLI
        gh release create "schemas-${schema_type}-$VERSION" \
            --title "${schema_type^} Schema Release $VERSION" \
            --notes "$RELEASE_NOTES" \
            "$ASSET_PATH" || echo "Failed to create release for ${schema_type} version $VERSION"
            
        echo "Release created for ${schema_type} version $VERSION"
    done
}

# Process each schema type
for schema_type in "${!VERSIONS_JSON[@]}"; do
    if [[ "${VERSIONS_JSON[$schema_type]}" != "[]" ]]; then
        create_releases "$schema_type"
        echo "All ${schema_type} releases created successfully"
    else
        echo "No ${schema_type} releases to create"
    fi
done

echo "Release creation complete"