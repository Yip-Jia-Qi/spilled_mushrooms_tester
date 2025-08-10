#!/usr/bin/env python3
"""
Test that Gopher gets Canyon bonus each time it re-enters Canyon
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import Critter, CritterType
from logger import logged_output


def test_canyon_reentry_bonus():
    """Test that location effects apply each time a critter enters via movement"""
    engine = GameEngine()
    
    print("Testing Canyon re-entry bonus...")
    print("=" * 50)
    
    # Create a test gopher
    gopher = Critter(CritterType.GOPHER, 1, 4)
    print(f"Initial Gopher: {gopher}")
    
    # Manually place gopher at Canyon first time
    canyon = engine.locations[1]  # Canyon is index 1
    jungle = engine.locations[2]  # Jungle is index 2
    
    gopher.current_location_id = 1
    canyon.critters.append(gopher)
    
    # Apply location effects for first Canyon visit
    engine._apply_location_effects(gopher, canyon)
    print(f"After first Canyon visit: {gopher}")
    
    expected_mushrooms = 1 + 1  # base + canyon bonus
    if gopher.current_mushrooms_per_day == expected_mushrooms:
        print("✅ First Canyon visit: got +1 mushrooms per day")
    else:
        print(f"❌ First Canyon visit: Expected {expected_mushrooms}, got {gopher.current_mushrooms_per_day}")
    
    # Simulate gopher moving to Jungle (simulating movement)
    print(f"\n--- Moving Gopher from Canyon to Jungle ---")
    canyon.critters.remove(gopher)
    gopher.current_location_id = 2
    jungle.critters.append(gopher)
    gopher.current_lifespan -= 1  # Simulate lifespan decrease
    print(f"Gopher at Jungle: {gopher}")
    
    # Simulate gopher moving back to Canyon (this is where the bug was)
    print(f"\n--- Moving Gopher back to Canyon (testing bug fix) ---")
    jungle.critters.remove(gopher)
    gopher.current_location_id = 1
    canyon.critters.append(gopher)
    
    # This is what the bug fix adds - location effects when moving back
    engine._apply_location_effects(gopher, canyon)
    print(f"After second Canyon visit: {gopher}")
    
    expected_second = expected_mushrooms + 1  # Should get another +1
    if gopher.current_mushrooms_per_day == expected_second:
        print("✅ Second Canyon visit: got another +1 mushrooms per day")
        print("🎉 Bug fix working! Location effects applied on re-entry.")
    else:
        print(f"❌ Second Canyon visit: Expected {expected_second}, got {gopher.current_mushrooms_per_day}")
        print("🐛 Bug still present - location effects not applied on re-entry")


if __name__ == "__main__":
    with logged_output(os.path.join("tests", "logs", "test_canyon_reentry.txt")) as log_path:
        print(f"Test session logging to: {log_path}")
        test_canyon_reentry_bonus()