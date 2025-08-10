#!/usr/bin/env python3
"""
Test the full detailed summary display
"""

from game_ui import GameUI


def test_full_summary():
    """Test the full detailed summary with top performers and bench warmers"""
    
    # Create a game and simulate it ending
    ui = GameUI("configs/balanced.json")
    engine = ui.engine
    
    # Fast forward to end of game by setting day to 8
    engine.day = 8
    engine.game_over = True
    engine.game_won = False
    
    # Add some collection data to various critters for demonstration
    all_critters = engine.all_critters_ever
    
    # Give some critters collection data
    if len(all_critters) >= 6:
        all_critters[0].mushrooms_collected = 15  # Top performer
        all_critters[1].mushrooms_collected = 12  # Second best
        all_critters[2].mushrooms_collected = 8   # Third
        all_critters[3].mushrooms_collected = 5   # Fourth
        all_critters[4].mushrooms_collected = 2   # Fifth
        # Leave others at 0 for bench warmers
    
    # Set some locations for deployed critters
    all_critters[0].current_location_id = 0  # Beach
    all_critters[1].current_location_id = 1  # Canyon
    all_critters[2].current_location_id = None  # In queue
    
    print("Testing full detailed summary...")
    ui.display_game_over()


if __name__ == "__main__":
    test_full_summary()