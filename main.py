#!/usr/bin/env python3
"""
Spilled Mushrooms - A card puzzle game about delivering mushrooms

Run this file to start playing the game.
"""

import sys
import os
from game_ui import GameUI
from logger import logged_output


def main():
    """Main entry point for the game"""
    config = None
    
    # Check for config file argument
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        if os.path.exists(config_path):
            config = config_path
            print(f"Loading configuration from: {config_path}")
        else:
            print(f"Config file not found: {config_path}")
            print("Using default configuration...")
    
    with logged_output() as log_path:
        print(f"Game session logging to: {log_path}")
        try:
            game = GameUI(config)
            game.play_game()
        except KeyboardInterrupt:
            print("\n\nThanks for playing Spilled Mushrooms!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please report this bug!")


if __name__ == "__main__":
    main()