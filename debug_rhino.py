#!/usr/bin/env python3
"""
Debug Rhino placement effect
"""

from game_engine import GameEngine
from models import CritterType
from collections import deque


def debug_rhino_effect():
    """Debug Rhino getting buff when another critter enters"""
    print("Debugging Rhino placement effect...")
    
    # Create a simple test case
    engine = GameEngine()
    
    # Set up a specific scenario: Rhino already at Beach
    from models import Critter, Location, LocationType
    rhino = Critter(CritterType.RHINO, 1, 4)
    gopher = Critter(CritterType.GOPHER, 1, 4) 
    frog = Critter(CritterType.FROG, 1, 5)
    
    # Clear existing setup and create controlled test
    engine.locations[0].critters = [rhino]  # Put Rhino at Beach
    rhino.current_location_id = 0
    engine.critter_queue = deque([gopher, frog])
    
    print(f"Initial state:")
    print(f"Beach critters: {[str(c) for c in engine.locations[0].critters]}")
    print(f"Rhino stats before: {rhino}")
    print(f"Next critter to place: {gopher}")
    
    # Send Gopher to Beach (where Rhino already is)
    print(f"\nSending Gopher to Beach...")
    engine.process_turn(0, 0)  # First critter (Gopher), first location (Beach)
    
    print(f"Beach critters after: {[str(c) for c in engine.locations[0].critters]}")
    
    # Find the rhino in the location and check its stats
    beach_rhino = None
    for critter in engine.locations[0].critters:
        if critter.type == CritterType.RHINO:
            beach_rhino = critter
            break
    
    if beach_rhino:
        print(f"Rhino stats after Gopher enters: {beach_rhino}")
        expected_mushrooms = 1 + 1  # base + buff from Gopher entering
        if beach_rhino.current_mushrooms_per_day == expected_mushrooms:
            print("✅ Rhino correctly got +1 mushrooms per day")
        else:
            print(f"❌ Rhino should have {expected_mushrooms} mushrooms per day, but has {beach_rhino.current_mushrooms_per_day}")
    else:
        print("❌ Rhino not found at Beach")


def debug_rhino_with_penguin():
    """Debug Rhino effect when Penguin enters (should swap to lifespan)"""
    print(f"\n{'='*50}")
    print("Debugging Rhino + Penguin interaction...")
    
    engine = GameEngine()
    
    # Set up: Rhino at Canyon, Penguin entering
    from models import Critter, Location, LocationType
    rhino = Critter(CritterType.RHINO, 1, 4)
    penguin = Critter(CritterType.PENGUIN, 2, 3)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.locations[1].critters = [rhino]  # Put Rhino at Canyon
    rhino.current_location_id = 1
    engine.critter_queue = deque([penguin, frog])
    
    print(f"Initial state:")
    print(f"Canyon critters: {[str(c) for c in engine.locations[1].critters]}")
    print(f"Rhino stats before: {rhino}")
    print(f"Next critter to place: {penguin}")
    
    # Send Penguin to Canyon
    print(f"\nSending Penguin to Canyon...")
    engine.process_turn(0, 1)  # First critter (Penguin), Canyon location
    
    print(f"Canyon critters after: {[str(c) for c in engine.locations[1].critters]}")
    
    # Check Rhino stats
    canyon_rhino = None
    for critter in engine.locations[1].critters:
        if critter.type == CritterType.RHINO:
            canyon_rhino = critter
            break
    
    if canyon_rhino:
        print(f"Rhino stats after Penguin enters: {canyon_rhino}")
        expected_lifespan = 4 + 1  # base + swapped buff from Penguin entering
        if canyon_rhino.current_lifespan == expected_lifespan:
            print("✅ Rhino correctly got +1 lifespan (swapped by Penguin)")
        else:
            print(f"❌ Rhino should have {expected_lifespan} lifespan, but has {canyon_rhino.current_lifespan}")


if __name__ == "__main__":
    debug_rhino_effect()
    debug_rhino_with_penguin()