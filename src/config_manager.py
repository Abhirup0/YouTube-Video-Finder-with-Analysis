"""
Configuration manager for YouTube Video Finder
Handles loading API keys and other configuration data
"""
import os
import json
import sys

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                         "config", "config.json")

def load_config():
    """
    Load configuration from config.json file
    Returns a dictionary with configuration values or None if configuration failed
    """
    try:
        if not os.path.exists(CONFIG_FILE):
            # Create default config if it doesn't exist
            default_config = {
                "youtube_api_key": "",
                "gemini_api_key": ""
            }
            
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
                
            print(f"Created default config file at {CONFIG_FILE}")
            print("Please fill in your API keys in the config file and run the program again.")
            return None
            
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            
        # Verify required keys exist
        required_keys = ["youtube_api_key", "gemini_api_key"]
        missing_keys = [key for key in required_keys if not config.get(key)]
        
        if missing_keys:
            print(f"Missing required configuration keys: {', '.join(missing_keys)}")
            print(f"Please update your config file at {CONFIG_FILE}")
            return None
            
        return config
        
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None 