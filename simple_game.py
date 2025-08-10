#!/usr/bin/env python3
"""
Simple version of Spilled Mushrooms that can be played with predetermined moves
"""

from game_engine import GameEngine
from models import CritterType
from logger import logged_output


def play_simple_game(config=None):
    """Play a simple game with predetermined moves"""
    with logged_output() as log_path:
        print(f"Simple game session logging to: {log_path}")
        engine = GameEngine(config)
        
        print("🍄 Spilled Mushrooms - Simple Demo 🍄")
        print("=" * 60)
        
        move_count = 0
        
        while not engine.game_over and move_count < 10:  # Limit to 10 moves for demo
            state = engine.get_game_state()
            
            print(f"\nDAY {state['day']}/7")
            print(f"Total mushrooms remaining: {state['total_mushrooms']}")
            print("\nLocations:")
            for i, location in enumerate(state['locations']):
                if location.mushrooms > 0:
                    print(f"  {location}")
            
            print(f"\nAvailable critters:")
            queue = state['queue']
            for i, critter in enumerate(queue):
                print(f"  {i+1}. {critter}")
            
            # Get valid moves
            valid_moves = engine.get_valid_moves()
            if not valid_moves:
                print("No valid moves!")
                break
            
            # Choose first valid move for demo
            critter_choice, location_choice = valid_moves[0]
            chosen_critter = list(engine.critter_queue)[critter_choice]
            target_location = engine.locations[location_choice]
            
            print(f"\nMove {move_count + 1}: Sending {chosen_critter.type.value.title()} to {target_location.type.value.title()}")
            
            # Process the turn
            engine.process_turn(critter_choice, location_choice)
            
            move_count += 1
            print("-" * 60)
        
        # Final state
        state = engine.get_game_state()
        print(f"\nFINAL STATE:")
        print(f"Day {state['day']}/7")
        print(f"Total mushrooms remaining: {state['total_mushrooms']}")
        
        if state['game_won']:
            print("🎉 GAME WON! 🎉")
        elif state['game_over']:
            print("💀 GAME OVER - Time ran out! 💀")
        else:
            print("Demo ended early")
        
        print("\nFinal locations:")
        for location in state['locations']:
            if location.mushrooms > 0 or location.critters:
                print(f"  {location}")
        
        # Show collection summary
        display_collection_summary(engine)


def display_collection_summary(engine):
    """Display summary of mushrooms collected by each animal"""
    summary = engine.get_collection_summary()
    
    print("\n🍄 MUSHROOM COLLECTION SUMMARY 🍄")
    print("-" * 60)
    
    # Sort by total collected (descending)
    sorted_types = sorted(summary['by_type'].items(), 
                         key=lambda x: x[1]['total_collected'], 
                         reverse=True)
    
    print(f"{'Animal Type':<12} {'Count':<5} {'Total Collected':<15} {'Average':<8}")
    print("-" * 50)
    
    for critter_type, data in sorted_types:
        count = data['count']
        total = data['total_collected']
        average = total / count if count > 0 else 0
        print(f"{critter_type:<12} {count:<5} {total:<15} {average:<8.1f}")
    
    print("-" * 50)
    print(f"{'TOTAL':<12} {'':<5} {summary['total_collected']:<15}")


if __name__ == "__main__":
    import sys
    config = None
    if len(sys.argv) > 1:
        config = sys.argv[1]
        print(f"Using config: {config}")
    
    play_simple_game(config)