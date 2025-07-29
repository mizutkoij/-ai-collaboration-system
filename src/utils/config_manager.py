#!/usr/bin/env python3
"""
Configuration Manager for AI Collaboration System
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union

class ConfigManager:
    """Manage configuration for AI Collaboration System"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_data = {}
        self.config_path = None
        
        # Default configuration
        self.defaults = {
            "system": {
                "auto_approve": True,
                "max_iterations": 20,
                "output_directory": "./generated_projects",
                "temp_directory": "./temp",
                "log_level": "INFO"
            },
            "ai": {
                "openai": {
                    "model": "gpt-4",
                    "max_tokens": 2000,
                    "temperature": 0.7
                },
                "anthropic": {
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 2000,
                    "temperature": 0.7
                }
            },
            "ui": {
                "theme": "dark",
                "show_progress": True,
                "auto_refresh": 2000,
                "port": 8080
            },
            "templates": {
                "design_template": "default",
                "project_templates": ["web_app", "api", "cli_tool"],
                "custom_templates_dir": "./templates/custom"
            },
            "file_generation": {
                "include_tests": True,
                "include_docs": True,
                "include_docker": True,
                "code_style": "black",
                "license": "MIT"
            }
        }
        
        # Load configuration
        if config_path:
            self.load_config(config_path)
        else:
            self._load_default_locations()
        
        # Merge with defaults
        self.config_data = self._merge_configs(self.defaults, self.config_data)

    def load_config(self, config_path: str) -> bool:
        """Load configuration from file"""
        path = Path(config_path)
        
        if not path.exists():
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix.lower() in ['.yml', '.yaml']:
                    self.config_data = yaml.safe_load(f)
                else:
                    self.config_data = json.load(f)
            
            self.config_path = path
            return True
        except Exception as e:
            print(f"Error loading config {config_path}: {e}")
            return False

    def _load_default_locations(self):
        """Try to load config from default locations"""
        default_locations = [
            "./config/ai_config.json",
            "./config/ai_config.yaml", 
            "./ai_config.json",
            "~/.ai_collaboration/config.json",
            os.getenv("AI_COLLAB_CONFIG", "")
        ]
        
        for location in default_locations:
            if location and self.load_config(os.path.expanduser(location)):
                break

    def _merge_configs(self, default: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge configuration dictionaries"""
        result = default.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        current = self.config_data
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current

    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        current = self.config_data
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value

    def get_ai_config(self, provider: str) -> Dict[str, Any]:
        """Get AI provider specific configuration"""
        config = self.get(f"ai.{provider}", {})
        
        # Add API key from environment
        api_key_env = f"{provider.upper()}_API_KEY"
        if api_key_env in os.environ:
            config["api_key"] = os.environ[api_key_env]
        
        return config

    def get_system_config(self) -> Dict[str, Any]:
        """Get system configuration"""
        return self.get("system", {})

    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration"""
        return self.get("ui", {})

    def save_config(self, path: Optional[str] = None) -> bool:
        """Save current configuration to file"""
        save_path = Path(path) if path else self.config_path
        
        if not save_path:
            save_path = Path.cwd() / "config" / "ai_config.json"
        
        # Ensure directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                if save_path.suffix.lower() in ['.yml', '.yaml']:
                    yaml.safe_dump(self.config_data, f, default_flow_style=False)
                else:
                    json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            self.config_path = save_path
            return True
        except Exception as e:
            print(f"Error saving config to {save_path}: {e}")
            return False

    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration"""
        issues = []
        warnings = []
        
        # Check required settings
        required_paths = [
            "system.output_directory",
            "ai.openai.model",
            "ai.anthropic.model"
        ]
        
        for path in required_paths:
            if self.get(path) is None:
                issues.append(f"Missing required setting: {path}")
        
        # Check API keys
        if not os.getenv("OPENAI_API_KEY"):
            warnings.append("OPENAI_API_KEY environment variable not set")
        
        if not os.getenv("ANTHROPIC_API_KEY"):
            warnings.append("ANTHROPIC_API_KEY environment variable not set")
        
        # Check directories
        output_dir = Path(self.get("system.output_directory", "./generated_projects"))
        if not output_dir.exists():
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create output directory: {e}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }

    def create_sample_config(self, path: str) -> bool:
        """Create a sample configuration file"""
        sample_config = {
            "system": {
                "auto_approve": True,
                "max_iterations": 20,
                "output_directory": "./generated_projects"
            },
            "ai": {
                "openai": {
                    "model": "gpt-4",
                    "max_tokens": 2000
                },
                "anthropic": {
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 2000
                }
            },
            "ui": {
                "theme": "dark",
                "show_progress": True,
                "auto_refresh": 2000
            }
        }
        
        try:
            path_obj = Path(path)
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path_obj, 'w', encoding='utf-8') as f:
                json.dump(sample_config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error creating sample config: {e}")
            return False

    def __str__(self) -> str:
        """String representation of configuration"""
        return f"ConfigManager(path={self.config_path}, keys={list(self.config_data.keys())})"

    def __repr__(self) -> str:
        return self.__str__()