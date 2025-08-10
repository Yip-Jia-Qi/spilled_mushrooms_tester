#!/usr/bin/env python3
"""
Test the configuration system
"""


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import ConfigManager, GameConfig
from game_engine import GameEngine
from models import CritterType


def test_config_loading():
    """Test loading configurations from files"""
    print("Testing configuration loading...")
    
    # Test loading each example config
    configs = ["balanced", "high_damage", "support", "easy"]
    
    for config_name in configs:
        print(f"\n--- Testing {config_name} config ---")
        config_path = f"configs/{config_name}.json"
        
        try:
            # Load config
            config = ConfigManager.load_config(config_path)
            print(f"Loaded config with {len(config.critters)} critters")
            
            # Create game with config
            engine = GameEngine(config_path)
            state = engine.get_game_state()
            
            print(f"Game initialized - Day: {state['day']}, Total mushrooms: {state['total_mushrooms']}")
            
            # Show critters
            print("Critters in queue:")
            for i, critter in enumerate(state['queue']):
                print(f"  {i+1}. {critter}")
            
            # Show locations
            print("Locations:")
            for location in state['locations']:
                print(f"  {location}")
                
        except Exception as e:
            print(f"Error testing {config_name}: {e}")


def test_custom_config():
    """Test creating and using custom configurations"""
    print("\n" + "="*50)
    print("Testing custom configuration creation...")
    
    # Create a custom config programmatically
    custom_config = GameConfig(
        critters=["crocodile", "crocodile", "penguin", "penguin", "rhino", "rhino", "sheep", "sheep"],
        locations=[
            {"type": "beach", "mushrooms": 12},
            {"type": "canyon", "mushrooms": 15},
            {"type": "jungle", "mushrooms": 8}
        ]
    )
    
    # Save it
    ConfigManager.save_config(custom_config, "configs/test_custom.json")
    
    # Load and test it
    engine = GameEngine("configs/test_custom.json")
    state = engine.get_game_state()
    
    print(f"Custom game initialized - Day: {state['day']}, Total mushrooms: {state['total_mushrooms']}")
    
    print("Custom critters:")
    for critter in state['queue']:
        print(f"  {critter}")
    
    print("Custom locations:")
    for location in state['locations']:
        print(f"  {location}")


def test_config_vs_default():
    """Compare configured game vs default game"""
    print("\n" + "="*50)
    print("Comparing configured vs default games...")
    
    # Default game
    default_engine = GameEngine()
    default_state = default_engine.get_game_state()
    
    # Configured game
    config_engine = GameEngine("configs/balanced.json")
    config_state = config_engine.get_game_state()
    
    print(f"Default total mushrooms: {default_state['total_mushrooms']}")
    print(f"Balanced config total mushrooms: {config_state['total_mushrooms']}")
    
    print(f"\nDefault first 2 critters:")
    for critter in default_state['queue']:
        print(f"  {critter}")
    
    print(f"\nBalanced config first 2 critters:")  
    for critter in config_state['queue']:
        print(f"  {critter}")


if __name__ == "__main__":
    test_config_loading()
    test_custom_config()
    test_config_vs_default()
    print("\nConfiguration system testing completed!")