#!/usr/bin/env python3
"""
Test the exact scenario from your game where Goose goes to Canyon
"""


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import Critter, CritterType
from collections import deque


def test_your_goose_scenario():
    """Test your exact scenario: Goose sent to Canyon"""
    print("Testing your exact scenario: Goose sent to Canyon...")
    
    # Use cursed config to match your game
    engine = GameEngine("configs/cursed.json")
    
    # Fast-forward to a state where we can place Goose at Canyon
    # This simulates your Day 5 state
    from models import Location, LocationType
    
    # Clear and set up specific state
    engine.locations[1].critters = []  # Empty Canyon
    engine.locations[1].mushrooms = 17  # From your game state
    
    goose = Critter(CritterType.GOOSE, 1, 2)
    frog = Critter(CritterType.FROG, 1, 5)
    engine.critter_queue = deque([goose, frog])
    
    print("Before placing Goose at Canyon:")
    print(f"  Canyon: {engine.locations[1].mushrooms} mushrooms, {[str(c) for c in engine.locations[1].critters]}")
    print(f"  Goose base stats: {goose}")
    
    # Process the turn: Goose to Canyon
    engine.process_turn(0, 1)
    
    print("After placing Goose at Canyon:")
    canyon = engine.locations[1]
    print(f"  Canyon: {canyon.mushrooms} mushrooms")
    print(f"  Canyon critters: {[str(c) for c in canyon.critters]}")
    
    # Verify the expected result from your game
    geese_count = len([c for c in canyon.critters if c.type == CritterType.GOOSE])
    if geese_count == 3:
        print(f"✅ Goose correctly summoned {geese_count} total geese")
        
        # Check their stats - should be (2/2) in your game
        all_correct = True
        for i, critter in enumerate(canyon.critters):
            if critter.type == CritterType.GOOSE:
                expected = "2/2"  # Canyon gives +1/+1, then day advance -1 lifespan
                actual = f"{critter.current_mushrooms_per_day}/{critter.current_lifespan}"
                print(f"    Goose {i+1}: {actual} (expected: {expected})")
                if actual != expected:
                    all_correct = False
        
        if all_correct:
            print("✅ All Geese have correct stats matching your game!")
        else:
            print("❌ Goose stats don't match expected values")
    else:
        print(f"❌ Expected 3 geese, got {geese_count}")
    
    # Check mushroom collection
    expected_collection = 3 * 2  # 3 geese * 2 mushrooms each
    actual_collection = 17 - canyon.mushrooms  # 17 was initial
    print(f"  Mushrooms collected: {actual_collection} (expected: ~{expected_collection})")


if __name__ == "__main__":
    test_your_goose_scenario()