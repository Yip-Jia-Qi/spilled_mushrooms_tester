#!/usr/bin/env python3
"""
Test Goose duplicates get location effects without advancing day
"""


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import Critter, CritterType, LocationType
from collections import deque


def test_goose_canyon_before_day_advance():
    """Test Goose duplicates get Canyon effects before day advances"""
    print("Testing Goose duplicates get Canyon effects (before day advance)...")
    
    engine = GameEngine()
    
    # Set up: Empty Canyon, place Goose there
    goose = Critter(CritterType.GOOSE, 1, 2)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.critter_queue = deque([goose, frog])
    canyon = engine.locations[1]
    
    print("Manual step-by-step processing:")
    print(f"  Goose base stats: {goose}")
    
    # Step 1: Move goose to location
    goose.current_location_id = 1
    canyon.critters.append(goose)
    
    # Step 2: Apply placement effects (including Goose duplication)
    engine._apply_placement_effects(goose, canyon)
    
    # Step 3: Apply location effects to original goose
    engine._apply_location_effects(goose, canyon)
    
    print(f"After Goose duplication and location effects:")
    for i, critter in enumerate(canyon.critters):
        if critter.type == CritterType.GOOSE:
            print(f"    Goose {i+1}: {critter}")
    
    # Check that all geese got Canyon buffs
    all_correct = True
    for critter in canyon.critters:
        if critter.type == CritterType.GOOSE:
            expected_mushrooms = 2  # 1 base + 1 canyon
            expected_lifespan = 3   # 2 base + 1 canyon
            if critter.current_mushrooms_per_day != expected_mushrooms or critter.current_lifespan != expected_lifespan:
                all_correct = False
                print(f"    ❌ {critter} should be ({expected_mushrooms}/{expected_lifespan})")
    
    if all_correct:
        print(f"    ✅ All Geese correctly have Canyon buffs (2/3)")
    
    print(f"\nAfter advancing day (should lose 1 lifespan):")
    for critter in canyon.critters:
        if critter.current_lifespan > 0:
            critter.current_lifespan -= 1
    
    for i, critter in enumerate(canyon.critters):
        if critter.type == CritterType.GOOSE and critter.current_lifespan > 0:
            print(f"    Goose {i+1} after day advance: {critter}")
            expected_final = "2/2"
            actual = f"{critter.current_mushrooms_per_day}/{critter.current_lifespan}"
            if actual == expected_final:
                print(f"    ✅ Correctly became ({expected_final}) after day advance")
            else:
                print(f"    ❌ Should be ({expected_final}), is ({actual})")


if __name__ == "__main__":
    test_goose_canyon_before_day_advance()