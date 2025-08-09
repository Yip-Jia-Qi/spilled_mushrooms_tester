#!/usr/bin/env python3
"""
Test queue rotation over multiple turns to verify correctness
"""

from game_engine import GameEngine


def test_queue_rotation_sequence():
    """Test the complete queue rotation sequence"""
    print("Testing queue rotation sequence...")
    
    engine = GameEngine("configs/cursed.json")
    
    print("Initial queue:")
    for i, c in enumerate(engine.critter_queue):
        print(f"  {i}: {c.type.value.title()}")
    
    # Expected sequence of available critters per day
    expected_days = [
        ["Grizzly", "Gopher"],      # Day 1
        ["Penguin", "Goose"],       # Day 2 (after choosing Gopher, Grizzly goes to back)
        ["Frog", "Crocodile"],      # Day 3 (after choosing Penguin, Goose goes to back)
        ["Rhino", "Sheep"],         # Day 4 (after choosing Frog, Crocodile goes to back)
        ["Grizzly", "Goose"],       # Day 5 (after choosing Rhino, Sheep goes to back)
    ]
    
    for day in range(1, 6):
        state = engine.get_game_state()
        available = [c.type.value.title() for c in state['queue']]
        expected = expected_days[day-1]
        
        print(f"\nDay {day}:")
        print(f"  Available: {available}")
        print(f"  Expected:  {expected}")
        print(f"  Match: {'✅' if available == expected else '❌'}")
        
        if day < 5:  # Don't process on last iteration
            # Choose first critter to first available location
            valid_moves = engine.get_valid_moves()
            if valid_moves:
                engine.process_turn(0, 0)  # Always choose first critter, first location


if __name__ == "__main__":
    test_queue_rotation_sequence()