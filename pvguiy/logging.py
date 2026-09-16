"""PVGUIY Logging System - Internal logging layer."""

import logging
from enum import IntEnum
from typing import Optional, List, Callable
from datetime import datetime


class LogLevel(IntEnum):
    """Log level enumeration."""
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Logger:
    """Internal PVGUIY logger."""
    
    _instance: Optional['Logger'] = None
    
    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._level = LogLevel.INFO
        self._handlers: List[Callable[[str, LogLevel], None]] = []
        self._console_handler: Optional[Callable] = None
        self._file_handler: Optional[str] = None
        
        # Set up Python logging
        self._logger = logging.getLogger('pvguiy')
        self._logger.setLevel(logging.DEBUG)
        
        self._initialized = True
    
    def set_level(self, level: LogLevel) -> 'Logger':
        self._level = level
        return self
    
    def add_handler(self, handler: Callable[[str, LogLevel], None]) -> 'Logger':
        self._handlers.append(handler)
        return self
    
    def set_console_handler(self, handler: Callable) -> 'Logger':
        self._console_handler = handler
        return self
    
    def set_file_handler(self, filepath: str) -> 'Logger':
        self._file_handler = filepath
        try:
            fh = logging.FileHandler(filepath)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)
        except IOError:
            pass
        return self
    
    def _log(self, message: str, level: LogLevel) -> None:
        if level < self._level:
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {self._level_name(level)}: {message}"
        
        # Call registered handlers
        for handler in self._handlers:
            try:
                handler(formatted, level)
            except:
                pass
        
        # Console handler
        if self._console_handler:
            try:
                self._console_handler(message, level)
            except:
                pass
        
        # Python logging
        py_level = self._to_python_level(level)
        self._logger.log(py_level, message)
    
    def _level_name(self, level: LogLevel) -> str:
        names = {
            LogLevel.DEBUG: "DEBUG",
            LogLevel.INFO: "INFO",
            LogLevel.SUCCESS: "SUCCESS",
            LogLevel.WARNING: "WARNING",
            LogLevel.ERROR: "ERROR",
            LogLevel.CRITICAL: "CRITICAL"
        }
        return names.get(level, "UNKNOWN")
    
    def _to_python_level(self, level: LogLevel) -> int:
        if level == LogLevel.SUCCESS:
            return logging.INFO
        return level
    
    def debug(self, message: str) -> None:
        self._log(message, LogLevel.DEBUG)
    
    def info(self, message: str) -> None:
        self._log(message, LogLevel.INFO)
    
    def success(self, message: str) -> None:
        self._log(message, LogLevel.SUCCESS)
    
    def warning(self, message: str) -> None:
        self._log(message, LogLevel.WARNING)
    
    def error(self, message: str) -> None:
        self._log(message, LogLevel.ERROR)
    
    def critical(self, message: str) -> None:
        self._log(message, LogLevel.CRITICAL)
    
    def clear_handlers(self) -> None:
        self._handlers.clear()
        self._console_handler = None


# Global logger instance
def get_logger() -> Logger:
    return Logger()


def debug(message: str) -> None:
    get_logger().debug(message)


def info(message: str) -> None:
    get_logger().info(message)


def success(message: str) -> None:
    get_logger().success(message)


def warning(message: str) -> None:
    get_logger().warning(message)


def error(message: str) -> None:
    get_logger().error(message)


def critical(message: str) -> None:
    get_logger().critical(message)
