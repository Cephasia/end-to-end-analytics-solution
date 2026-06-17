"""
Configuration management for the analytics solution
"""

import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    """Load and manage configuration settings"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_path = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    @property
    def database(self) -> Dict[str, Any]:
        return self.config.get('database', {})
    
    @property
    def paths(self) -> Dict[str, str]:
        return self.config.get('paths', {})
    
    @property
    def processing(self) -> Dict[str, Any]:
        return self.config.get('processing', {})
    
    @property
    def visualization(self) -> Dict[str, Any]:
        return self.config.get('visualization', {})

# Global config instance
config = Config()
