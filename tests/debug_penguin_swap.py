#!/usr/bin/env python3
"""
Debug Penguin stat swapping in detail
"""


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import CritterType, Critter, LocationType
from collections import deque


def debug_penguin_swap_step_by_step():
    """Debug Penguin swap with detailed step tracking"""
    print("Debugging Penguin stat swapping step by step...")
    
    engine = GameEngine()
    
    # Set up: Rhino at Canyon, Penguin to be placed
    rhino = Critter(CritterType.RHINO, 1, 4)
    penguin = Critter(CritterType.PENGUIN, 2, 3)
    frog = Critter(CritterType.FROG, 1, 5)
    
    # Manual setup
    engine.locations[1].critters = [rhino]
    rhino.current_location_id = 1
    engine.critter_queue = deque([penguin, frog])
    
    print(f"Before placement:")
    print(f"  Rhino: {rhino}")
    print(f"  Penguin: {penguin}")
    
    # Step by step processing
    canyon = engine.locations[1]
    
    # Step 1: Move penguin to location (this happens first)
    penguin.current_location_id = 1
    canyon.critters.append(penguin)
    print(f"\nAfter adding Penguin to Canyon:")
    print(f"  Canyon critters: {[str(c) for c in canyon.critters]}")
    
    # Step 2: Apply placement effects manually
    print(f"\nApplying placement effects...")
    for existing in canyon.critters[:-1]:  # Exclude just-added Penguin
        print(f"  Checking existing critter: {existing}")
        if existing.type == CritterType.RHINO:
            print(f"    Found Rhino! Applying effect...")
            buff_amount = 1
            if penguin.type == CritterType.PENGUIN:
                print(f"    Penguin entering, so Rhino gets +{buff_amount} lifespan instead of mushrooms")
                existing.current_lifespan += buff_amount
            else:
                print(f"    Normal critter entering, Rhino gets +{buff_amount} mushrooms per day")
                existing.current_mushrooms_per_day += buff_amount
            print(f"    Rhino after buff: {existing}")
    
    # Step 3: Apply location effects to Penguin
    print(f"\nApplying Canyon location effects to Penguin...")
    if canyon.type == LocationType.CANYON:
        print(f"  Canyon gives +1 mushrooms and +1 lifespan, but Penguin swaps these")
        penguin.current_mushrooms_per_day += 1  # Should be swapped but net effect is same
        penguin.current_lifespan += 1
        print(f"  Penguin after Canyon: {penguin}")
    
    print(f"\nFinal state:")
    print(f"  Rhino: {rhino}")
    print(f"  Penguin: {penguin}")


if __name__ == "__main__":
    debug_penguin_swap_step_by_step()