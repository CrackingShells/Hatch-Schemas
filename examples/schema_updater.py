"""Schema retrieval and caching utility for Hatch schemas.

This module provides utilities for:
1. Discovering latest schema versions via GitHub API
2. Downloading schemas directly from GitHub releases
3. Caching schemas locally for offline use
4. Validating schema updates and version management
"""

import os
import json
import shutil
import logging
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any

# Configure logging
logger = logging.getLogger("schema_updater")
logger.setLevel(logging.INFO)

# Configuration
GITHUB_API_BASE = "https://api.github.com/repos/crackingshells/Hatch-Schemas"
GITHUB_RELEASES_BASE = "https://github.com/crackingshells/Hatch-Schemas/releases/download"
CACHE_DIR = Path.home() / ".crackingshells" / "schemas"
CACHE_INFO_FILE = CACHE_DIR / "schema_info.json"


def configure_logger(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """Configure the logger with custom settings.
    
    Args:
        level: The logging level (e.g., logging.DEBUG, logging.INFO).
        log_file (optional): Path to a log file. Defaults to None.
    """
    logger.setLevel(level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)


def get_latest_schema_info() -> Optional[Dict[str, Any]]:
    """Get latest schema version information from GitHub API.
    
    Returns:
        Dict containing latest schema information, or None if unavailable.
    """
    try:
        logger.debug(f"Requesting releases from {GITHUB_API_BASE}/releases")
        response = requests.get(f"{GITHUB_API_BASE}/releases", timeout=10)
        response.raise_for_status()
        releases = response.json()
        
        # Extract latest versions for each schema type
        latest_schemas = {
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }
        
        for release in releases:
            tag = release['tag_name']
            if tag.startswith('schemas-package-'):
                if 'latest_package_version' not in latest_schemas:
                    version = tag.replace('schemas-package-', '')
                    latest_schemas['latest_package_version'] = version
                    latest_schemas['package'] = {
                        'version': version,
                        'url': f"{GITHUB_RELEASES_BASE}/schemas-package-{version}/hatch_pkg_metadata_schema.json",
                        'release_url': release['html_url']
                    }
            elif tag.startswith('schemas-registry-'):
                if 'latest_registry_version' not in latest_schemas:
                    version = tag.replace('schemas-registry-', '')
                    latest_schemas['latest_registry_version'] = version
                    latest_schemas['registry'] = {
                        'version': version,
                        'url': f"{GITHUB_RELEASES_BASE}/schemas-registry-{version}/hatch_all_pkg_metadata_schema.json",
                        'release_url': release['html_url']
                    }
        
        logger.debug("Schema info retrieved successfully")
        return latest_schemas
    except requests.RequestException as e:
        logger.error(f"Error fetching schema info: {e}")
        return None


def get_cached_schema_info() -> Optional[Dict[str, Any]]:
    """Get information about the locally cached schema versions.
    
    Returns:
        Dict containing cached schema information, or None if unavailable.
    """
    if not CACHE_INFO_FILE.exists():
        logger.debug("No cached schema info found")
        return None
    
    try:
        logger.debug(f"Reading cached schema info from {CACHE_INFO_FILE}")
        with open(CACHE_INFO_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error reading cached schema info: {e}")
        return None


def download_schema_file(schema_type: str, schema_url: str) -> bool:
    """Download a schema file directly from the raw URL.
    
    Args:
        schema_type: Either "package" or "registry".
        schema_url: Direct URL to the schema JSON file.
        
    Returns:
        bool: True if download was successful, False otherwise.
    """
    try:
        # Create schema type directory
        schema_cache_dir = CACHE_DIR / schema_type
        schema_cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine filename based on schema type
        if schema_type == "package":
            filename = "hatch_pkg_metadata_schema.json"
        elif schema_type == "registry":
            filename = "hatch_all_pkg_metadata_schema.json"
        else:
            logger.error(f"Unknown schema type: {schema_type}")
            return False
        
        # Download the schema file
        logger.info(f"Downloading {schema_type} schema from {schema_url}")
        response = requests.get(schema_url, timeout=30)
        response.raise_for_status()
        
        # Save to cache
        schema_path = schema_cache_dir / filename
        with open(schema_path, "w") as f:
            json.dump(response.json(), f, indent=2)
        
        logger.debug(f"{schema_type.capitalize()} schema saved to {schema_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error downloading {schema_type} schema: {e}")
        return False


def update_cache_info(schema_info: Dict[str, Any]) -> bool:
    """Update the cached schema information.
    
    Args:
        schema_info: Dictionary containing schema information to cache.
        
    Returns:
        bool: True if update was successful, False otherwise.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        logger.debug(f"Writing updated schema info to {CACHE_INFO_FILE}")
        with open(CACHE_INFO_FILE, "w") as f:
            json.dump(schema_info, f, indent=2)
        return True
    except IOError as e:
        logger.error(f"Error writing cache info: {e}")
        return False


def check_and_update_schemas() -> bool:
    """Check if new schema versions are available and update if needed.
    
    Returns:
        bool: True if any schemas were updated, False otherwise.
    """
    # Get info about the latest available schemas
    latest_info = get_latest_schema_info()
    if not latest_info:
        logger.warning("Could not retrieve latest schema information. Using cached version if available.")
        return False
    
    # Get info about the cached schemas
    cached_info = get_cached_schema_info()
    
    updated = False
    
    # Check and update each schema type separately
    for schema_type in ["package", "registry"]:
        # Skip if this schema type is not in the latest info
        if schema_type not in latest_info:
            logger.debug(f"No {schema_type} schema information in the latest info")
            continue
            
        latest_version_key = f"latest_{schema_type}_version"
        latest_version = latest_info.get(latest_version_key)
        
        # Skip if no latest version is defined
        if not latest_version:
            logger.debug(f"No latest version for {schema_type} schema")
            continue
        
        needs_update = True
        
        # Check if we have this version cached already
        if cached_info and schema_type in cached_info:
            cached_version_key = f"latest_{schema_type}_version"
            cached_version = cached_info.get(cached_version_key)
            
            if cached_version == latest_version:
                # Check if the cached version is up to date
                cached_updated = datetime.fromisoformat(cached_info.get("updated_at", "1970-01-01T00:00:00Z").replace("Z", "+00:00"))
                latest_updated = datetime.fromisoformat(latest_info.get("updated_at", "1970-01-01T00:00:00Z").replace("Z", "+00:00"))
                
                if cached_updated >= latest_updated:
                    logger.info(f"{schema_type.capitalize()} schema is up to date (version {latest_version}).")
                    needs_update = False
        
        # Update schema if needed
        if needs_update:
            schema_url = latest_info.get(schema_type, {}).get("url")
            if schema_url:
                logger.info(f"New {schema_type} schema version available: {latest_version}")
                if download_schema_file(schema_type, schema_url):
                    updated = True
                    logger.info(f"{schema_type.capitalize()} schema updated successfully.")
                else:
                    logger.error(f"{schema_type.capitalize()} schema update failed.")
            else:
                logger.warning(f"No download URL found for {schema_type} schema")
    
    # Update cache info after all schemas are updated
    if updated:
        update_cache_info(latest_info)
    
    return updated


def load_schema(schema_type: str = "package", version: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Load a schema from the cache or download if needed.
    
    Args:
        schema_type: Either "package" or "registry". Defaults to "package".
        version (optional): Specific version to load. If None, loads latest version.
        
    Returns:
        Dict containing the schema, or None if unavailable.
        
    Raises:
        ValueError: If schema_type is not "package" or "registry".
    """
    if schema_type not in ["package", "registry"]:
        raise ValueError(f"Unknown schema type: {schema_type}")
      # If specific version requested, try to load directly from GitHub releases
    if version is not None:
        # Ensure version has 'v' prefix
        if not version.startswith('v'):
            version = f"v{version}"
        
        # Determine schema filename and release tag
        if schema_type == "package":
            filename = "hatch_pkg_metadata_schema.json"
            release_tag = f"schemas-package-{version}"
        else:
            filename = "hatch_all_pkg_metadata_schema.json"
            release_tag = f"schemas-registry-{version}"
        
        # Try to download specific version from release
        schema_url = f"{GITHUB_RELEASES_BASE}/{release_tag}/{filename}"
        try:
            logger.debug(f"Loading {schema_type} schema version {version} from {schema_url}")
            response = requests.get(schema_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error loading {schema_type} schema version {version}: {e}")
            return None
    
    # For latest version, ensure schemas are up to date
    check_and_update_schemas()
    
    # Determine schema filename based on type
    if schema_type == "package":
        schema_filename = "hatch_pkg_metadata_schema.json"
    else:
        schema_filename = "hatch_all_pkg_metadata_schema.json"
    
    # Load from cache
    schema_path = CACHE_DIR / schema_type / schema_filename
    if schema_path.exists():
        try:
            logger.debug(f"Loading {schema_type} schema from {schema_path}")
            with open(schema_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading {schema_type} schema: {e}")
            return None
    else:
        logger.warning(f"{schema_type.capitalize()} schema file not found: {schema_path}")
        return None


if __name__ == "__main__":
    # Set up logging
    configure_logger(
        level=logging.INFO,
        log_file=str(Path.home() / ".crackingshells" / "logs" / "schema_updates.log")
    )
    
    # Example usage
    updated = check_and_update_schemas()
    
    if updated:
        logger.info("Downloaded new schemas")
    
    # Load and use the schemas
    package_schema = load_schema("package")
    registry_schema = load_schema("registry")
    
    if package_schema:
        logger.info(f"Package schema title: {package_schema.get('title')}")
    
    if registry_schema:
        logger.info(f"Registry schema title: {registry_schema.get('title')}")