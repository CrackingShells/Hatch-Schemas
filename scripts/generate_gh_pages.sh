#!/bin/bash
# generate_gh_pages.sh
#
# This script generates GitHub Pages content with latest schema information
#
# Usage: ./generate_gh_pages.sh [output_dir] [highest_pkg_version] [highest_registry_version] [repo]
#
# Example:
# ./generate_gh_pages.sh ./gh-pages-content v1 v1 "username/repo-name"

set -eo pipefail

# Get arguments
OUTPUT_DIR="${1:-./gh-pages-content}"
HIGHEST_PKG_VERSION="${2}"
HIGHEST_REGISTRY_VERSION="${3}"
REPO="${4:-$GITHUB_REPOSITORY}"

# Define schema types and their configurations
declare -A SCHEMA_CONFIGS=(
  ["package"]="hatch_pkg_metadata_schema.json"
  ["registry"]="hatch_all_pkg_metadata_schema.json"
)

declare -A HIGHEST_VERSIONS=(
  ["package"]="$HIGHEST_PKG_VERSION"
  ["registry"]="$HIGHEST_REGISTRY_VERSION"
)

echo "Generating GitHub Pages content in $OUTPUT_DIR"
echo "Highest package version: $HIGHEST_PKG_VERSION"
echo "Highest registry version: $HIGHEST_REGISTRY_VERSION"
echo "Repository: $REPO"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to generate HTML schema links section
generate_schema_section() {
  local schema_type=$1
  local version=${HIGHEST_VERSIONS[$schema_type]}
  local file_name=${SCHEMA_CONFIGS[$schema_type]}
  
  if [[ -z "$version" ]]; then
    return
  fi
  
  cat << EOS
        <h2>${schema_type^} Schemas</h2>
        <div class="schema-link">
          <strong>Latest version:</strong> ${version}
          <br>
          <a href="https://github.com/$REPO/releases/tag/schemas-${schema_type}-${version}">Release page</a> |
          <a href="https://github.com/$REPO/releases/download/schemas-${schema_type}-${version}/schemas-${schema_type}-${version}.zip">Download ZIP</a> |
          <a href="https://raw.githubusercontent.com/$REPO/main/${schema_type}/${version}/${file_name}">View JSON</a>
        </div>
EOS
}

# Create index.html file
cat > "$OUTPUT_DIR/index.html" << EOF
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Hatch Schemas</title>
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #24292e;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
      }
      h1 { color: #2188ff; }
      a { color: #0366d6; text-decoration: none; }
      a:hover { text-decoration: underline; }
      .container { margin-top: 40px; }
      .schema-link { margin-bottom: 10px; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Hatch Schemas</h1>
      <p>This page provides access to the latest schema versions:</p>
      
      <div class="schema-versions">
$(generate_schema_section "package")
        
$(generate_schema_section "registry")      </div>
    </div>
  </body>
</html>
EOF

# Function to generate JSON object for a schema type
generate_json_section() {
  local schema_type=$1
  local version=${HIGHEST_VERSIONS[$schema_type]}
  local file_name=${SCHEMA_CONFIGS[$schema_type]}
  
  if [[ -z "$version" ]]; then
    return
  fi
  
  cat << EOS
  "${schema_type}": {
    "version": "${version}",
    "release_url": "https://github.com/${REPO}/releases/tag/schemas-${schema_type}-${version}",
    "download_url": "https://github.com/${REPO}/releases/download/schemas-${schema_type}-${version}/schemas-${schema_type}-${version}.zip",
    "schema_url": "https://raw.githubusercontent.com/${REPO}/main/${schema_type}/${version}/${file_name}"
  }
EOS
}

# Create latest.json file with version information
cat > "$OUTPUT_DIR/latest.json" << EOF
{
  "latest_package_version": "${HIGHEST_PKG_VERSION}",
  "latest_registry_version": "${HIGHEST_REGISTRY_VERSION}",
$(generate_json_section "package"),
$(generate_json_section "registry"),
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

echo "GitHub Pages content generated successfully in $OUTPUT_DIR"