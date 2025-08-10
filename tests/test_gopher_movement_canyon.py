#!/usr/bin/env python3
"""
Test Gopher automatic movement and Canyon bonus interaction
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import Critter, CritterType
from logger import logged_output


def test_gopher_movement_canyon():
    """Test that Gopher gets Canyon bonus when it automatically moves to Canyon"""
    engine = GameEngine()
    
    print("Testing Gopher automatic movement with Canyon bonus...")
    print("=" * 60)
    
    # Create and place a gopher at Beach (so it will move to Canyon next)
    gopher = Critter(CritterType.GOPHER, 1, 4)
    beach = engine.locations[0]
    canyon = engine.locations[1]
    
    # Place gopher at Beach
    gopher.current_location_id = 0
    beach.critters.append(gopher)
    print(f"Gopher placed at Beach: {gopher}")
    
    # Apply end-of-day effects (should move Gopher from Beach to Canyon)
    print(f"\n--- Applying end-of-day effects (Gopher should move Beach -> Canyon) ---")
    engine._apply_end_of_day_effects()
    
    # Check where the gopher ended up
    gopher_found = None
    location_name = None
    for i, location in enumerate(engine.locations):
        for critter in location.critters:
            if critter.type == CritterType.GOPHER:
                gopher_found = critter
                location_name = location.type.value
                break
        if gopher_found:
            break
    
    if gopher_found is None:
        print("❌ Gopher not found after movement!")
        return
    
    print(f"Gopher after movement: {gopher_found} at {location_name}")
    
    if gopher_found.current_location_id == 1:  # Canyon
        expected_mushrooms = 1 + 1  # base + canyon bonus
        if gopher_found.current_mushrooms_per_day == expected_mushrooms:
            print("✅ Gopher moved to Canyon and got +1 mushrooms per day bonus")
            print("🎉 Bug fix working! Automatic movement triggers location effects.")
        else:
            print(f"❌ Gopher at Canyon but mushrooms wrong: Expected {expected_mushrooms}, got {gopher_found.current_mushrooms_per_day}")
            print("🐛 Bug present - automatic movement not triggering location effects")
    else:
        print(f"❌ Gopher moved to unexpected location: {location_name} (index {gopher_found.current_location_id})")


if __name__ == "__main__":
    with logged_output(os.path.join("tests", "logs", "test_gopher_movement_canyon.txt")) as log_path:
        print(f"Test session logging to: {log_path}")
        test_gopher_movement_canyon()