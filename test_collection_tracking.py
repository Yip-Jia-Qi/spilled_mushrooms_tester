#!/usr/bin/env python3
"""
Test mushroom collection tracking
"""

from game_engine import GameEngine
from models import Critter, CritterType
from collections import deque


def test_basic_collection_tracking():
    """Test basic mushroom collection tracking"""
    print("Testing basic mushroom collection tracking...")
    
    engine = GameEngine()
    
    # Set up simple test: one Frog at Beach with 5 mushrooms
    frog = Critter(CritterType.FROG, 1, 5)
    sheep = Critter(CritterType.SHEEP, 1, 4)
    
    engine.critter_queue = deque([frog, sheep])
    engine.locations[0].mushrooms = 5  # Beach with 5 mushrooms
    
    print(f"Initial state:")
    print(f"  Beach: {engine.locations[0].mushrooms} mushrooms")
    print(f"  Frog collected so far: {frog.mushrooms_collected}")
    
    # Process turn: place Frog at Beach
    engine.process_turn(0, 0)
    
    print(f"After Day 1:")
    print(f"  Beach: {engine.locations[0].mushrooms} mushrooms")
    print(f"  Frog collected so far: {frog.mushrooms_collected}")
    
    # Process another turn to see more collection
    if not engine.game_over:
        engine.process_turn(0, 0)  # Place Sheep at Beach too
        
        print(f"After Day 2:")
        print(f"  Beach: {engine.locations[0].mushrooms} mushrooms")
        print(f"  Frog collected so far: {frog.mushrooms_collected}")
        
        # Find sheep at beach
        beach_sheep = None
        for critter in engine.locations[0].critters:
            if critter.type == CritterType.SHEEP:
                beach_sheep = critter
                break
        if beach_sheep:
            print(f"  Sheep collected so far: {beach_sheep.mushrooms_collected}")
    
    # Check summary
    summary = engine.get_collection_summary()
    print(f"\nCollection Summary:")
    print(f"  Total collected by all: {summary['total_collected']}")
    for critter_type, data in summary['by_type'].items():
        print(f"  {critter_type}: {data['total_collected']} mushrooms")


def test_crocodile_alone_collection():
    """Test Crocodile collection when alone vs with others"""
    print(f"\n{'='*50}")
    print("Testing Crocodile collection (alone vs with others)...")
    
    engine = GameEngine()
    
    # Set up: Crocodile alone at Canyon
    crocodile = Critter(CritterType.CROCODILE, 3, 2)
    frog = Critter(CritterType.FROG, 1, 5)
    
    engine.critter_queue = deque([crocodile, frog])
    engine.locations[1].mushrooms = 10  # Canyon with 10 mushrooms
    
    print(f"Turn 1: Crocodile alone at Canyon")
    engine.process_turn(0, 1)  # Crocodile to Canyon
    
    print(f"  Canyon: {engine.locations[1].mushrooms} mushrooms remaining")
    print(f"  Crocodile collected: {crocodile.mushrooms_collected}")
    
    print(f"Turn 2: Frog joins Crocodile at Canyon")  
    if not engine.game_over:
        engine.process_turn(0, 1)  # Frog to Canyon
        
        print(f"  Canyon: {engine.locations[1].mushrooms} mushrooms remaining")
        print(f"  Crocodile collected: {crocodile.mushrooms_collected} (should be unchanged - can't collect when not alone)")
        
        # Find frog at canyon
        canyon_frog = None
        for critter in engine.locations[1].critters:
            if critter.type == CritterType.FROG:
                canyon_frog = critter
                break
        if canyon_frog:
            print(f"  Frog collected: {canyon_frog.mushrooms_collected}")


if __name__ == "__main__":
    test_basic_collection_tracking()
    test_crocodile_alone_collection()