#!/usr/bin/env python3
"""
Test script to verify game mechanics work correctly
"""

from game_engine import GameEngine
from models import CritterType, LocationType


def test_basic_functionality():
    """Test basic game mechanics"""
    print("Testing Spilled Mushrooms Game Engine...")
    
    # Create a game engine
    engine = GameEngine()
    state = engine.get_game_state()
    
    print(f"Initial state - Day: {state['day']}, Total mushrooms: {state['total_mushrooms']}")
    
    # Display initial setup
    print("\nInitial Locations:")
    for i, location in enumerate(state['locations']):
        print(f"  {i}: {location}")
    
    print(f"\nInitial Queue (first 2):")
    for i, critter in enumerate(state['queue']):
        print(f"  {i}: {critter}")
    
    # Test a few moves
    print("\n" + "="*50)
    print("TESTING MOVES")
    print("="*50)
    
    # Move 1: Send first critter to beach
    valid_moves = engine.get_valid_moves()
    print(f"Valid moves: {valid_moves}")
    
    if valid_moves:
        critter_choice, location_choice = valid_moves[0]
        chosen_critter = list(engine.critter_queue)[critter_choice]
        target_location = engine.locations[location_choice]
        
        print(f"\nMove 1: Sending {chosen_critter.type.value.title()} to {target_location.type.value.title()}")
        engine.process_turn(critter_choice, location_choice)
        
        # Display state after move 1
        state = engine.get_game_state()
        print(f"After Move 1 - Day: {state['day']}, Total mushrooms: {state['total_mushrooms']}")
        
        for location in state['locations']:
            if location.critters or location.mushrooms < [20, 21, 15][location.id]:
                print(f"  {location}")
    
    # Move 2: Test another move
    if not engine.game_over:
        valid_moves = engine.get_valid_moves()
        if valid_moves:
            critter_choice, location_choice = valid_moves[0]
            chosen_critter = list(engine.critter_queue)[critter_choice]
            target_location = engine.locations[location_choice]
            
            print(f"\nMove 2: Sending {chosen_critter.type.value.title()} to {target_location.type.value.title()}")
            engine.process_turn(critter_choice, location_choice)
            
            # Display state after move 2
            state = engine.get_game_state()
            print(f"After Move 2 - Day: {state['day']}, Total mushrooms: {state['total_mushrooms']}")
            
            for location in state['locations']:
                if location.critters or location.mushrooms < [20, 21, 15][location.id]:
                    print(f"  {location}")
    
    print(f"\nGame Over: {engine.game_over}, Game Won: {engine.game_won}")
    print("Basic functionality test completed!")


def test_specific_critter_abilities():
    """Test specific critter abilities"""
    print("\n" + "="*50)
    print("TESTING CRITTER ABILITIES")
    print("="*50)
    
    # Test Canyon + Penguin interaction
    from models import Critter, Location
    
    engine = GameEngine()
    
    # Force specific critters for testing
    from collections import deque
    penguin = Critter(CritterType.PENGUIN, 2, 3)
    engine.critter_queue = deque([penguin, Critter(CritterType.FROG, 1, 5)])
    
    print(f"Testing Penguin at Canyon...")
    print(f"Penguin before: {penguin}")
    
    # Send penguin to canyon (location 1)
    engine.process_turn(0, 1)
    
    # Find the penguin in the canyon
    canyon = engine.locations[1]
    penguin_in_canyon = canyon.critters[0] if canyon.critters else None
    
    if penguin_in_canyon:
        print(f"Penguin after Canyon: {penguin_in_canyon}")
        expected_mushrooms = 2 + 1  # base + canyon buff
        expected_lifespan = 3 + 1   # base + canyon buff  
        print(f"Expected: Penguin should have {expected_mushrooms} mushrooms and {expected_lifespan} lifespan")
        print("(Canyon gives both stats, so Penguin swap doesn't change the result)")
    
    print("Specific ability test completed!")


if __name__ == "__main__":
    test_basic_functionality()
    test_specific_critter_abilities()