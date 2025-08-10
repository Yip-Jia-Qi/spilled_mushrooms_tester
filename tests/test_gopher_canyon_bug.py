#!/usr/bin/env python3
"""
Test the Gopher Canyon bonus bug fix
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from models import CritterType
from logger import logged_output


def test_gopher_canyon_bonus():
    """Test that Gopher gets Canyon bonus each time it enters Canyon"""
    engine = GameEngine()
    
    print("Testing Gopher Canyon bonus bug fix...")
    print("=" * 50)
    
    # Show initial queue
    print("Initial queue:")
    for i, critter in enumerate(engine.critter_queue):
        print(f"  {i}: {critter}")
    
    # Find a gopher in the queue
    gopher = None
    gopher_index = None
    for i, critter in enumerate(engine.critter_queue):
        if critter.type == CritterType.GOPHER:
            gopher = critter
            gopher_index = i
            break
    
    if gopher is None:
        print("❌ No Gopher found in queue!")
        return
    
    print(f"\nGopher found at index {gopher_index}: {gopher}")
    initial_mushrooms = gopher.current_mushrooms_per_day
    
    # Check valid moves
    valid_moves = engine.get_valid_moves()
    print(f"Valid moves: {valid_moves}")
    
    # If gopher is not in the first two positions, make some moves to get it there
    if gopher_index > 1:
        print(f"Gopher is at index {gopher_index}, need to advance queue...")
        # Make moves to advance the queue until gopher is available
        moves_made = 0
        while gopher_index > 1 and moves_made < 5:
            # Make any valid move to advance the queue
            if valid_moves:
                first_move = valid_moves[0]
                print(f"  Making move to advance queue: {first_move}")
                engine.process_turn(first_move[0], first_move[1])
                moves_made += 1
                # Update gopher index
                for i, critter in enumerate(engine.critter_queue):
                    if critter.type == CritterType.GOPHER:
                        gopher_index = i
                        break
                valid_moves = engine.get_valid_moves()
            else:
                break
    
    # Find a move that sends the gopher to Canyon
    canyon_move = None
    for critter_idx, location_idx in valid_moves:
        if critter_idx == gopher_index and location_idx == 1:  # Canyon is location index 1
            canyon_move = (critter_idx, location_idx)
            break
    
    if canyon_move is None:
        print(f"❌ No valid move to send Gopher (index {gopher_index}) to Canyon!")
        print("Available moves for current queue positions:")
        for i, critter in enumerate(list(engine.critter_queue)[:2]):
            print(f"  {i}: {critter}")
        return
    
    # Send Gopher to Canyon
    print(f"\n--- Sending Gopher to Canyon (first time) ---")
    print(f"Move: {canyon_move}")
    engine.process_turn(canyon_move[0], canyon_move[1])
    
    # Check all locations for the gopher
    print("After move, checking all locations:")
    for i, location in enumerate(engine.locations):
        print(f"  Location {i} ({location.type.value}): {location.critters}")
    
    # Find the gopher at Canyon
    canyon = engine.locations[1]
    gopher_at_canyon = None
    for critter in canyon.critters:
        if critter.type == CritterType.GOPHER:
            gopher_at_canyon = critter
            break
    
    if gopher_at_canyon is None:
        print("Gopher not found at Canyon - it may have moved during end-of-day effects!")
        # Find the gopher wherever it is
        gopher_moved = None
        for location in engine.locations:
            for critter in location.critters:
                if critter.type == CritterType.GOPHER:
                    gopher_moved = critter
                    break
            if gopher_moved:
                break
        
        if gopher_moved:
            print(f"Found Gopher at {gopher_moved.current_location_id}: {gopher_moved}")
            first_canyon_mushrooms = gopher_moved.current_mushrooms_per_day
            
            expected_first = initial_mushrooms + 1  # Canyon gives +1
            if first_canyon_mushrooms == expected_first:
                print(f"✅ Canyon bonus applied: {initial_mushrooms} -> {first_canyon_mushrooms} (+1)")
                print("🎉 Bug fix working! Gopher got Canyon bonus and moved to next location.")
            else:
                print(f"❌ Canyon bonus not applied: Expected {expected_first}, got {first_canyon_mushrooms}")
            return
        else:
            print("❌ Gopher disappeared completely!")
            return
        
    print(f"Gopher after first Canyon visit: {gopher_at_canyon}")
    first_canyon_mushrooms = gopher_at_canyon.current_mushrooms_per_day
    
    expected_first = initial_mushrooms + 1  # Canyon gives +1
    if first_canyon_mushrooms == expected_first:
        print(f"✅ First Canyon visit: {initial_mushrooms} -> {first_canyon_mushrooms} (+1)")
    else:
        print(f"❌ First Canyon visit: Expected {expected_first}, got {first_canyon_mushrooms}")
    
    # Apply end-of-day effects multiple times to make Gopher move around and come back to Canyon
    print(f"\n--- Moving Gopher around (should return to Canyon eventually) ---")
    for day in range(2, 8):
        engine._advance_day()
        engine._apply_end_of_day_effects()
        
        # Check if Gopher is back at Canyon
        canyon = engine.locations[1]
        gopher_at_canyon = None
        for critter in canyon.critters:
            if critter.type == CritterType.GOPHER:
                gopher_at_canyon = critter
                break
        
        if gopher_at_canyon is not None:
            print(f"Day {day}: Gopher back at Canyon: {gopher_at_canyon}")
            second_canyon_mushrooms = gopher_at_canyon.current_mushrooms_per_day
            
            expected_second = first_canyon_mushrooms + 1  # Should get another +1
            if second_canyon_mushrooms == expected_second:
                print(f"✅ Second Canyon visit: {first_canyon_mushrooms} -> {second_canyon_mushrooms} (+1)")
                print("🎉 Bug fix successful! Gopher gets Canyon bonus each time it enters.")
                return
            else:
                print(f"❌ Second Canyon visit: Expected {expected_second}, got {second_canyon_mushrooms}")
                print("🐛 Bug still exists - Gopher not getting Canyon bonus on re-entry")
                return
    
    print("⚠️  Gopher didn't return to Canyon during test period")


if __name__ == "__main__":
    with logged_output(os.path.join("tests", "logs", "test_gopher_canyon_bug.txt")) as log_path:
        print(f"Test session logging to: {log_path}")
        test_gopher_canyon_bonus()