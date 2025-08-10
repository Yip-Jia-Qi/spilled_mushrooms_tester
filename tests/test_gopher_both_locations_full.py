#!/usr/bin/env python3
"""
Test Gopher behavior when both next and skip locations are full
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import Critter, CritterType
from logger import logged_output


def test_gopher_both_locations_full():
    """Test Gopher goes to queue when both Canyon and Jungle are full"""
    engine = GameEngine()
    
    print("Testing Gopher when both next locations are full...")
    print("=" * 55)
    
    # Create test scenario: Gopher at Beach, both Canyon and Jungle are full
    gopher = Critter(CritterType.GOPHER, 1, 4)
    beach = engine.locations[0]  # Beach
    canyon = engine.locations[1]  # Canyon  
    jungle = engine.locations[2]  # Jungle
    
    # Place gopher at Beach
    gopher.current_location_id = 0
    beach.critters.append(gopher)
    print(f"Gopher placed at Beach: {gopher}")
    
    # Fill both Canyon and Jungle
    for i in range(3):  # Fill Canyon
        dummy = Critter(CritterType.GOOSE, 1, 2)
        dummy.current_location_id = 1
        canyon.critters.append(dummy)
        
    for i in range(3):  # Fill Jungle
        dummy = Critter(CritterType.CROCODILE, 3, 2)
        dummy.current_location_id = 2
        jungle.critters.append(dummy)
    
    print(f"Canyon filled: {len(canyon.critters)}/3 critters")
    print(f"Jungle filled: {len(jungle.critters)}/3 critters")
    print(f"Canyon is full: {canyon.is_full()}")
    print(f"Jungle is full: {jungle.is_full()}")
    print(f"Current queue size: {len(engine.critter_queue)}/8")
    
    # Apply end-of-day effects (Gopher should go to queue)
    print(f"\n--- Applying end-of-day effects ---")
    print("Gopher should try: Beach -> Canyon (full) -> Jungle (full) -> queue")
    engine._apply_end_of_day_effects()
    
    print(f"After movement, queue size: {len(engine.critter_queue)}/8")
    
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
    
    if gopher_found is not None:
        print(f"❌ Gopher found at {location_name}: {gopher_found}")
        print("Expected: Gopher should be in queue, not at a location")
        return
    
    # Check queue
    gopher_in_queue = None
    for critter in engine.critter_queue:
        if critter.type == CritterType.GOPHER:
            gopher_in_queue = critter
            break
    
    if gopher_in_queue:
        print(f"✅ Success! Gopher moved to queue: {gopher_in_queue}")
        print("🎉 Correct behavior when both locations are full!")
    else:
        print("❌ Gopher disappeared completely!")


if __name__ == "__main__":
    with logged_output(os.path.join("tests", "logs", "test_gopher_both_locations_full.txt")) as log_path:
        print(f"Test session logging to: {log_path}")
        test_gopher_both_locations_full()