"""PVGUIY Configuration System - JSON-based settings."""

import json
from typing import Any, Optional, Dict
from pathlib import Path


class Config:
    """Configuration manager using JSON files."""
    
    def __init__(self, filepath: str):
        self._filepath = Path(filepath)
        self._data: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> 'Config':
        """Load configuration from file."""
        if self._filepath.exists():
            try:
                with open(self._filepath, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = {}
        return self
    
    def save(self) -> bool:
        """Save configuration to file."""
        try:
            self._filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by dot-separated key."""
        keys = key.split('.')
        value = self._data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> 'Config':
        """Set a configuration value by dot-separated key."""
        keys = key.split('.')
        data = self._data
        
        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]
        
        data[keys[-1]] = value
        return self
    
    def remove(self, key: str) -> 'Config':
        """Remove a configuration value."""
        keys = key.split('.')
        data = self._data
        
        for k in keys[:-1]:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return self
        
        if isinstance(data, dict) and keys[-1] in data:
            del data[keys[-1]]
        
        return self
    
    def exists(self, key: str) -> bool:
        """Check if a configuration key exists."""
        return self.get(key, None) is not None
    
    def clear(self) -> 'Config':
        """Clear all configuration."""
        self._data = {}
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return dict(self._data)
    
    def from_dict(self, data: Dict[str, Any]) -> 'Config':
        """Load configuration from dictionary."""
        self._data = dict(data)
        return self
    
    def keys(self) -> list:
        """Get top-level keys."""
        return list(self._data.keys())
    
    def __getitem__(self, key: str) -> Any:
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        return self.exists(key)
