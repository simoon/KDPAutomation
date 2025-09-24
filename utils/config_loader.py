"""
Configuration Loader for BookBolt Automation
Handles loading and validation of JSON configuration files
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors"""
    pass

class ConfigLoader:
    """
    Loads and validates configuration files for BookBolt automation.
    Provides centralized configuration management with validation.
    """
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize config loader.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self.areas_cache = None
        self.sequences_cache = None
        self.settings_cache = None
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🔧 ConfigLoader initialized")
        print(f"📁 Config directory: {self.config_dir.absolute()}")
    
    def load_areas(self, filename: str = "bookbolt_areas.json", use_cache: bool = True) -> Dict[str, Any]:
        """
        Load click areas configuration from JSON file.
        
        Args:
            filename: Name of the areas configuration file
            use_cache: Whether to use cached data if available
            
        Returns:
            Dict containing areas configuration
            
        Raises:
            ConfigurationError: If file not found or invalid format
        """
        if use_cache and self.areas_cache is not None:
            return self.areas_cache
        
        print(f"📍 Loading click areas from {filename}")
        
        config = self._load_json_file(filename)
        
        # Validate areas configuration
        if not self.validate_areas_config(config):
            raise ConfigurationError(f"Invalid areas configuration in {filename}")
        
        # Cache the configuration
        self.areas_cache = config
        
        areas_count = len(config.get('areas', {}))
        print(f"✅ Loaded {areas_count} click areas successfully")
        
        return config
    
    def load_sequences(self, filename: str = "bookbolt_sequences.json", use_cache: bool = True) -> Dict[str, Any]:
        """
        Load action sequences configuration from JSON file.
        
        Args:
            filename: Name of the sequences configuration file
            use_cache: Whether to use cached data if available
            
        Returns:
            Dict containing sequences configuration
            
        Raises:
            ConfigurationError: If file not found or invalid format
        """
        if use_cache and self.sequences_cache is not None:
            return self.sequences_cache
        
        print(f"🎬 Loading action sequences from {filename}")
        
        config = self._load_json_file(filename)
        
        # Validate sequences configuration
        if not self.validate_sequences_config(config):
            raise ConfigurationError(f"Invalid sequences configuration in {filename}")
        
        # Cache the configuration
        self.sequences_cache = config
        
        sequences_count = len(config.get('sequences', {}))
        actions_count = sum(len(seq.get('actions', [])) for seq in config.get('sequences', {}).values())
        print(f"✅ Loaded {sequences_count} sequences with {actions_count} total actions")
        
        return config
    
    def load_settings(self, filename: str = "settings.json", use_cache: bool = True) -> Dict[str, Any]:
        """
        Load general settings configuration.
        
        Args:
            filename: Name of the settings file
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing settings
        """
        if use_cache and self.settings_cache is not None:
            return self.settings_cache
        
        print(f"⚙️ Loading settings from {filename}")
        
        try:
            config = self._load_json_file(filename)
            self.settings_cache = config
            print(f"✅ Settings loaded successfully")
            return config
        except FileNotFoundError:
            # Return default settings if file doesn't exist
            default_settings = self._get_default_settings()
            print(f"⚠️ Settings file not found, using defaults")
            return default_settings
    
    def get_area_by_name(self, area_name: str) -> Optional[Dict[str, Any]]:
        """
        Get specific area configuration by name.
        
        Args:
            area_name: Name of the area to retrieve
            
        Returns:
            Area configuration dict or None if not found
        """
        areas_config = self.load_areas()
        return areas_config.get('areas', {}).get(area_name)
    
    def get_sequence_by_name(self, sequence_name: str) -> Optional[Dict[str, Any]]:
        """
        Get specific sequence configuration by name.
        
        Args:
            sequence_name: Name of the sequence to retrieve
            
        Returns:
            Sequence configuration dict or None if not found
        """
        sequences_config = self.load_sequences()
        return sequences_config.get('sequences', {}).get(sequence_name)
    
    def list_available_areas(self) -> List[str]:
        """
        Get list of all available area names.
        
        Returns:
            List of area names
        """
        areas_config = self.load_areas()
        return list(areas_config.get('areas', {}).keys())
    
    def list_available_sequences(self) -> List[str]:
        """
        Get list of all available sequence names.
        
        Returns:
            List of sequence names
        """
        sequences_config = self.load_sequences()
        return list(sequences_config.get('sequences', {}).keys())
    
    def get_areas_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all areas belonging to a specific category.
        
        Args:
            category: Category to filter by
            
        Returns:
            Dict of areas in the specified category
        """
        areas_config = self.load_areas()
        areas = areas_config.get('areas', {})
        
        return {
            name: area for name, area in areas.items()
            if area.get('category') == category
        }
    
    def get_sequences_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all sequences belonging to a specific category.
        
        Args:
            category: Category to filter by
            
        Returns:
            Dict of sequences in the specified category
        """
        sequences_config = self.load_sequences()
        sequences = sequences_config.get('sequences', {})
        
        return {
            name: seq for name, seq in sequences.items()
            if seq.get('category') == category
        }
    
    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """
        Load and parse JSON configuration file.
        
        Args:
            filename: Name of the file to load
            
        Returns:
            Parsed JSON data
            
        Raises:
            ConfigurationError: If file not found or invalid JSON
        """
        file_path = self.config_dir / filename
        
        if not file_path.exists():
            raise ConfigurationError(f"Configuration file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in {filename}: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error reading {filename}: {e}")
    
    def validate_areas_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate areas configuration structure and data.
        
        Args:
            config: Areas configuration to validate
            
        Returns:
            True if configuration is valid
        """
        try:
            # Check required top-level keys
            if 'areas' not in config:
                print("❌ Areas configuration missing 'areas' key")
                return False
            
            areas = config['areas']
            if not isinstance(areas, dict):
                print("❌ Areas must be a dictionary")
                return False
            
            # Validate each area
            for area_name, area_config in areas.items():
                if not self._validate_single_area(area_name, area_config):
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Areas validation error: {e}")
            return False
    
    def validate_sequences_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate sequences configuration structure and data.
        
        Args:
            config: Sequences configuration to validate
            
        Returns:
            True if configuration is valid
        """
        try:
            # Check required top-level keys
            if 'sequences' not in config:
                print("❌ Sequences configuration missing 'sequences' key")
                return False
            
            sequences = config['sequences']
            if not isinstance(sequences, dict):
                print("❌ Sequences must be a dictionary")
                return False
            
            # Validate each sequence
            for seq_name, seq_config in sequences.items():
                if not self._validate_single_sequence(seq_name, seq_config):
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Sequences validation error: {e}")
            return False
    
    def _validate_single_area(self, area_name: str, area_config: Dict[str, Any]) -> bool:
        """Validate a single area configuration"""
        required_fields = ['name', 'coordinates', 'description']
        
        # Check required fields
        for field in required_fields:
            if field not in area_config:
                print(f"❌ Area '{area_name}' missing required field: {field}")
                return False
        
        # Validate coordinates format
        coordinates = area_config['coordinates']
        if not isinstance(coordinates, list) or len(coordinates) != 4:
            print(f"❌ Area '{area_name}' coordinates must be a list of 4 integers")
            return False
        
        if not all(isinstance(coord, int) for coord in coordinates):
            print(f"❌ Area '{area_name}' coordinates must be integers")
            return False
        
        # Validate coordinate values (x1, y1, x2, y2)
        x1, y1, x2, y2 = coordinates
        if x1 >= x2 or y1 >= y2:
            print(f"❌ Area '{area_name}' has invalid coordinate bounds")
            return False
        
        return True
    
    def _validate_single_sequence(self, seq_name: str, seq_config: Dict[str, Any]) -> bool:
        """Validate a single sequence configuration"""
        required_fields = ['name', 'description', 'actions']
        
        # Check required fields
        for field in required_fields:
            if field not in seq_config:
                print(f"❌ Sequence '{seq_name}' missing required field: {field}")
                return False
        
        # Validate actions
        actions = seq_config['actions']
        if not isinstance(actions, list):
            print(f"❌ Sequence '{seq_name}' actions must be a list")
            return False
        
        # Validate each action
        for i, action in enumerate(actions):
            if not self._validate_single_action(seq_name, i + 1, action):
                return False
        
        return True
    
    def _validate_single_action(self, seq_name: str, action_num: int, action: Dict[str, Any]) -> bool:
        """Validate a single action within a sequence"""
        required_fields = ['type']
        
        # Check required fields
        for field in required_fields:
            if field not in action:
                print(f"❌ Sequence '{seq_name}' action {action_num} missing required field: {field}")
                return False
        
        action_type = action['type']
        valid_types = ['click_area', 'type_text', 'type_dynamic_text', 'select_all', 'copy_graphic', 'paste_graphic', 'press_key', 'wait']
        
        if action_type not in valid_types:
            print(f"❌ Sequence '{seq_name}' action {action_num} has invalid type: {action_type}")
            return False
        
        # Type-specific validation
        if action_type == 'click_area' and 'area' not in action:
            print(f"❌ click_area action in '{seq_name}' missing 'area' field")
            return False
        
        if action_type == 'type_text' and 'text' not in action:
            print(f"❌ type_text action in '{seq_name}' missing 'text' field")
            return False
        
        if action_type == 'press_key' and 'key' not in action:
            print(f"❌ press_key action in '{seq_name}' missing 'key' field")
            return False
        
        return True
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings configuration"""
        return {
            "browser": {
                "driver_type": "chrome",
                "headless": False,
                "window_width": 1920,
                "window_height": 1080,
                "page_load_timeout": 30
            },
            "mouse": {
                "movement_speed": 1.0,
                "click_delay_min": 0.1,
                "click_delay_max": 0.5,
                "randomize_position": True,
                "max_position_offset": 5
            },
            "automation": {
                "screenshot_dir": "static/screenshots",
                "log_dir": "static/logs",
                "default_timeout": 10,
                "retry_attempts": 3,
                "anti_detection": True
            }
        }
    
    def clear_cache(self):
        """Clear all cached configurations"""
        self.areas_cache = None
        self.sequences_cache = None
        self.settings_cache = None
        print("🗑️ Configuration cache cleared")
    
    def export_configuration_summary(self) -> str:
        """
        Export a summary of current configuration for debugging.
        
        Returns:
            Formatted string with configuration summary
        """
        try:
            areas_config = self.load_areas()
            sequences_config = self.load_sequences()
            
            summary = []
            summary.append("📋 BOOKBOLT CONFIGURATION SUMMARY")
            summary.append("=" * 50)
            
            # Areas summary
            areas = areas_config.get('areas', {})
            summary.append(f"📍 CLICK AREAS ({len(areas)} total):")
            for name, area in areas.items():
                coords = area['coordinates']
                category = area.get('category', 'unknown')
                summary.append(f"   • {area['name']}: ({coords[0]}, {coords[1]}) → ({coords[2]}, {coords[3]}) [{category}]")
            
            # Sequences summary
            sequences = sequences_config.get('sequences', {})
            summary.append(f"\n🎬 ACTION SEQUENCES ({len(sequences)} total):")
            for name, seq in sequences.items():
                actions_count = len(seq.get('actions', []))
                category = seq.get('category', 'unknown')
                summary.append(f"   • {seq['name']}: {actions_count} actions [{category}]")
            
            summary.append("\n" + "=" * 50)
            return "\n".join(summary)
            
        except Exception as e:
            return f"❌ Error generating configuration summary: {e}"

# Convenience functions for quick access
def load_bookbolt_areas(config_dir: str = "config") -> Dict[str, Any]:
    """Quick function to load areas configuration"""
    loader = ConfigLoader(config_dir)
    return loader.load_areas()['areas']

def load_bookbolt_sequences(config_dir: str = "config") -> Dict[str, Any]:
    """Quick function to load sequences configuration"""
    loader = ConfigLoader(config_dir)
    return loader.load_sequences()['sequences']

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Configuration Loader...")
    
    try:
        # Create loader
        loader = ConfigLoader("config")
        
        # Test loading areas
        areas_config = loader.load_areas()
        print(f"✅ Areas loaded: {len(areas_config.get('areas', {}))}")
        
        # Test loading sequences
        sequences_config = loader.load_sequences()
        print(f"✅ Sequences loaded: {len(sequences_config.get('sequences', {}))}")
        
        # Test utility functions
        area_names = loader.list_available_areas()
        sequence_names = loader.list_available_sequences()
        print(f"📍 Available areas: {area_names}")
        print(f"🎬 Available sequences: {sequence_names}")
        
        # Export summary
        print("\n" + loader.export_configuration_summary())
        
        print("\n✅ Configuration loader test completed!")
        
    except Exception as e:
        print(f"❌ Configuration loader test failed: {e}")