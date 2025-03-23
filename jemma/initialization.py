import tomli_w
from pathlib import Path
import sys

CONFIG_PATH = Path.home() / ".jemma-config.toml"

if CONFIG_PATH.exists():
        confirm = input("⚠️  Existing configuration found. Overwrite? [y/N] ").lower()
        if confirm != "y":
            print("Aborting configuration")
            sys.exit(0)
            

def initialize_jemma():
    """Interactive configuration setup for Jemma AI assistant"""
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

    print("\n✨ Welcome to Jemma Setup! ✨\n")
    
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
            print(f"⚠️  Invalid choice '{choice}'. Please enter 1 or 2\n")

    # Additional Configuration
    print("\n🔧 Optional Advanced Settings (press Enter to use defaults)")
    try:
        temp = float(input(f"Temperature ({config['settings']['temperature']}): ") 
                  or config['settings']['temperature'])
        config['settings']['temperature'] = max(0.0, min(1.0, temp))
    except:
        pass

    # Save Configuration
    try:
        with CONFIG_PATH.open("wb") as f:
            tomli_w.dump(config, f)
        print(f"\n✅ Configuration saved to {CONFIG_PATH}")
    except Exception as e:
        print(f"\n❌ Failed to save configuration: {str(e)}")
        sys.exit(1)



