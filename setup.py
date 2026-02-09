"""
Setup and validation for ┴ROOF Radio
Checks dependencies and environment before broadcast
"""

import sys
import json
from pathlib import Path


def load_config(config_path="config.json"):
    """
    Load configuration file
    
    Args:
        config_path: Path to config.json
    
    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)
    
    with open(config_file) as f:
        return json.load(f)


def validate_ollama_models():
    """
    Verify required Ollama models are available
    
    Returns:
        True if all models available, exits otherwise
    """
    try:
        import ollama
        response = ollama.list()
        
        # Extract model names from the ListResponse object
        model_names = []
        if hasattr(response, 'models'):
            # New Ollama library returns ListResponse with .models attribute
            for model in response.models:
                if hasattr(model, 'model'):
                    model_names.append(model.model)
        elif isinstance(response, dict):
            # Fallback for older versions that return dict
            for m in response.get('models', []):
                if isinstance(m, dict):
                    model_names.append(m.get('name', ''))
        
        required = ['deepseek-r1:14b', 'llama3.1:8b']
        missing = [m for m in required if m not in model_names]
        
        if missing:
            print(f"Error: Missing required Ollama models: {', '.join(missing)}")
            print("\nInstall them with:")
            for model in missing:
                print(f"  ollama pull {model}")
            sys.exit(1)
        
        return True
            
    except ImportError:
        print("Error: ollama Python package not found")
        print("Install with: pip install ollama")
        sys.exit(1)
    except Exception as e:
        print(f"Warning: Could not verify Ollama models: {e}")
        print("Attempting to continue anyway...")
        print("(Make sure deepseek-r1:14b and llama3.1:8b are installed)\n")
        return True


def parse_topic(args):
    """
    Parse topic from command line arguments
    
    Args:
        args: Command line arguments (sys.argv)
    
    Returns:
        Topic string
    """
    if len(args) < 2:
        print("Usage: python troof.py \"Your topic here\"")
        print("\nExample:")
        print("  python troof.py \"Are LLMs actually reasoning?\"")
        sys.exit(1)
    
    return " ".join(args[1:])
