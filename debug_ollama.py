#!/usr/bin/env python3
"""
Debug script to see what ollama.list() actually returns
"""

import ollama
import json

print("Testing ollama.list() response format...")
print()

try:
    response = ollama.list()
    print("Type of response:", type(response))
    print()
    print("Full response:")
    print(json.dumps(response, indent=2, default=str))
    print()
    
    # Try to extract models
    if hasattr(response, 'models'):
        print("Has .models attribute")
        print("Models:", response.models)
    
    if isinstance(response, dict):
        print("\nIt's a dict with keys:", response.keys())
        if 'models' in response:
            print("\nModels list:")
            for m in response['models']:
                print(f"  Type: {type(m)}")
                print(f"  Content: {m}")
                if hasattr(m, '__dict__'):
                    print(f"  Dict: {m.__dict__}")
                print()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
