import os
from pathlib import Path

def configure_api_key():
    """Interactive configuration of the Gemini API key."""
    api_key = input("Enter your Gemini API key: ").strip()
    
    if api_key:
        # Create config directory if it doesn't exist
        config_dir = Path.home() / ".autodoc"
        os.makedirs(config_dir, exist_ok=True)
        
        # Write API key to config file
        with open(config_dir / "config", "w") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        
        print(f"API key saved to {config_dir}/config")
        return True
    else:
        print("No API key provided. Configuration cancelled.")
        return False

if __name__ == "__main__":
    configure_api_key()