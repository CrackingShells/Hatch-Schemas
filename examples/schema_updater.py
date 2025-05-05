#!/usr/bin/env python
"""
Schema Update Checker Example

This script demonstrates how to:
1. Check for the latest schema version for each schema type
2. Compare with a locally cached version
3. Download the latest schema if needed
"""

import os
import json
import shutil
import logging
import requests
from pathlib import Path
from datetime import datetime
import tempfile
import zipfile

# Configure logging
logger = logging.getLogger("schema_updater")
logger.setLevel(logging.INFO)

# Configuration
SCHEMA_INFO_URL = "https://crackingshells.github.io/Hatch-Schemas/latest.json"
CACHE_DIR = Path.home() / ".crackingshells" / "schemas"
CACHE_INFO_FILE = CACHE_DIR / "schema_info.json"


def configure_logger(level=logging.INFO, log_file=None):
    """Configure the logger with custom settings.
    
    Args:
        level: The logging level (e.g., logging.DEBUG, logging.INFO)
        log_file: Optional path to a log file
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


def get_latest_schema_info():
    """Fetch information about the latest schema versions."""
    try:
        logger.debug(f"Requesting schema info from {SCHEMA_INFO_URL}")
        response = requests.get(SCHEMA_INFO_URL, timeout=10)
        response.raise_for_status()
        logger.debug("Schema info retrieved successfully")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching schema info: {e}")
        return None


def get_cached_schema_info():
    """Get information about the locally cached schema versions."""
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


def download_and_extract_schema(schema_type, download_url):
    """Download and extract schema files to the cache directory for a specific schema type.
    
    Args:
        schema_type: Either "package" or "registry"
        download_url: URL to download the schema ZIP archive
    """
    try:
        # Create a temporary file to download to
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_file:
            temp_path = temp_file.name
        
        # Download the schema zip
        logger.info(f"Downloading {schema_type} schema from {download_url}")
        response = requests.get(download_url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Save to temporary file
        with open(temp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Clear existing cache directory for this schema type
        schema_cache_dir = CACHE_DIR / schema_type
        if schema_cache_dir.exists():
            logger.debug(f"Clearing existing cache directory: {schema_cache_dir}")
            shutil.rmtree(schema_cache_dir)
        
        # Create schema type directory
        schema_cache_dir.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            logger.debug(f"Extracting {schema_type} schema to {schema_cache_dir}")
            zip_ref.extractall(schema_cache_dir)
            
            # Find the version directory in the extracted content
            extracted_dirs = [d for d in os.listdir(schema_cache_dir) if os.path.isdir(os.path.join(schema_cache_dir, d))]
            if extracted_dirs:
                version_dir = extracted_dirs[0]
                extracted_version_path = os.path.join(schema_cache_dir, version_dir)
                
                logger.debug(f"Restructuring extracted content from {version_dir} directory")
                # Move the contents up one level (from cache_dir/package/v1/... to cache_dir/package/...)
                for item in os.listdir(extracted_version_path):
                    target_path = os.path.join(schema_cache_dir, item)
                    source_path = os.path.join(extracted_version_path, item)
                    
                    # Remove existing file/directory if it exists
                    if os.path.exists(target_path):
                        if os.path.isdir(target_path):
                            shutil.rmtree(target_path)
                        else:
                            os.remove(target_path)
                    
                    # Move the item
                    shutil.move(source_path, target_path)
                
                # Remove the now-empty version directory
                if os.path.exists(extracted_version_path):
                    shutil.rmtree(extracted_version_path)
        
        # Clean up the temporary file
        os.unlink(temp_path)
        logger.debug(f"{schema_type.capitalize()} schema extraction completed successfully")
        
        return True
    except Exception as e:
        logger.error(f"Error downloading {schema_type} schema: {e}", exc_info=True)
        return False


def update_cache_info(schema_info):
    """Update the cached schema information."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        logger.debug(f"Writing updated schema info to {CACHE_INFO_FILE}")
        with open(CACHE_INFO_FILE, "w") as f:
            json.dump(schema_info, f, indent=2)
        return True
    except IOError as e:
        logger.error(f"Error writing cache info: {e}")
        return False


def check_and_update_schemas():
    """Check if new schema versions are available and update if needed."""
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
            download_url = latest_info.get(schema_type, {}).get("download_url")
            if download_url:
                logger.info(f"New {schema_type} schema version available: {latest_version}")
                if download_and_extract_schema(schema_type, download_url):
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


def load_schema(schema_type="package"):
    """Load a schema from the cache.
    
    Args:
        schema_type: Either "package" or "registry"
        
    Returns:
        The schema as a dictionary, or None if not available
    """
    # Ensure schemas are up to date
    check_and_update_schemas()
    
    # Get the cached schema info to determine current version
    cached_info = get_cached_schema_info()
    if not cached_info:
        logger.warning("No cached schema information available.")
        return None
    
    # Get the specific schema info
    schema_info = cached_info.get(schema_type, {})
    if not schema_info:
        logger.warning(f"No {schema_type} schema information available in the cache.")
        return None
    
    # Get the schema version
    version = schema_info.get("version")
    if not version:
        version_key = f"latest_{schema_type}_version"
        version = cached_info.get(version_key)
        if not version:
            logger.error(f"No version information for {schema_type} schema in cached schema info")
            return None
    
    # Ensure version has 'v' prefix
    if not version.startswith('v'):
        version = f"v{version}"
    
    # Determine schema filename based on type
    if schema_type == "package":
        schema_filename = "hatch_pkg_metadata_schema.json"
    elif schema_type == "registry":
        schema_filename = "hatch_all_pkg_metadata_schema.json"
    else:
        logger.error(f"Unknown schema type: {schema_type}")
        raise ValueError(f"Unknown schema type: {schema_type}")
    
    # Load and return the schema
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