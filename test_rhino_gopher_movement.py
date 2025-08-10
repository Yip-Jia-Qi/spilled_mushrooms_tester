#!/usr/bin/env python3
"""
Test that Rhino gets buffed when Gopher moves to its location
"""

from game_engine import GameEngine
from models import Critter, CritterType, LocationType
from collections import deque


def test_rhino_gopher_movement():
    """Test Rhino gets buff when Gopher moves to same location"""
    print("Testing Rhino effect on Gopher movement...")
    
    engine = GameEngine()
    
    # Set up scenario:
    # - Rhino at Beach (location 0)
    # - Gopher at Jungle (location 2) - will move to Beach (location 0) at end of day
    rhino = Critter(CritterType.RHINO, 1, 4)
    gopher = Critter(CritterType.GOPHER, 1, 4)
    frog = Critter(CritterType.FROG, 1, 5)
    
    # Manual setup
    engine.locations[0].critters = [rhino]  # Rhino at Beach
    rhino.current_location_id = 0
    
    engine.locations[2].critters = [gopher]  # Gopher at Jungle  
    gopher.current_location_id = 2
    
    engine.critter_queue = deque([frog])
    
    print("Initial setup:")
    print(f"  Beach: {[str(c) for c in engine.locations[0].critters]}")
    print(f"  Canyon: {[str(c) for c in engine.locations[1].critters]}")
    print(f"  Jungle: {[str(c) for c in engine.locations[2].critters]}")
    print(f"  Rhino stats: {rhino}")
    
    print(f"\nApplying end-of-day effects (Gopher should move from Jungle to Beach)...")
    engine._apply_end_of_day_effects()
    
    print("After Gopher movement:")
    print(f"  Beach: {[str(c) for c in engine.locations[0].critters]}")
    print(f"  Canyon: {[str(c) for c in engine.locations[1].critters]}")
    print(f"  Jungle: {[str(c) for c in engine.locations[2].critters]}")
    
    # Check if Rhino got buffed
    beach_rhino = None
    for critter in engine.locations[0].critters:
        if critter.type == CritterType.RHINO:
            beach_rhino = critter
            break
    
    if beach_rhino:
        print(f"  Rhino stats after Gopher enters: {beach_rhino}")
        expected_mushrooms = 1 + 1  # base + buff from Gopher entering
        if beach_rhino.current_mushrooms_per_day == expected_mushrooms:
            print("✅ Rhino correctly got +1 mushrooms per day when Gopher moved to Beach")
        else:
            print(f"❌ Rhino should have {expected_mushrooms} mushrooms per day, but has {beach_rhino.current_mushrooms_per_day}")
    else:
        print("❌ Rhino not found at Beach")


def test_sheep_gopher_movement():
    """Test Sheep gets buff when Gopher moves to same location"""
    print(f"\n{'='*60}")
    print("Testing Sheep effect on Gopher movement...")
    
    engine = GameEngine()
    
    # Set up scenario: Sheep at Canyon, Gopher at Beach (will move to Canyon)
    sheep = Critter(CritterType.SHEEP, 1, 4)
    gopher = Critter(CritterType.GOPHER, 1, 4)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.locations[1].critters = [sheep]  # Sheep at Canyon
    sheep.current_location_id = 1
    
    engine.locations[0].critters = [gopher]  # Gopher at Beach
    gopher.current_location_id = 0
    
    engine.critter_queue = deque([frog])
    
    print("Initial setup:")
    print(f"  Beach: {[str(c) for c in engine.locations[0].critters]}")
    print(f"  Canyon: {[str(c) for c in engine.locations[1].critters]}")
    print(f"  Sheep stats: {sheep}")
    
    print(f"\nApplying end-of-day effects (Gopher should move from Beach to Canyon)...")
    engine._apply_end_of_day_effects()
    
    print("After Gopher movement:")
    print(f"  Beach: {[str(c) for c in engine.locations[0].critters]}")
    print(f"  Canyon: {[str(c) for c in engine.locations[1].critters]}")
    
    # Check if Sheep got buffed
    canyon_sheep = None
    for critter in engine.locations[1].critters:
        if critter.type == CritterType.SHEEP:
            canyon_sheep = critter
            break
    
    if canyon_sheep:
        print(f"  Sheep stats after Gopher enters: {canyon_sheep}")
        expected_lifespan = 4 + 1  # base + buff from Gopher entering
        if canyon_sheep.current_lifespan == expected_lifespan:
            print("✅ Sheep correctly got +1 lifespan when Gopher moved to Canyon")
        else:
            print(f"❌ Sheep should have {expected_lifespan} lifespan, but has {canyon_sheep.current_lifespan}")
    else:
        print("❌ Sheep not found at Canyon")


if __name__ == "__main__":
    test_rhino_gopher_movement()
    test_sheep_gopher_movement()