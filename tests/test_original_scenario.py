#!/usr/bin/env python3
"""
Test the original scenario from game_run_20250810_132906.txt
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import Critter, CritterType
from logger import logged_output


def test_original_scenario():
    """Recreate the scenario: Gopher at Beach, Canyon full with 3 Geese, Jungle empty"""
    engine = GameEngine()
    
    print("Testing original scenario from game log...")
    print("=" * 45)
    
    # Recreate Day 6 scenario: Gopher(3/3) at Beach, Canyon full with Geese, Jungle empty  
    gopher = Critter(CritterType.GOPHER, 3, 3)  # Same stats as in log
    beach = engine.locations[0]  # Beach
    canyon = engine.locations[1]  # Canyon  
    jungle = engine.locations[2]  # Jungle
    
    # Place gopher at Beach
    gopher.current_location_id = 0
    beach.critters.append(gopher)
    print(f"Gopher at Beach: {gopher}")
    
    # Fill Canyon with 3 Geese (like in the log)
    for i in range(3):
        goose = Critter(CritterType.GOOSE, 2, 1)  # Goose(2/1) like in log
        goose.current_location_id = 1
        canyon.critters.append(goose)
    
    # Leave Jungle empty (like in the log)
    print(f"Canyon: {len(canyon.critters)} Geese (full)")
    print(f"Jungle: {len(jungle.critters)} critters (empty)")
    
    # Clear the queue to make sure Gopher can move
    engine.critter_queue.clear()
    print(f"Queue: {len(engine.critter_queue)}/8 (cleared for test)")
    
    # Apply end-of-day effects
    print(f"\n--- End of Day 6 → Day 7 ---")
    print("Expected: Gopher should move Beach → Canyon (full) → skip to Jungle")
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
        # Check queue
        for critter in engine.critter_queue:
            if critter.type == CritterType.GOPHER:
                print(f"❌ Gopher went to queue: {critter}")
                print("With the fix, it should have skipped to Jungle instead")
                return
        print("❌ Gopher completely disappeared!")
        return
    
    print(f"Result: Gopher moved to {location_name}: {gopher_found}")
    
    if location_id == 2:  # Jungle
        print("✅ SUCCESS! Gopher correctly skipped full Canyon and moved to Jungle")
        print("🎉 This fixes the original disappearance bug!")
    elif location_id == 0:  # Beach
        print("❌ Gopher stayed at Beach - something went wrong")
    elif location_id == 1:  # Canyon
        print("❌ Gopher somehow moved to full Canyon - this shouldn't happen")


if __name__ == "__main__":
    with logged_output(os.path.join("tests", "logs", "test_original_scenario.txt")) as log_path:
        print(f"Test session logging to: {log_path}")
        test_original_scenario()