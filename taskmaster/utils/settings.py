"""
Settings management for TaskMaster Pro.

This module handles loading and saving application settings.
"""
import os
import json
from typing import Dict, Any, Optional


class Settings:
    """Manages application settings with persistence."""
    
    DEFAULTS = {
        'app': {
            'version': '1.0.0',
            'theme': 'light',  # 'light' or 'dark'
            'window_geometry': None,
            'window_state': None,
        },
        'tasks': {
            'default_priority': 'MEDIUM',
            'default_due_days': 7,
            'show_completed': True,
        },
        'notifications': {
            'enabled': True,
            'sound': True,
            'reminder_minutes': 15,
        },
        'backup': {
            'auto_backup': True,
            'backup_location': '',
            'backup_interval_days': 7,
        }
    }
    
    def __init__(self, filename: str = None):
        """Initialize settings with optional custom filename.
        
        Args:
            filename: Path to settings file. If None, uses default location.
        """
        if filename is None:
            # Default location: user's app data directory
            app_data = os.getenv('APPDATA') or os.path.expanduser('~')
            self.settings_dir = os.path.join(app_data, 'TaskMasterPro')
            os.makedirs(self.settings_dir, exist_ok=True)
            self.filename = os.path.join(self.settings_dir, 'settings.json')
        else:
            self.filename = filename
            self.settings_dir = os.path.dirname(filename)
        
        # Initialize with default values
        self._settings = self.DEFAULTS.copy()
        
        # Load saved settings if they exist
        self.load()
    
    def load(self) -> bool:
        """Load settings from file.
        
        Returns:
            bool: True if settings were loaded successfully, False otherwise.
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self._deep_update(self._settings, loaded_settings)
            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading settings: {e}")
            return False
    
    def save(self) -> bool:
        """Save current settings to file.
        
        Returns:
            bool: True if settings were saved successfully, False otherwise.
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=4, sort_keys=True)
            return True
        except IOError as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default=None) -> Any:
        """Get a setting value by dot notation key.
        
        Args:
            key: Dot notation key (e.g., 'app.theme')
            default: Default value if key is not found
            
        Returns:
            The setting value or default if not found.
        """
        keys = key.split('.')
        value = self._settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any, save_immediately: bool = False) -> bool:
        """Set a setting value by dot notation key.
        
        Args:
            key: Dot notation key (e.g., 'app.theme')
            value: Value to set
            save_immediately: If True, save settings to disk immediately
            
        Returns:
            bool: True if the setting was updated successfully.
        """
        keys = key.split('.')
        current = self._settings
        
        try:
            # Navigate to the parent of the target key
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            # Set the value
            current[keys[-1]] = value
            
            # Save if requested
            if save_immediately:
                return self.save()
                
            return True
        except (KeyError, TypeError):
            return False
    
    def _deep_update(self, original: Dict, update: Dict) -> Dict:
        """Recursively update a dictionary."""
        for key, value in update.items():
            if isinstance(value, dict) and key in original and isinstance(original[key], dict):
                original[key] = self._deep_update(original[key], value)
            else:
                original[key] = value
        return original
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to default values.
        
        Returns:
            bool: True if reset was successful.
        """
        self._settings = self.DEFAULTS.copy()
        return self.save()
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access to settings."""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-style setting of values."""
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """Check if a setting exists."""
        try:
            self.get(key)
            return True
        except KeyError:
            return False


# Global settings instance
settings = Settings()
