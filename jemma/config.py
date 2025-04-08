 
from pathlib import Path
import sys
from jemma.utils.terminalPrettifier import successText, errorText

import json
 
from typing import Dict, Any

class JemmaConfig:
    _instance = None
    _config: Dict[str, Any] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JemmaConfig, cls).__new__(cls)
            cls._load_config()
        return cls._instance
    
    @classmethod
    def _load_config(cls):
        """Load config once per session"""
        config_path = Path.home() / ".jemma" / "config.json"
        try:
            with open(config_path, 'r') as f:
                cls._config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            cls._config = {
                'model': 'gemini-2.0-flash',  # Default fallback
                'settings': {
                    'temperature': 0.7,
                    'max_tokens': 2048
                }
            }
    
    @property
    def model(self) -> str:
        return self._config.get('model', 'gemini-2.0-flash')
    
    @property
    def temperature(self) -> float:
        return self._config.get('settings', {}).get('temperature', 0.7)
    
    @property
    def api_base(self) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}"

# Global configuration instance
CONFIG = JemmaConfig()

def configure_jemma():
    """Interactive configuration setup for Jemma AI assistant"""
    CONFIG_PATH = Path.home() / ".jemma" /  "config.json"
    
    # Check for existing configuration
    if CONFIG_PATH.exists():
        confirm = input("⚠️ Existing configuration found. Overwrite? [y/N] ").lower()
        if confirm != "y":
            print("Aborting configuration")
            sys.exit(0)
    
    # Default configuration
    config = {
        "model": None,
        "settings": {
            "temperature": 0.7,
            "max_tokens": 2048,
            "safety_settings": {
                "harassment": "block_only_high",
                "dangerous": "block_medium_and_above"
            }
        }
    }
    
    print(successText("\n✨ Welcome to Jemma Setup! ✨\n"))
    
    # Model Selection
    while True:
        print("Choose your preferred model:")
        print("1. Gemini 2.0 (Higher quality)")
        print("2. Gemini 2.0 Flash (Faster responses)")
        choice = input("> ").strip()
        
        if choice == "1":
            config["model"] = "gemini-2.0"
            break
        elif choice == "2":
            config["model"] = "gemini-2.0-flash"
            break
        else:
            print(errorText(f"⚠️ Invalid choice '{choice}'. Please enter 1 or 2\n"))
    
    # Additional Configuration
    print("\n🔧 Optional Advanced Settings (press Enter to use defaults)")
    
    # Temperature setting
    try:
        temp_input = input(f"Temperature ({config['settings']['temperature']}): ")
        if temp_input:
            temp = float(temp_input)
            config['settings']['temperature'] = max(0.0, min(1.0, temp))
    except ValueError:
        print(errorText("Invalid temperature value. Using default."))
    
    # Max tokens setting
    try:
        tokens_input = input(f"Max tokens ({config['settings']['max_tokens']}): ")
        if tokens_input:
            tokens = int(tokens_input)
            config['settings']['max_tokens'] = max(1, tokens)
    except ValueError:
        print(errorText("Invalid max tokens value. Using default."))
    
    # Save Configuration
    try:
        # Use json.dump with indentation for readability
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        
        # Verify the file was created
        if CONFIG_PATH.exists() and CONFIG_PATH.stat().st_size > 0:
            print(successText(f"\n✅ Configuration saved to {CONFIG_PATH}"))
            print(f"Your Jemma AI assistant is now configured to use {config['model']}")
            return True
        else:
            print(errorText("\n❌ Configuration file appears to be empty or not created"))
            return False
    except Exception as e:
        print(errorText(f"\n❌ Failed to save configuration: {str(e)}"))
        sys.exit(1)

def load_config():
    """Load existing configuration"""
    CONFIG_PATH = Path.home() / ".jemma-config.json"
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(errorText("No configuration found. Please run jemma-configure and jemma -init first."))
        return None
    except json.JSONDecodeError:
        print(errorText("Configuration file is corrupted. Please reconfigure."))
        return None

if __name__ == "__main__":
    initialize_jemma()