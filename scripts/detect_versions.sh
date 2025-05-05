#!/bin/bash
# detect_versions.sh
#
# This script detects schema versions from a list of changed files
# It outputs version information for package and registry schemas separately
#
# Usage: ./detect_versions.sh [file1] [file2] ... [fileN]
#   Or pipe in file list: cat file_list.txt | ./detect_versions.sh

# Define schema types to process
SCHEMA_TYPES=("package" "registry")

# Initialize associative arrays for tracking versions
declare -A VERSIONS_ARRAY
declare -A HIGHEST_VERSION
declare -A VERSIONS_JSON

# Process files either from arguments or stdin
FILES=("$@")
if [ $# -eq 0 ]; then
  while read -r line; do
    FILES+=("$line")
  done
fi

echo "Processing ${#FILES[@]} changed files"

# Function to extract version from file path
extract_version() {
  local file=$1
  local schema_type=$2
  echo "$file" | grep -o "${schema_type}/v[0-9]\+\(\.[0-9]\+\)*" | cut -d'/' -f2
}

# Extract directory versions from changed files
for file in "${FILES[@]}"; do
  # Process each schema type
  for schema_type in "${SCHEMA_TYPES[@]}"; do
    if [[ $file == ${schema_type}/v* ]]; then
      VERSION=$(extract_version "$file" "$schema_type")
      if [[ ! -z "$VERSION" ]]; then
        VERSIONS_ARRAY[${schema_type}]+=" $VERSION"
        echo "Found ${schema_type} schema version: $VERSION"
      fi
    fi
  done
done

# Process each schema type to get unique versions and determine highest version
for schema_type in "${SCHEMA_TYPES[@]}"; do
  # Get unique versions
  if [[ ! -z "${VERSIONS_ARRAY[${schema_type}]}" ]]; then
    UNIQUE_VERSIONS=($(echo "${VERSIONS_ARRAY[${schema_type}]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))
    echo "${schema_type^} schema versions: ${UNIQUE_VERSIONS[*]}"
    
    # Find highest version
    HIGHEST_VERSION[${schema_type}]=$(echo "${UNIQUE_VERSIONS[*]}" | tr ' ' '\n' | sort -Vr | head -n1)
    # Create JSON array
    VERSIONS_JSON[${schema_type}]="[\"$(echo "${UNIQUE_VERSIONS[@]}" | sed 's/ /\", \"/g')\"]"
  else
    # No schema changes detected for this type
    HIGHEST_VERSION[${schema_type}]=""
    VERSIONS_JSON[${schema_type}]="[]"
  fi
done

# Output results in GitHub Actions compatible format (legacy format)
echo "::set-output name=pkg_versions::${VERSIONS_JSON[package]}"
echo "::set-output name=registry_versions::${VERSIONS_JSON[registry]}"
echo "::set-output name=highest_pkg_version::${HIGHEST_VERSION[package]}"
echo "::set-output name=highest_registry_version::${HIGHEST_VERSION[registry]}"

# Also output in the modern GitHub Actions compatible format
{
  echo "pkg_versions=${VERSIONS_JSON[package]}" >> "$GITHUB_OUTPUT" 
  echo "registry_versions=${VERSIONS_JSON[registry]}" >> "$GITHUB_OUTPUT"
  echo "highest_pkg_version=${HIGHEST_VERSION[package]}" >> "$GITHUB_OUTPUT"
  echo "highest_registry_version=${HIGHEST_VERSION[registry]}" >> "$GITHUB_OUTPUT"
} 2>/dev/null || true  # Ignore errors if GITHUB_OUTPUT isn't set