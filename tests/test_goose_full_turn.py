#!/usr/bin/env python3
"""
Test Goose duplicates with full turn processing
"""


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import CritterType
from collections import deque


def test_goose_canyon_full_turn():
    """Test Goose at Canyon with full turn processing"""
    print("Testing Goose at Canyon with full turn processing...")
    
    engine = GameEngine()
    
    # Set up specific critters for controlled test
    from models import Critter
    goose = Critter(CritterType.GOOSE, 1, 2)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.critter_queue = deque([goose, frog])
    
    print(f"Before turn - Canyon: {[str(c) for c in engine.locations[1].critters]}")
    print(f"Goose base stats: {goose}")
    
    # Process full turn: Goose (index 0) to Canyon (index 1)
    engine.process_turn(0, 1)
    
    print(f"After turn - Canyon: {[str(c) for c in engine.locations[1].critters]}")
    
    # Verify all geese have correct stats
    canyon_geese = [c for c in engine.locations[1].critters if c.type == CritterType.GOOSE]
    expected_stats = "2/2"  # (1+1)/(2+1-1) = 2/2 after Canyon buff and day advance
    
    all_correct = True
    for i, goose in enumerate(canyon_geese):
        actual_stats = f"{goose.current_mushrooms_per_day}/{goose.current_lifespan}"
        print(f"  Goose {i+1}: {actual_stats} (expected: {expected_stats})")
        if actual_stats != expected_stats:
            all_correct = False
    
    if all_correct and len(canyon_geese) == 3:
        print(f"✅ SUCCESS: All {len(canyon_geese)} Geese correctly have stats {expected_stats}")
    else:
        print(f"❌ FAILED: Expected 3 Geese with stats {expected_stats}")


def test_goose_beach_full_turn():
    """Test Goose at Beach (no lifespan loss)"""
    print(f"\n{'='*50}")
    print("Testing Goose at Beach with full turn processing...")
    
    engine = GameEngine()
    
    from models import Critter
    goose = Critter(CritterType.GOOSE, 1, 2)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.critter_queue = deque([goose, frog])
    
    print(f"Before turn - Beach: {[str(c) for c in engine.locations[0].critters]}")
    
    # Process full turn: Goose (index 0) to Beach (index 0)
    engine.process_turn(0, 0)
    
    print(f"After turn - Beach: {[str(c) for c in engine.locations[0].critters]}")
    
    # At Beach, no lifespan loss, so should be base stats (1/2)
    beach_geese = [c for c in engine.locations[0].critters if c.type == CritterType.GOOSE]
    expected_stats = "1/2"  # No location buff, no lifespan loss at Beach
    
    all_correct = True
    for i, goose in enumerate(beach_geese):
        actual_stats = f"{goose.current_mushrooms_per_day}/{goose.current_lifespan}"
        print(f"  Goose {i+1}: {actual_stats} (expected: {expected_stats})")
        if actual_stats != expected_stats:
            all_correct = False
    
    if all_correct and len(beach_geese) == 3:
        print(f"✅ SUCCESS: All {len(beach_geese)} Geese correctly have stats {expected_stats}")
    else:
        print(f"❌ FAILED: Expected 3 Geese with stats {expected_stats}")


if __name__ == "__main__":
    test_goose_canyon_full_turn()
    test_goose_beach_full_turn()