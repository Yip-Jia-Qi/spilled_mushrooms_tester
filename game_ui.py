from typing import List, Tuple
from models import Critter, Location
from game_engine import GameEngine


class GameUI:
    def __init__(self, config=None):
        """
        Initialize GameUI with optional configuration
        
        Args:
            config: GameConfig object, config file path (str), or None for default
        """
        self.engine = GameEngine(config)
    
    def display_game_state(self):
        """Display current game state"""
        state = self.engine.get_game_state()
        
        print(f"\n{'='*60}")
        print(f"DAY {state['day']}/7 - Spilled Mushrooms")
        print(f"Total mushrooms remaining: {state['total_mushrooms']}")
        print(f"{'='*60}")
        
        # Display locations
        print("\nLOCATIONS:")
        for i, location in enumerate(state['locations']):
            if location.mushrooms > 0:  # Only show locations with mushrooms
                print(f"  {i+1}. {location}")
        
        # Display available critters
        print(f"\nAVAILABLE CRITTERS:")
        queue = state['queue']
        for i, critter in enumerate(queue):
            print(f"  {i+1}. {critter}")
        
        print()
    
    def display_critter_abilities(self):
        """Display critter abilities reference"""
        abilities = {
            "Frog": "No special effects",
            "Crocodile": "Can only gather mushrooms when alone at an area",
            "Gopher": "At night, move to the next area",
            "Penguin": "Swap any effects that change this critter's stats",
            "Rhino": "When another critter enters the area, give this critter +1 mushrooms per day",
            "Grizzly": "When played, give -1 mushrooms per day to other critters at the area",
            "Goose": "When played, summon additional copies until the area is full",
            "Sheep": "When another critter enters the area, give this critter +1 lifespan"
        }
        
        print("\nCRITTER ABILITIES:")
        print("-" * 40)
        for critter, ability in abilities.items():
            print(f"{critter}: {ability}")
        print()
    
    def display_location_effects(self):
        """Display location effects reference"""
        effects = {
            "Beach": "When gathering mushrooms here, critters do not use lifespan",
            "Canyon": "When a critter enters here, give it +1 mushrooms per day and +1 lifespan",
            "Jungle": "Only critters with 2 mushrooms per day or more can gather mushrooms here"
        }
        
        print("\nLOCATION EFFECTS:")
        print("-" * 40)
        for location, effect in effects.items():
            print(f"{location}: {effect}")
        print()
    
    def get_player_move(self) -> Tuple[int, int]:
        """Get player's move choice"""
        valid_moves = self.engine.get_valid_moves()
        
        if not valid_moves:
            print("No valid moves available!")
            return None, None
        
        print("VALID MOVES:")
        for i, (critter_idx, location_idx) in enumerate(valid_moves):
            critter = list(self.engine.critter_queue)[critter_idx]
            location = self.engine.locations[location_idx]
            print(f"  {i+1}. Send {critter.type.value.title()} to {location.type.value.title()}")
        
        while True:
            try:
                choice = input(f"\nChoose move (1-{len(valid_moves)}) or 'help' for abilities: ").strip().lower()
                
                if choice == 'help':
                    self.display_critter_abilities()
                    self.display_location_effects()
                    continue
                
                move_idx = int(choice) - 1
                if 0 <= move_idx < len(valid_moves):
                    return valid_moves[move_idx]
                else:
                    print(f"Please enter a number between 1 and {len(valid_moves)}")
            
            except ValueError:
                print("Please enter a valid number or 'help'")
            except KeyboardInterrupt:
                print("\nGame interrupted!")
                return None, None
    
    def display_turn_summary(self, critter_choice: int, location_choice: int):
        """Display what happened this turn"""
        chosen_critter = list(self.engine.critter_queue)[critter_choice]
        target_location = self.engine.locations[location_choice]
        
        print(f"\nTurn Summary:")
        print(f"Sent {chosen_critter.type.value.title()} to {target_location.type.value.title()}")
    
    def display_game_over(self):
        """Display game over screen"""
        state = self.engine.get_game_state()
        
        print("\n" + "="*60)
        if state['game_won']:
            print("🎉 CONGRATULATIONS! YOU WON! 🎉")
            print("All mushrooms have been successfully collected!")
        else:
            print("💀 GAME OVER 💀")
            print(f"Time ran out with {state['total_mushrooms']} mushrooms remaining.")
        
        print(f"Final day: {state['day']-1}/7")
        print("="*60)
        
        # Display collection summary
        self.display_collection_summary()
    
    def display_collection_summary(self):
        """Display summary of mushrooms collected by each animal"""
        summary = self.engine.get_collection_summary()
        
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
        
        # Show top performers
        individual = summary['individual']
        top_performers = sorted([c for c in individual if c['collected'] > 0], 
                              key=lambda x: x['collected'], 
                              reverse=True)
        
        if top_performers:
            print(f"\n🏆 TOP PERFORMERS:")
            print("-" * 40)
            for i, performer in enumerate(top_performers[:5]):  # Show top 5
                location_name = ""
                if performer['location'] is not None:
                    locations = ['Beach', 'Canyon', 'Jungle']
                    location_name = f" (at {locations[performer['location']]})"
                
                print(f"{i+1}. {performer['type']} - {performer['collected']} mushrooms{location_name}")
        
        # Show animals that didn't collect anything
        non_collectors = [c for c in individual if c['collected'] == 0]
        if non_collectors:
            print(f"\n🐌 BENCH WARMERS (0 mushrooms collected):")
            print("-" * 40)
            bench_by_type = {}
            for critter in non_collectors:
                critter_type = critter['type']
                if critter_type not in bench_by_type:
                    bench_by_type[critter_type] = 0
                bench_by_type[critter_type] += 1
            
            for critter_type, count in bench_by_type.items():
                plural = "s" if count > 1 else ""
                print(f"  {count} {critter_type}{plural}")
        
        print("=" * 60)
    
    def play_game(self):
        """Main game loop"""
        print("🍄 Welcome to Spilled Mushrooms! 🍄")
        print("Collect all mushrooms within 7 days to win!")
        print("Type 'help' during any turn to see critter abilities.")
        
        while not self.engine.game_over:
            self.display_game_state()
            
            critter_choice, location_choice = self.get_player_move()
            
            if critter_choice is None:  # Player quit or no valid moves
                break
            
            self.display_turn_summary(critter_choice, location_choice)
            
            try:
                self.engine.process_turn(critter_choice, location_choice)
            except ValueError as e:
                print(f"Error: {e}")
                continue
            
            # Show immediate results
            input("\nPress Enter to continue...")
        
        if self.engine.game_over:
            self.display_game_over()


if __name__ == "__main__":
    game = GameUI()
    game.play_game()