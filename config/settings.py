"""
Configuration management for browser automation software.
Handles loading settings from JSON files, environment variables, and provides defaults.
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, Union, List

@dataclass
class BrowserConfig:
    """Browser-specific configuration settings"""
    driver_type: str = "chrome"                    # Browser type (chrome, firefox, edge)
    headless: bool = False                         # Run browser in headless mode
    window_width: int = 1920                       # Browser window width
    window_height: int = 1080                      # Browser window height
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    page_load_timeout: int = 30                    # Page load timeout in seconds
    implicit_wait: int = 10                        # Implicit wait timeout
    download_dir: str = "static/downloads"         # Download directory
    enable_images: bool = True                     # Load images
    enable_javascript: bool = True                 # Enable JavaScript
    enable_plugins: bool = False                   # Enable plugins
    incognito_mode: bool = True                    # Use incognito/private mode
    disable_extensions: bool = True                # Disable browser extensions
    disable_dev_shm: bool = True                   # Disable /dev/shm usage
    disable_gpu: bool = False                      # Disable GPU acceleration
    window_position_x: int = 100                   # Window X position
    window_position_y: int = 100                   # Window Y position

@dataclass
class MouseConfig:
    """Mouse control configuration settings"""
    movement_speed: float = 1.0                    # Mouse movement speed multiplier
    click_delay_min: float = 0.1                   # Minimum delay between clicks
    click_delay_max: float = 0.5                   # Maximum delay between clicks
    move_delay_min: float = 0.01                   # Minimum delay between mouse moves
    move_delay_max: float = 0.03                   # Maximum delay between mouse moves
    randomize_position: bool = True                # Add random offset to clicks
    max_position_offset: int = 5                   # Maximum pixel offset for randomization
    natural_movement: bool = True                  # Use natural mouse movement curves
    movement_steps: int = 20                       # Steps for smooth movement
    double_click_interval: float = 0.1             # Interval between double clicks
    scroll_delay: float = 0.1                      # Delay between scroll actions
    drag_duration_min: float = 0.5                 # Minimum drag duration
    drag_duration_max: float = 2.0                 # Maximum drag duration

@dataclass
class TypingConfig:
    """Text typing configuration settings"""
    typing_speed_min: float = 0.05                 # Minimum delay between keystrokes
    typing_speed_max: float = 0.15                 # Maximum delay between keystrokes
    word_pause_min: float = 0.1                    # Minimum pause between words
    word_pause_max: float = 0.3                    # Maximum pause between words
    mistake_probability: float = 0.02              # Probability of making typing mistakes
    correction_delay: float = 0.1                  # Delay before correcting mistakes
    natural_pauses: bool = True                    # Add natural pauses while typing
    pause_on_punctuation: bool = True              # Pause longer on punctuation
    variable_speed: bool = True                    # Vary typing speed
    burst_typing_probability: float = 0.1          # Probability of fast typing bursts

@dataclass
class AutomationConfig:
    """General automation configuration settings"""
    screenshot_dir: str = "static/screenshots"     # Screenshot storage directory
    log_dir: str = "static/logs"                   # Log files directory
    template_dir: str = "static/templates"         # Template images directory
    default_timeout: int = 10                      # Default timeout for operations
    retry_attempts: int = 3                        # Number of retry attempts
    retry_delay: float = 1.0                       # Delay between retries
    anti_detection: bool = True                    # Enable anti-detection features
    human_behavior: bool = True                    # Simulate human behavior
    action_delay_min: float = 0.5                  # Minimum delay between actions
    action_delay_max: float = 2.0                  # Maximum delay between actions
    screenshot_on_error: bool = True               # Take screenshot on errors
    max_screenshot_size: int = 1920                # Maximum screenshot width
    compress_screenshots: bool = True              # Compress screenshot files
    session_timeout: int = 3600                    # Session timeout in seconds

@dataclass
class DetectionConfig:
    """Anti-detection configuration settings"""
    randomize_timing: bool = True                  # Randomize action timing
    randomize_coordinates: bool = True             # Randomize click coordinates
    simulate_human_errors: bool = True             # Simulate human mistakes
    vary_user_agent: bool = False                  # Rotate user agents
    use_proxy: bool = False                        # Use proxy servers
    proxy_list: List[str] = None                   # List of proxy servers
    stealth_mode: bool = True                      # Enable stealth features
    viewport_randomization: bool = False           # Randomize browser viewport
    timezone_randomization: bool = False           # Randomize timezone
    webgl_randomization: bool = False              # Randomize WebGL fingerprint
    
    def __post_init__(self):
        if self.proxy_list is None:
            self.proxy_list = []

@dataclass
class LoggingConfig:
    """Logging configuration settings"""
    log_level: str = "INFO"                        # Logging level
    console_colors: bool = True                    # Use colors in console output
    log_to_file: bool = True                       # Enable file logging
    log_rotation_size: int = 10 * 1024 * 1024      # Log file size before rotation (10MB)
    log_backup_count: int = 5                      # Number of backup log files
    log_retention_days: int = 30                   # Days to keep log files
    performance_logging: bool = True               # Log performance metrics
    action_logging: bool = True                    # Log automation actions
    debug_mode: bool = False                       # Enable debug mode

class Settings:
    """
    Central configuration manager for automation software.
    Loads settings from JSON files, environment variables, and provides validation.
    """
    
    def __init__(self, config_file: str = "config/settings.json"):
        self.config_file = config_file
        self.project_root = Path(__file__).parent.parent
        self.config_path = self.project_root / config_file
        
        # Initialize configuration objects with defaults
        self.browser = BrowserConfig()
        self.mouse = MouseConfig()
        self.typing = TypingConfig()
        self.automation = AutomationConfig()
        self.detection = DetectionConfig()
        self.logging = LoggingConfig()
        
        # Load configuration from various sources
        self._load_configuration()
        self._validate_configuration()
        self._create_directories()
        
    def _load_configuration(self):
        """Load configuration from all sources in priority order"""
        # 1. Load from JSON file
        self._load_from_json()
        
        # 2. Override with environment variables
        self._load_from_environment()
        
        # 3. Load local overrides if they exist
        self._load_local_overrides()
    
    def _load_from_json(self):
        """Load configuration from JSON file"""
        if not self.config_path.exists():
            print(f"⚠️  Config file not found: {self.config_path}")
            print("ℹ️  Using default configuration")
            return
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Update configuration objects from JSON data
            self._update_config_from_dict(config_data)
            print(f"✅ Configuration loaded from {self.config_path}")
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in config file: {e}")
            print("ℹ️  Using default configuration")
        except Exception as e:
            print(f"❌ Error loading config file: {e}")
            print("ℹ️  Using default configuration")
    
    def _update_config_from_dict(self, config_data: Dict[str, Any]):
        """Update configuration objects from dictionary"""
        
        # Update browser config
        if 'browser' in config_data:
            for key, value in config_data['browser'].items():
                if hasattr(self.browser, key):
                    setattr(self.browser, key, value)
                else:
                    print(f"⚠️  Unknown browser config: {key}")
        
        # Update mouse config  
        if 'mouse' in config_data:
            for key, value in config_data['mouse'].items():
                if hasattr(self.mouse, key):
                    setattr(self.mouse, key, value)
                else:
                    print(f"⚠️  Unknown mouse config: {key}")
        
        # Update typing config
        if 'typing' in config_data:
            for key, value in config_data['typing'].items():
                if hasattr(self.typing, key):
                    setattr(self.typing, key, value)
                else:
                    print(f"⚠️  Unknown typing config: {key}")
        
        # Update automation config
        if 'automation' in config_data:
            for key, value in config_data['automation'].items():
                if hasattr(self.automation, key):
                    setattr(self.automation, key, value)
                else:
                    print(f"⚠️  Unknown automation config: {key}")
        
        # Update detection config
        if 'detection' in config_data:
            for key, value in config_data['detection'].items():
                if hasattr(self.detection, key):
                    setattr(self.detection, key, value)
                else:
                    print(f"⚠️  Unknown detection config: {key}")
        
        # Update logging config
        if 'logging' in config_data:
            for key, value in config_data['logging'].items():
                if hasattr(self.logging, key):
                    setattr(self.logging, key, value)
                else:
                    print(f"⚠️  Unknown logging config: {key}")
    
    def _load_from_environment(self):
        """Load configuration overrides from environment variables"""
        
        # Browser settings
        if os.getenv('BROWSER_HEADLESS'):
            self.browser.headless = os.getenv('BROWSER_HEADLESS').lower() == 'true'
        if os.getenv('BROWSER_TYPE'):
            self.browser.driver_type = os.getenv('BROWSER_TYPE')
        if os.getenv('BROWSER_WIDTH'):
            self.browser.window_width = int(os.getenv('BROWSER_WIDTH'))
        if os.getenv('BROWSER_HEIGHT'):
            self.browser.window_height = int(os.getenv('BROWSER_HEIGHT'))
        
        # Mouse settings
        if os.getenv('MOUSE_SPEED'):
            self.mouse.movement_speed = float(os.getenv('MOUSE_SPEED'))
        if os.getenv('CLICK_DELAY_MIN'):
            self.mouse.click_delay_min = float(os.getenv('CLICK_DELAY_MIN'))
        if os.getenv('CLICK_DELAY_MAX'):
            self.mouse.click_delay_max = float(os.getenv('CLICK_DELAY_MAX'))
        
        # Automation settings
        if os.getenv('ANTI_DETECTION'):
            self.automation.anti_detection = os.getenv('ANTI_DETECTION').lower() == 'true'
        if os.getenv('DEFAULT_TIMEOUT'):
            self.automation.default_timeout = int(os.getenv('DEFAULT_TIMEOUT'))
        if os.getenv('RETRY_ATTEMPTS'):
            self.automation.retry_attempts = int(os.getenv('RETRY_ATTEMPTS'))
        
        # Logging settings
        if os.getenv('LOG_LEVEL'):
            self.logging.log_level = os.getenv('LOG_LEVEL').upper()
        if os.getenv('LOG_TO_FILE'):
            self.logging.log_to_file = os.getenv('LOG_TO_FILE').lower() == 'true'
        if os.getenv('DEBUG_MODE'):
            self.logging.debug_mode = os.getenv('DEBUG_MODE').lower() == 'true'
    
    def _load_local_overrides(self):
        """Load local configuration overrides"""
        local_config_path = self.project_root / "config" / "local_settings.json"
        
        if local_config_path.exists():
            try:
                with open(local_config_path, 'r', encoding='utf-8') as f:
                    local_config = json.load(f)
                
                self._update_config_from_dict(local_config)
                print(f"✅ Local overrides loaded from {local_config_path}")
                
            except Exception as e:
                print(f"⚠️  Error loading local overrides: {e}")
    
    def _validate_configuration(self):
        """Validate configuration values"""
        errors = []
        
        # Validate browser config
        if self.browser.driver_type not in ['chrome', 'firefox', 'edge', 'safari']:
            errors.append(f"Invalid browser type: {self.browser.driver_type}")
        
        if self.browser.window_width < 800 or self.browser.window_height < 600:
            errors.append("Browser window size too small (minimum 800x600)")
        
        if self.browser.page_load_timeout < 5:
            errors.append("Page load timeout too small (minimum 5 seconds)")
        
        # Validate mouse config
        if self.mouse.click_delay_min > self.mouse.click_delay_max:
            errors.append("Mouse click_delay_min cannot be greater than click_delay_max")
        
        if self.mouse.movement_speed <= 0:
            errors.append("Mouse movement speed must be positive")
        
        # Validate automation config
        if self.automation.retry_attempts < 0:
            errors.append("Retry attempts cannot be negative")
        
        if self.automation.default_timeout < 1:
            errors.append("Default timeout too small (minimum 1 second)")
        
        # Print validation errors
        if errors:
            print("❌ Configuration validation errors:")
            for error in errors:
                print(f"   - {error}")
            print("ℹ️  Please fix configuration and restart")
    
    def _create_directories(self):
        """Create required directories if they don't exist"""
        directories = [
            self.automation.screenshot_dir,
            self.automation.log_dir,
            self.automation.template_dir,
            self.browser.download_dir,
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"⚠️  Could not create directory {dir_path}: {e}")
    
    # Convenience methods for getting paths
    def get_screenshot_path(self, filename: str) -> str:
        """Get full path for screenshot file"""
        return str(self.project_root / self.automation.screenshot_dir / filename)
    
    def get_log_path(self, filename: str) -> str:
        """Get full path for log file"""
        return str(self.project_root / self.automation.log_dir / filename)
    
    def get_template_path(self, filename: str) -> str:
        """Get full path for template file"""
        return str(self.project_root / self.automation.template_dir / filename)
    
    def get_download_path(self, filename: str = "") -> str:
        """Get full path for download directory or file"""
        if filename:
            return str(self.project_root / self.browser.download_dir / filename)
        return str(self.project_root / self.browser.download_dir)
    
    # Configuration export/import methods
    def export_config(self, filepath: Optional[str] = None) -> str:
        """
        Export current configuration to JSON file.
        
        Args:
            filepath: Optional path to save config file
            
        Returns:
            str: Path to exported configuration file
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.project_root / f"config/exported_config_{timestamp}.json"
        else:
            filepath = Path(filepath)
        
        config_dict = {
            'browser': asdict(self.browser),
            'mouse': asdict(self.mouse),
            'typing': asdict(self.typing),
            'automation': asdict(self.automation),
            'detection': asdict(self.detection),
            'logging': asdict(self.logging)
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Configuration exported to {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Failed to export configuration: {e}")
            return ""
    
    def reload_config(self):
        """Reload configuration from files"""
        print("🔄 Reloading configuration...")
        self._load_configuration()
        self._validate_configuration()
        print("✅ Configuration reloaded")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration"""
        return {
            'browser': {
                'type': self.browser.driver_type,
                'headless': self.browser.headless,
                'window_size': f"{self.browser.window_width}x{self.browser.window_height}"
            },
            'automation': {
                'anti_detection': self.automation.anti_detection,
                'human_behavior': self.automation.human_behavior,
                'timeout': self.automation.default_timeout,
                'retries': self.automation.retry_attempts
            },
            'mouse': {
                'randomization': self.mouse.randomize_position,
                'natural_movement': self.mouse.natural_movement,
                'click_delay': f"{self.mouse.click_delay_min}-{self.mouse.click_delay_max}s"
            },
            'logging': {
                'level': self.logging.log_level,
                'to_file': self.logging.log_to_file,
                'debug_mode': self.logging.debug_mode
            }
        }
    
    def print_config_summary(self):
        """Print a formatted configuration summary"""
        summary = self.get_config_summary()
        
        print("\n" + "="*50)
        print("📋 CONFIGURATION SUMMARY")
        print("="*50)
        
        for section, config in summary.items():
            print(f"\n🔧 {section.upper()}:")
            for key, value in config.items():
                print(f"   • {key}: {value}")
        
        print("\n" + "="*50 + "\n")

# Global settings instance
_settings_instance = None

def get_settings() -> Settings:
    """
    Get global settings instance (singleton pattern).
    
    Returns:
        Settings: Global settings instance
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance

def reload_settings():
    """Reload global settings instance"""
    global _settings_instance
    if _settings_instance:
        _settings_instance.reload_config()

# Example usage and testing
if __name__ == "__main__":
    from datetime import datetime
    
    print("🧪 Testing configuration system...")
    
    # Create settings instance
    settings = Settings()
    
    # Print configuration summary
    settings.print_config_summary()
    
    # Test path methods
    print("\n📁 Path examples:")
    print(f"Screenshot: {settings.get_screenshot_path('test.png')}")
    print(f"Log file: {settings.get_log_path('test.log')}")
    print(f"Template: {settings.get_template_path('button.png')}")
    print(f"Download: {settings.get_download_path('file.pdf')}")
    
    # Test configuration export
    print("\n💾 Testing export...")
    exported_path = settings.export_config()
    if exported_path:
        print(f"✅ Configuration exported to: {exported_path}")
    
    # Test singleton pattern
    print("\n🔄 Testing singleton...")
    settings2 = get_settings()
    print(f"Same instance: {settings is settings2}")
    
    print("\n✅ Configuration system test completed!")