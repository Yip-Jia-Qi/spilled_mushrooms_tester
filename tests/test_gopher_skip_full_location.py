#!/usr/bin/env python3
"""
Test that Gopher skips full locations during movement
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import Critter, CritterType
from logger import logged_output


def test_gopher_skip_full_location():
    """Test that Gopher skips full Canyon and goes to Jungle"""
    engine = GameEngine()
    
    print("Testing Gopher skipping full location...")
    print("=" * 50)
    
    # Create test scenario: Gopher at Beach, Canyon is full
    gopher = Critter(CritterType.GOPHER, 1, 4)
    beach = engine.locations[0]  # Beach
    canyon = engine.locations[1]  # Canyon  
    jungle = engine.locations[2]  # Jungle
    
    # Place gopher at Beach
    gopher.current_location_id = 0
    beach.critters.append(gopher)
    print(f"Gopher placed at Beach: {gopher}")
    
    # Fill Canyon with dummy critters to make it full
    for i in range(3):  # Canyon capacity is 3
        dummy = Critter(CritterType.GOOSE, 1, 2)
        dummy.current_location_id = 1
        canyon.critters.append(dummy)
    
    print(f"Canyon filled: {len(canyon.critters)}/3 critters")
    print(f"Canyon is full: {canyon.is_full()}")
    print(f"Jungle is full: {jungle.is_full()}")
    
    # Apply end-of-day effects (Gopher should skip Canyon and go to Jungle)
    print(f"\n--- Applying end-of-day effects ---")
    print("Gopher should move: Beach -> Canyon (full) -> skip to Jungle")
    engine._apply_end_of_day_effects()
    
    # Check where the gopher ended up
    gopher_found = None
    location_name = None
    location_id = None
    
    for i, location in enumerate(engine.locations):
        for critter in location.critters:
            if critter.type == CritterType.GOPHER:
                gopher_found = critter
                location_name = location.type.value
                location_id = i
                break
        if gopher_found:
            break
    
    if gopher_found is None:
        print("❌ Gopher not found in any location!")
        # Check queue
        print("Checking queue:")
        for i, critter in enumerate(engine.critter_queue):
            if critter.type == CritterType.GOPHER:
                print(f"  Found Gopher in queue: {critter}")
                print("⚠️  Gopher went to queue instead of skipping to Jungle")
                return
        print("❌ Gopher completely disappeared!")
        return
    
    print(f"Gopher after movement: {gopher_found} at {location_name} (location {location_id})")
    
    if location_id == 2:  # Jungle
        print("✅ Success! Gopher skipped full Canyon and moved to Jungle")
        print("🎉 Bug fix working! Gopher can skip full locations.")
    elif location_id == 1:  # Canyon
        print("❌ Gopher somehow moved to Canyon even though it was full")
    elif location_id == 0:  # Beach  
        print("⚠️  Gopher stayed at Beach (couldn't move anywhere)")
    else:
        print(f"❌ Gopher moved to unexpected location: {location_name}")


if __name__ == "__main__":
    with logged_output(os.path.join("tests", "logs", "test_gopher_skip_full_location.txt")) as log_path:
        print(f"Test session logging to: {log_path}")
        test_gopher_skip_full_location()