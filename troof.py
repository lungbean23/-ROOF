#!/usr/bin/env python3
"""
┴ROOF Radio - Truth with a speech impediment
An infinite AI conversation where Goku and Homer seek truth together
"""

import sys
from setup import load_config, validate_ollama_models, parse_topic
from log_cleanup import clean_logs, create_current_session_marker
from broadcast import TroofRadio


def main():
    """CLI entry point"""
    
    # Parse command line
    topic = parse_topic(sys.argv)
    
    # Clean old logs
    clean_logs()
    create_current_session_marker()
    
    # Validate environment
    validate_ollama_models()
    
    # Load configuration
    config = load_config()
    
    # Start the broadcast
    radio = TroofRadio(config)
    radio.broadcast(topic)


if __name__ == "__main__":
    main()
