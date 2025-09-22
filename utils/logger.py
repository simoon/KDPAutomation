"""
Logging configuration for the browser automation software.
Uses Python standard logging library (no external dependencies).
"""

import sys
import os
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    # Emoji mapping
    EMOJIS = {
        'DEBUG': '🔍',
        'INFO': 'ℹ️ ',
        'WARNING': '⚠️ ',
        'ERROR': '❌',
        'CRITICAL': '🚨'
    }
    
    def __init__(self, use_colors=True, use_emojis=True):
        self.use_colors = use_colors
        self.use_emojis = use_emojis
        super().__init__()
    
    def format(self, record):
        # Create format string
        if self.use_colors and self.use_emojis:
            format_str = (
                f"{self.COLORS.get(record.levelname, '')}"
                f"{self.EMOJIS.get(record.levelname, '')} "
                f"%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
                f"{self.COLORS['RESET']}"
            )
        elif self.use_emojis:
            format_str = (
                f"{self.EMOJIS.get(record.levelname, '')} "
                f"%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
            )
        else:
            format_str = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
        
        formatter = logging.Formatter(format_str, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

class AutomationLogger:
    """
    Advanced logging system for browser automation using Python standard logging.
    """
    
    def __init__(self):
        self.is_configured = False
        self.log_dir = None
        self.console_level = "INFO"
        self.file_level = "DEBUG"
        self.loggers = {}
        self.root_logger = None
    
    def setup_logging(self, 
                     log_level: str = "INFO",
                     log_to_file: bool = True,
                     log_dir: Optional[Union[str, Path]] = None,
                     console_colors: bool = True,
                     file_max_size: int = 10 * 1024 * 1024,  # 10MB
                     backup_count: int = 5) -> bool:
        """
        Configure comprehensive logging for the application.
        
        Args:
            log_level: Minimum logging level for console (DEBUG, INFO, WARNING, ERROR)
            log_to_file: Whether to enable file logging
            log_dir: Directory for log files (defaults to static/logs)
            console_colors: Whether to use colors in console output
            file_max_size: Maximum size for each log file in bytes
            backup_count: Number of backup files to keep
            
        Returns:
            bool: True if setup successful
        """
        try:
            # Set log directory
            if log_dir is None:
                self.log_dir = Path("static/logs")
            else:
                self.log_dir = Path(log_dir)
            
            self.log_dir.mkdir(parents=True, exist_ok=True)
            self.console_level = log_level.upper()
            
            # Configure root logger
            self.root_logger = logging.getLogger('automation')
            self.root_logger.setLevel(logging.DEBUG)
            
            # Clear existing handlers
            self.root_logger.handlers.clear()
            
            # Setup console handler
            self._setup_console_handler(log_level, console_colors)
            
            # Setup file handlers if requested
            if log_to_file:
                self._setup_file_handlers(file_max_size, backup_count)
            
            # Test logging
            logger = self.get_logger("setup")
            logger.info("🚀 Logging system initialized successfully")
            logger.debug(f"📁 Log directory: {self.log_dir.absolute()}")
            logger.debug(f"📊 Console level: {self.console_level}, File level: {self.file_level}")
            
            self.is_configured = True
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup logging: {e}")
            return False
    
    def _setup_console_handler(self, log_level: str, console_colors: bool):
        """Setup console logging handler with colors and formatting"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Use colored formatter
        formatter = ColoredFormatter(use_colors=console_colors, use_emojis=True)
        console_handler.setFormatter(formatter)
        
        self.root_logger.addHandler(console_handler)
    
    def _setup_file_handlers(self, max_size: int, backup_count: int):
        """Setup file logging handlers with rotation"""
        
        # Main log file (all levels)
        main_log_file = self.log_dir / "automation.log"
        main_handler = logging.handlers.RotatingFileHandler(
            main_log_file, 
            maxBytes=max_size, 
            backupCount=backup_count,
            encoding='utf-8'
        )
        main_handler.setLevel(getattr(logging, self.file_level))
        main_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        main_handler.setFormatter(main_formatter)
        self.root_logger.addHandler(main_handler)
        
        # Error log file (only errors and above)
        error_log_file = self.log_dir / "errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file, 
            maxBytes=max_size, 
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s\n%(pathname)s:%(lineno)d',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_formatter)
        self.root_logger.addHandler(error_handler)
        
        # Actions log file (filtered for automation actions)
        actions_log_file = self.log_dir / "actions.log"
        actions_handler = logging.handlers.RotatingFileHandler(
            actions_log_file, 
            maxBytes=max_size, 
            backupCount=backup_count,
            encoding='utf-8'
        )
        actions_handler.setLevel(logging.INFO)
        actions_handler.addFilter(self._action_filter)
        actions_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        actions_handler.setFormatter(actions_formatter)
        self.root_logger.addHandler(actions_handler)
    
    def _action_filter(self, record):
        """Filter to capture only automation actions"""
        message = record.getMessage().lower()
        action_keywords = ["click", "type", "wait", "navigate", "screenshot", "scroll", "mouse", "browser"]
        return any(keyword in message for keyword in action_keywords)
    
    def get_logger(self, name: Optional[str] = None):
        """
        Get logger instance with optional name binding.
        
        Args:
            name: Optional component name
            
        Returns:
            Logger instance
        """
        if not self.is_configured:
            # Setup with defaults if not configured
            self.setup_logging()
        
        if name:
            logger_name = f"automation.{name}"
            if logger_name not in self.loggers:
                self.loggers[logger_name] = logging.getLogger(logger_name)
            return self.loggers[logger_name]
        
        return self.root_logger
    
    def log_automation_action(self, action: str, details: str = "", success: bool = True):
        """
        Log automation actions with consistent formatting.
        
        Args:
            action: Action performed (click, type, wait, etc.)
            details: Additional details about the action
            success: Whether the action was successful
        """
        status_emoji = "✅" if success else "❌"
        status_text = "SUCCESS" if success else "FAILED"
        
        message = f"{status_emoji} {action.upper()}"
        if details:
            message += f" | {details}"
        message += f" | Status: {status_text}"
        
        logger = self.get_logger("actions")
        if success:
            logger.info(message)
        else:
            logger.error(message)
    
    def log_performance_metric(self, operation: str, duration: float, additional_info: str = ""):
        """
        Log performance metrics for operations.
        
        Args:
            operation: Name of the operation
            duration: Time taken in seconds
            additional_info: Additional information
        """
        message = f"⏱️  PERFORMANCE | {operation} | Duration: {duration:.2f}s"
        if additional_info:
            message += f" | {additional_info}"
        
        logger = self.get_logger("performance")
        logger.info(message)
    
    def log_browser_event(self, event: str, url: str = "", details: str = ""):
        """
        Log browser-specific events.
        
        Args:
            event: Browser event (navigate, load, error, etc.)
            url: URL involved in the event
            details: Additional details
        """
        message = f"🌐 BROWSER | {event.upper()}"
        if url:
            message += f" | URL: {url}"
        if details:
            message += f" | {details}"
        
        logger = self.get_logger("browser")
        logger.info(message)
    
    def log_mouse_event(self, event: str, coordinates: tuple = None, details: str = ""):
        """
        Log mouse-specific events.
        
        Args:
            event: Mouse event (click, move, drag, etc.)
            coordinates: Mouse coordinates (x, y)
            details: Additional details
        """
        message = f"🖱️  MOUSE | {event.upper()}"
        if coordinates:
            message += f" | Coords: {coordinates}"
        if details:
            message += f" | {details}"
        
        logger = self.get_logger("mouse")
        logger.info(message)
    
    def log_detection_event(self, event: str, details: str = "", risk_level: str = "INFO"):
        """
        Log anti-detection related events.
        
        Args:
            event: Detection event
            details: Event details
            risk_level: Risk level (INFO, WARNING, ERROR)
        """
        emoji_map = {
            "INFO": "🔒",
            "WARNING": "⚠️",
            "ERROR": "🚨"
        }
        
        emoji = emoji_map.get(risk_level.upper(), "🔒")
        message = f"{emoji} ANTI-DETECTION | {event.upper()}"
        if details:
            message += f" | {details}"
        
        logger = self.get_logger("detection")
        log_method = getattr(logger, risk_level.lower())
        log_method(message)
    
    def create_session_log(self) -> str:
        """
        Create a new session log file and return its path.
        
        Returns:
            str: Path to the session log file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_log_file = self.log_dir / f"session_{timestamp}.log"
        
        # Create session handler
        session_handler = logging.FileHandler(session_log_file, encoding='utf-8')
        session_handler.setLevel(logging.DEBUG)
        session_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        session_handler.setFormatter(session_formatter)
        
        # Add to root logger
        self.root_logger.addHandler(session_handler)
        
        logger = self.get_logger("session")
        logger.info(f"📝 Session log created: {session_log_file}")
        return str(session_log_file)
    
    def cleanup_old_logs(self, days_to_keep: int = 30):
        """
        Clean up old log files manually.
        
        Args:
            days_to_keep: Number of days of logs to keep
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            deleted_count = 0
            for log_file in self.log_dir.glob("*.log*"):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    log_file.unlink()
                    deleted_count += 1
            
            logger = self.get_logger("cleanup")
            if deleted_count > 0:
                logger.info(f"🗑️  Cleaned up {deleted_count} old log files")
            else:
                logger.info("🗑️  No old log files to clean up")
                
        except Exception as e:
            logger = self.get_logger("cleanup")
            logger.error(f"❌ Failed to cleanup old logs: {e}")

# Global logger instance
automation_logger = AutomationLogger()

def setup_logging(log_level: str = "INFO", 
                 log_to_file: bool = True,
                 log_dir: Optional[Union[str, Path]] = None,
                 console_colors: bool = True) -> bool:
    """
    Convenience function to setup logging with default parameters.
    
    Args:
        log_level: Minimum logging level
        log_to_file: Enable file logging
        log_dir: Log directory path
        console_colors: Enable console colors
        
    Returns:
        bool: True if setup successful
    """
    return automation_logger.setup_logging(
        log_level=log_level,
        log_to_file=log_to_file,
        log_dir=log_dir,
        console_colors=console_colors
    )

def get_logger(name: Optional[str] = None):
    """
    Get configured logger instance.
    
    Args:
        name: Optional component name
        
    Returns:
        Logger instance
    """
    return automation_logger.get_logger(name)

# Convenience functions for specific log types
def log_action(action: str, details: str = "", success: bool = True):
    """Log automation action"""
    automation_logger.log_automation_action(action, details, success)

def log_performance(operation: str, duration: float, additional_info: str = ""):
    """Log performance metric"""
    automation_logger.log_performance_metric(operation, duration, additional_info)

def log_browser(event: str, url: str = "", details: str = ""):
    """Log browser event"""
    automation_logger.log_browser_event(event, url, details)

def log_mouse(event: str, coordinates: tuple = None, details: str = ""):
    """Log mouse event"""
    automation_logger.log_mouse_event(event, coordinates, details)

def log_detection(event: str, details: str = "", risk_level: str = "INFO"):
    """Log anti-detection event"""
    automation_logger.log_detection_event(event, details, risk_level)

# Example usage and testing
if __name__ == "__main__":
    # Test the logging system
    print("🧪 Testing logging system...")
    
    # Setup logging
    setup_logging(log_level="DEBUG", console_colors=True)
    
    # Test different log levels
    logger = get_logger("test")
    
    logger.debug("🔍 This is a debug message")
    logger.info("ℹ️  This is an info message")
    logger.warning("⚠️ This is a warning message")
    logger.error("❌ This is an error message")
    
    # Test specialized logging functions
    log_action("click", "Clicked on login button", success=True)
    log_action("type", "Typed username", success=False)
    log_performance("page_load", 2.34, "example.com loaded")
    log_browser("navigate", "https://example.com", "Navigation successful")
    log_mouse("click", (150, 200), "Left click in area")
    log_detection("randomization", "Added 3px offset to click", "INFO")
    
    print("✅ Logging system test completed!")