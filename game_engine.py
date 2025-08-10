from collections import deque
from typing import List, Optional, Union
import random
from models import Critter, Location, CritterType, LocationType, CRITTER_STATS, LOCATION_STATS


class GameEngine:
    def __init__(self, config=None):
        """
        Initialize game engine with optional configuration
        
        Args:
            config: GameConfig object, config file path (str), or None for default
        """
        self.day = 1
        self.locations = self._init_locations(config)
        self.critter_queue = deque(self._init_critters(config))
        self.all_critters_ever = []  # Track all critters for summary
        self.game_over = False
        self.game_won = False
        
        # Add initial critters to the full history
        self.all_critters_ever.extend(self.critter_queue)
    
    def _init_locations(self, config=None) -> List[Location]:
        """Initialize locations from config or use defaults"""
        if config is not None:
            game_config = self._load_config(config)
            return game_config.to_locations()
        
        # Default locations
        locations = []
        for i, (location_type, mushroom_count) in enumerate(LOCATION_STATS.items()):
            locations.append(Location(i, location_type, mushroom_count))
        return locations
    
    def _init_critters(self, config=None) -> List[Critter]:
        """Initialize critters from config or use defaults"""
        if config is not None:
            game_config = self._load_config(config)
            return game_config.to_critters()
        
        # Default random critters
        critters = []
        critter_types = list(CritterType)
        
        for _ in range(8):
            critter_type = random.choice(critter_types)
            mushrooms, lifespan = CRITTER_STATS[critter_type]
            critters.append(Critter(critter_type, mushrooms, lifespan))
        
        return critters
    
    def _load_config(self, config):
        """Load configuration from various sources"""
        if isinstance(config, str):
            # Config is a file path
            from config import ConfigManager
            return ConfigManager.load_config(config)
        else:
            # Config is already a GameConfig object
            return config
    
    def get_valid_moves(self) -> List[tuple]:
        """Returns list of (critter_index, location_index) valid moves"""
        valid_moves = []
        for critter_idx in range(min(2, len(self.critter_queue))):
            for location_idx in range(len(self.locations)):
                if not self.locations[location_idx].is_full():
                    valid_moves.append((critter_idx, location_idx))
        return valid_moves
    
    def process_turn(self, critter_choice: int, location_choice: int):
        """Process a complete turn with the given choices"""
        if (critter_choice, location_choice) not in self.get_valid_moves():
            raise ValueError("Invalid move")
        
        # 1. Get chosen critter and location
        chosen_critter = self.critter_queue[critter_choice]
        target_location = self.locations[location_choice]
        
        # 2. Move critter to location
        chosen_critter.current_location_id = location_choice
        target_location.critters.append(chosen_critter)
        
        # 3. Apply placement effects
        self._apply_placement_effects(chosen_critter, target_location)
        
        # 4. Apply location effects
        self._apply_location_effects(chosen_critter, target_location)
        
        # 5. Move unchosen critter to back of queue
        self._rotate_queue(critter_choice)
        
        # 6. Collect mushrooms
        self._collect_mushrooms()
        
        # 7. Remove completed locations
        self._remove_completed_locations()
        
        # 8. Apply end-of-day effects (Gopher movement)
        self._apply_end_of_day_effects()
        
        # 9. Reduce lifespans and advance day
        self._advance_day()
        
        # 10. Check win/lose conditions
        self._check_game_over()
    
    def _apply_placement_effects(self, critter: Critter, location: Location):
        """Apply effects when a critter is placed at a location"""
        
        # Grizzly: Give -1 mushrooms per day to other critters at area
        if critter.type == CritterType.GRIZZLY:
            for other in location.critters[:-1]:  # Exclude the just-added critter
                other.current_mushrooms_per_day = max(0, other.current_mushrooms_per_day - 1)
        
        # Goose: Summon basic 1/2 copies until area is full
        if critter.type == CritterType.GOOSE:
            while not location.is_full():
                goose_copy = Critter(CritterType.GOOSE, 1, 2)
                goose_copy.current_location_id = location.id
                location.critters.append(goose_copy)
                
                # Track the new critter
                self.all_critters_ever.append(goose_copy)
                
                # Apply location effects to the duplicate (they are "entering" the location)
                self._apply_location_effects(goose_copy, location)
                
                # Apply Rhino/Sheep effects for the duplicate entering
                self._apply_rhino_sheep_effects(goose_copy, location)
        
        # Rhino/Sheep effects on existing critters
        self._apply_rhino_sheep_effects(critter, location)
    
    def _apply_rhino_sheep_effects(self, entering_critter: Critter, location: Location):
        """Apply Rhino/Sheep effects when a critter enters a location"""
        for existing in location.critters[:-1]:  # Exclude the just-added critter
            if existing.type == CritterType.RHINO:
                buff_amount = 1
                if entering_critter.type == CritterType.PENGUIN:
                    # Penguin swaps mushroom buff to lifespan buff
                    existing.current_lifespan += buff_amount
                else:
                    existing.current_mushrooms_per_day += buff_amount
            
            elif existing.type == CritterType.SHEEP:
                buff_amount = 1
                if entering_critter.type == CritterType.PENGUIN:
                    # Penguin swaps lifespan buff to mushroom buff
                    existing.current_mushrooms_per_day += buff_amount
                else:
                    existing.current_lifespan += buff_amount
    
    def _apply_location_effects(self, critter: Critter, location: Location):
        """Apply location-specific effects to newly placed critter"""
        if location.type == LocationType.CANYON:
            # Canyon gives +1 mushrooms per day and +1 lifespan
            # Penguin swaps these effects
            critter.current_mushrooms_per_day += 1
            critter.current_lifespan += 1
    
    def _rotate_queue(self, chosen_index: int):
        """Remove chosen critter and move unchosen critter to back"""
        if chosen_index == 0:
            # Remove first critter (chosen)
            self.critter_queue.popleft()
            # Move second critter (unchosen) to back if it exists
            if len(self.critter_queue) >= 1:
                unchosen = self.critter_queue.popleft()
                self.critter_queue.append(unchosen)
        else:
            # chosen_index == 1, remove second critter and move first to back
            if len(self.critter_queue) >= 2:
                # Move first critter (unchosen) to back
                unchosen = self.critter_queue.popleft()  # Remove first
                self.critter_queue.popleft()  # Remove second (chosen)
                self.critter_queue.append(unchosen)  # Put first at back
    
    def _collect_mushrooms(self):
        """Calculate mushroom collection for all locations"""
        for location in self.locations:
            daily_collection = 0
            
            for critter in location.critters:
                can_collect = True
                collection_amount = 0
                
                # Crocodile: Can only collect when alone
                if critter.type == CritterType.CROCODILE and len(location.critters) > 1:
                    can_collect = False
                
                # Jungle: Only 2+ mushrooms per day critters can collect
                if location.type == LocationType.JUNGLE and critter.current_mushrooms_per_day < 2:
                    can_collect = False
                
                if can_collect:
                    # Calculate how much this critter can collect (limited by remaining mushrooms)
                    available_mushrooms = max(0, location.mushrooms - daily_collection)
                    collection_amount = min(critter.current_mushrooms_per_day, available_mushrooms)
                    if collection_amount > 0:
                        critter.mushrooms_collected += collection_amount
                        daily_collection += collection_amount
            
            location.mushrooms = max(0, location.mushrooms - daily_collection)
    
    def _remove_completed_locations(self):
        """Remove locations with 0 mushrooms and their critters"""
        for location in self.locations[:]:  # Create a copy to iterate over
            if location.mushrooms <= 0:
                location.critters.clear()
    
    def _apply_end_of_day_effects(self):
        """Apply end-of-day effects like Gopher movement"""
        gophers_to_move = []
        
        # Find all gophers that need to move
        for location in self.locations:
            for critter in location.critters[:]:  # Copy to avoid modification during iteration
                if critter.type == CritterType.GOPHER:
                    gophers_to_move.append((critter, location.id))
        
        # Process gopher movements
        for gopher, current_loc_id in gophers_to_move:
            next_loc_id = (current_loc_id + 1) % 3
            target_location = self.locations[next_loc_id]
            
            if not target_location.is_full():
                # Move to next location
                self.locations[current_loc_id].critters.remove(gopher)
                gopher.current_location_id = next_loc_id
                target_location.critters.append(gopher)
                # Apply Rhino/Sheep effects when Gopher enters new location
                self._apply_rhino_sheep_effects(gopher, target_location)
            else:
                # Next location is full, try to add to queue
                if len(self.critter_queue) < 8:
                    self.locations[current_loc_id].critters.remove(gopher)
                    gopher.current_location_id = None
                    self.critter_queue.append(gopher)
                # If no queue spot available, gopher stays put
    
    def _advance_day(self):
        """Advance day and reduce lifespans"""
        # Reduce lifespans for all critters (except those at Beach)
        for location in self.locations:
            if location.type != LocationType.BEACH:
                for critter in location.critters:
                    critter.current_lifespan -= 1
            
            # Remove critters with 0 lifespan
            location.critters = [c for c in location.critters if c.current_lifespan > 0]
        
        self.day += 1
    
    def _check_game_over(self):
        """Check if the game is won or lost"""
        # Check win condition: all locations have 0 mushrooms
        if all(location.mushrooms <= 0 for location in self.locations):
            self.game_won = True
            self.game_over = True
            return
        
        # Check lose condition: day 8 with mushrooms remaining
        if self.day > 7:
            self.game_over = True
            return
    
    def get_game_state(self) -> dict:
        """Return current game state for display"""
        return {
            'day': self.day,
            'locations': self.locations,
            'queue': list(self.critter_queue)[:2],  # Only show next 2 critters
            'game_over': self.game_over,
            'game_won': self.game_won,
            'total_mushrooms': sum(loc.mushrooms for loc in self.locations)
        }
    
    def get_all_critters(self) -> List[Critter]:
        """Get all critters in the game (deployed and in queue)"""
        all_critters = []
        
        # Add critters from locations
        for location in self.locations:
            all_critters.extend(location.critters)
        
        # Add critters from queue
        all_critters.extend(self.critter_queue)
        
        return all_critters
    
    def get_collection_summary(self) -> dict:
        """Get summary of mushrooms collected by each critter type"""
        all_critters = self.all_critters_ever
        
        # Group by critter type and sum collections
        type_summary = {}
        individual_summary = []
        
        for critter in all_critters:
            critter_type = critter.type.value.title()
            
            # Add to type summary
            if critter_type not in type_summary:
                type_summary[critter_type] = {'count': 0, 'total_collected': 0, 'critters': []}
            
            type_summary[critter_type]['count'] += 1
            type_summary[critter_type]['total_collected'] += critter.mushrooms_collected
            type_summary[critter_type]['critters'].append(critter)
            
            # Add to individual summary
            individual_summary.append({
                'type': critter_type,
                'collected': critter.mushrooms_collected,
                'final_stats': f"{critter.current_mushrooms_per_day}/{critter.current_lifespan}",
                'location': critter.current_location_id
            })
        
        return {
            'by_type': type_summary,
            'individual': individual_summary,
            'total_collected': sum(critter.mushrooms_collected for critter in all_critters)
        }