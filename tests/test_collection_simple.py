#!/usr/bin/env python3
"""
Simple test of mushroom collection using actual game flow
"""


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine


def test_collection_with_real_game():
    """Test collection tracking with real game flow"""
    print("Testing collection with real game flow...")
    
    # Use a simple setup
    engine = GameEngine("configs/easy.json")
    
    print("Initial critters in queue:")
    for i, critter in enumerate(list(engine.critter_queue)[:4]):
        print(f"  {i}: {critter} (collected: {critter.mushrooms_collected})")
    
    print(f"\nInitial mushrooms: Beach={engine.locations[0].mushrooms}, Canyon={engine.locations[1].mushrooms}, Jungle={engine.locations[2].mushrooms}")
    
    # Play a few turns
    for turn in range(3):
        if not engine.game_over:
            valid_moves = engine.get_valid_moves()
            if valid_moves:
                critter_idx, location_idx = valid_moves[0]  # Choose first valid move
                critter_name = list(engine.critter_queue)[critter_idx].type.value.title()
                location_name = ['Beach', 'Canyon', 'Jungle'][location_idx]
                
                print(f"\nTurn {turn + 1}: Send {critter_name} to {location_name}")
                engine.process_turn(critter_idx, location_idx)
                
                print(f"  Mushrooms remaining: Beach={engine.locations[0].mushrooms}, Canyon={engine.locations[1].mushrooms}, Jungle={engine.locations[2].mushrooms}")
    
    # Show collection summary
    summary = engine.get_collection_summary()
    print(f"\nFinal Collection Summary:")
    print(f"Total mushrooms collected: {summary['total_collected']}")
    
    for critter_type, data in summary['by_type'].items():
        if data['total_collected'] > 0:
            print(f"  {critter_type}: {data['total_collected']} mushrooms (from {data['count']} critters)")
    
    # Show individual performers
    performers = [c for c in summary['individual'] if c['collected'] > 0]
    if performers:
        print(f"\nIndividual performers:")
        for perf in performers:
            print(f"  {perf['type']}: {perf['collected']} mushrooms")


if __name__ == "__main__":
    test_collection_with_real_game()