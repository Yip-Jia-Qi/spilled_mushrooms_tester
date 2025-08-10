#!/usr/bin/env python3
"""
Test that Goose duplicates get location and placement effects
"""


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import Critter, CritterType, LocationType
from collections import deque


def test_goose_canyon_effects():
    """Test Goose duplicates get Canyon location effects"""
    print("Testing Goose duplicates get Canyon effects...")
    
    engine = GameEngine()
    
    # Set up: Empty Canyon, place Goose there
    goose = Critter(CritterType.GOOSE, 1, 2)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.critter_queue = deque([goose, frog])
    
    print("Before placing Goose at Canyon:")
    print(f"  Canyon: {[str(c) for c in engine.locations[1].critters]}")
    print(f"  Goose base stats: {goose}")
    
    # Place Goose at Canyon (location 1)
    engine.process_turn(0, 1)
    
    print("After placing Goose at Canyon:")
    print(f"  Canyon: {[str(c) for c in engine.locations[1].critters]}")
    
    # Check all geese in canyon
    canyon_geese = engine.locations[1].critters
    for i, critter in enumerate(canyon_geese):
        if critter.type == CritterType.GOOSE:
            expected_mushrooms = 1 + 1  # base + canyon buff
            expected_lifespan = 2 + 1   # base + canyon buff
            print(f"  Goose {i+1}: {critter}")
            if critter.current_mushrooms_per_day == expected_mushrooms and critter.current_lifespan == expected_lifespan:
                print(f"    ✅ Correctly has Canyon buffs ({expected_mushrooms}/{expected_lifespan})")
            else:
                print(f"    ❌ Should have ({expected_mushrooms}/{expected_lifespan}), has ({critter.current_mushrooms_per_day}/{critter.current_lifespan})")


def test_goose_with_rhino():
    """Test Goose duplicates trigger Rhino effects"""
    print(f"\n{'='*60}")
    print("Testing Goose duplicates trigger Rhino effects...")
    
    engine = GameEngine()
    
    # Set up: Rhino at Beach, place Goose there
    rhino = Critter(CritterType.RHINO, 1, 4)
    goose = Critter(CritterType.GOOSE, 1, 2)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.locations[0].critters = [rhino]  # Put Rhino at Beach first
    rhino.current_location_id = 0
    engine.critter_queue = deque([goose, frog])
    
    print("Before placing Goose at Beach (with Rhino):")
    print(f"  Beach: {[str(c) for c in engine.locations[0].critters]}")
    print(f"  Rhino initial stats: {rhino}")
    
    # Place Goose at Beach (location 0) where Rhino is
    engine.process_turn(0, 0)
    
    print("After placing Goose at Beach:")
    print(f"  Beach: {[str(c) for c in engine.locations[0].critters]}")
    
    # Check Rhino buff - should get multiple buffs from multiple Goose entries
    beach_rhino = None
    goose_count = 0
    for critter in engine.locations[0].critters:
        if critter.type == CritterType.RHINO:
            beach_rhino = critter
        elif critter.type == CritterType.GOOSE:
            goose_count += 1
    
    if beach_rhino:
        expected_mushrooms = 1 + goose_count  # base + buff from each goose entering
        print(f"  Rhino after {goose_count} Geese enter: {beach_rhino}")
        if beach_rhino.current_mushrooms_per_day == expected_mushrooms:
            print(f"  ✅ Rhino correctly got +{goose_count} mushrooms per day from {goose_count} Goose entries")
        else:
            print(f"  ❌ Rhino should have {expected_mushrooms} mushrooms per day, has {beach_rhino.current_mushrooms_per_day}")
    else:
        print("  ❌ Rhino not found at Beach")


def test_goose_jungle_filter():
    """Test Goose duplicates get filtered by Jungle (need 2+ mushrooms to collect)"""
    print(f"\n{'='*60}")
    print("Testing Goose duplicates at Jungle (need 2+ mushrooms to collect)...")
    
    engine = GameEngine()
    
    # Set up: Place Goose at Jungle
    goose = Critter(CritterType.GOOSE, 1, 2)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.critter_queue = deque([goose, frog])
    
    initial_jungle_mushrooms = engine.locations[2].mushrooms
    print(f"Before placing Goose at Jungle:")
    print(f"  Jungle mushrooms: {initial_jungle_mushrooms}")
    print(f"  Goose base stats: {goose}")
    
    # Place Goose at Jungle (location 2)
    engine.process_turn(0, 2)
    
    print("After placing Goose at Jungle:")
    print(f"  Jungle: {[str(c) for c in engine.locations[2].critters]}")
    print(f"  Jungle mushrooms: {engine.locations[2].mushrooms}")
    
    # Check if any geese can collect (need 2+ mushrooms per day)
    geese_that_can_collect = 0
    for critter in engine.locations[2].critters:
        if critter.type == CritterType.GOOSE and critter.current_mushrooms_per_day >= 2:
            geese_that_can_collect += 1
    
    mushrooms_collected = initial_jungle_mushrooms - engine.locations[2].mushrooms
    print(f"  Geese that can collect in Jungle: {geese_that_can_collect}")
    print(f"  Mushrooms collected: {mushrooms_collected}")
    
    if geese_that_can_collect == 0:
        print("  ✅ Correctly, no basic Geese (1/2) can collect in Jungle")
    else:
        print(f"  ⚠️  {geese_that_can_collect} Geese can collect - check if they got buffs")


if __name__ == "__main__":
    test_goose_canyon_effects()
    test_goose_with_rhino()
    test_goose_jungle_filter()