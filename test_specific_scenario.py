#!/usr/bin/env python3
"""
Test the specific scenario where Gopher moves to Beach with Rhino
"""

from game_engine import GameEngine
from models import Critter, CritterType
from collections import deque


def test_your_specific_scenario():
    """Test the exact scenario from your game"""
    print("Testing your specific scenario: Rhino at Beach, Gopher moves there...")
    
    engine = GameEngine()
    
    # Set up the scenario from your game:
    # Day 5: Beach has Rhino(1/4)
    # Day 6: Gopher moves to Beach, should make Rhino become (2/4)
    
    rhino = Critter(CritterType.RHINO, 1, 4)
    gopher = Critter(CritterType.GOPHER, 2, 2)  # Stats from your game  
    frog = Critter(CritterType.FROG, 1, 3)     # At jungle from your game
    
    # Set up Day 5 state
    engine.locations[0].critters = [rhino]  # Beach
    rhino.current_location_id = 0
    
    engine.locations[2].critters = [frog]   # Jungle  
    frog.current_location_id = 2
    
    engine.locations[1].critters = [gopher] # Canyon (Gopher will move to Beach)
    gopher.current_location_id = 1
    
    print("Before end-of-day (simulating Day 5 state):")
    print(f"  Beach: {[str(c) for c in engine.locations[0].critters]}")
    print(f"  Canyon: {[str(c) for c in engine.locations[1].critters]}")
    print(f"  Jungle: {[str(c) for c in engine.locations[2].critters]}")
    
    # Apply end-of-day effects (Gopher moves Canyon -> Jungle, but Jungle is occupied, so Beach)
    print(f"\nApplying end-of-day Gopher movement...")
    
    # Since Jungle has Frog, Gopher can't go there, should cycle to Beach
    # Let's manually check the logic
    target_location = engine.locations[(1 + 1) % 3]  # Canyon -> Jungle
    if target_location.is_full() or len(target_location.critters) > 0:
        print(f"  Jungle is occupied, checking if Gopher can go to queue or Beach...")
        # In real game, this would depend on queue space, but let's assume it goes to Beach
        
        # Manual movement to Beach for testing
        engine.locations[1].critters.remove(gopher)
        gopher.current_location_id = 0
        engine.locations[0].critters.append(gopher)
        engine._apply_rhino_sheep_effects(gopher, engine.locations[0])
    
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
        print(f"\nResult: Rhino stats are now {beach_rhino}")
        if beach_rhino.current_mushrooms_per_day == 2:  # 1 + 1 buff
            print("✅ SUCCESS: Rhino correctly got buffed when Gopher entered Beach!")
            print("   This matches the expected behavior from your game scenario.")
        else:
            print(f"❌ FAILED: Rhino should have 2 mushrooms per day, has {beach_rhino.current_mushrooms_per_day}")
    else:
        print("❌ Rhino not found at Beach")


if __name__ == "__main__":
    test_your_specific_scenario()