#!/usr/bin/env python3
"""
Debug the Gopher movement issue
"""


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import CritterType


def debug_gopher_issue():
    """Debug the specific Gopher issue"""
    print("Debugging Gopher movement issue...")
    
    # Create engine with the cursed config
    engine = GameEngine("configs/cursed.json")
    
    # Initial state
    state = engine.get_game_state()
    print(f"Initial state - Day {state['day']}")
    print(f"Queue: {[str(c) for c in state['queue']]}")
    print(f"All critters in queue: {[str(c) for c in engine.critter_queue]}")
    
    # Move 1: Send Gopher (index 1) to Canyon (index 1) 
    print(f"\n--- Move 1: Gopher to Canyon ---")
    print("Before move:")
    print(f"Queue length: {len(engine.critter_queue)}")
    for i, c in enumerate(engine.critter_queue):
        print(f"  {i}: {c}")
    
    # Process the move
    engine.process_turn(1, 1)  # Gopher (index 1) to Canyon (index 1)
    
    print("Expected after move: Grizzly should be at the back, queue should be [Penguin, Goose, Frog, Crocodile, Rhino, Sheep, Grizzly]")
    
    print("After move:")
    print(f"Queue length: {len(engine.critter_queue)}")
    for i, c in enumerate(engine.critter_queue):
        print(f"  {i}: {c}")
    
    # Check locations
    print("Locations after move:")
    for i, location in enumerate(engine.locations):
        if location.critters:
            print(f"  Location {i} ({location.type.value}): {[str(c) for c in location.critters]}")
    
    # Show state
    state = engine.get_game_state()
    print(f"\nState after move 1 - Day {state['day']}")
    print(f"Available critters: {[str(c) for c in state['queue']]}")
    
    # Check if any critters are in both queue and locations
    print(f"\nChecking for duplicates...")
    queue_critters = list(engine.critter_queue)
    location_critters = []
    for location in engine.locations:
        location_critters.extend(location.critters)
    
    print(f"Critters in queue: {len(queue_critters)}")
    print(f"Critters in locations: {len(location_critters)}")
    
    # Check for same object references
    for i, queue_critter in enumerate(queue_critters):
        for j, loc_critter in enumerate(location_critters):
            if queue_critter is loc_critter:
                print(f"ERROR: Same critter object found in queue[{i}] and location[{j}]: {queue_critter}")


if __name__ == "__main__":
    debug_gopher_issue()