import json
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from models import CritterType, LocationType, Critter, Location, CRITTER_STATS, LOCATION_STATS


@dataclass
class GameConfig:
    """Configuration for a game setup"""
    critters: List[str]  # List of critter type names
    locations: Optional[List[Dict[str, Union[str, int]]]] = None  # Custom locations
    
    def to_critters(self) -> List[Critter]:
        """Convert critter names to Critter objects"""
        critters = []
        for critter_name in self.critters:
            try:
                critter_type = CritterType(critter_name.lower())
                mushrooms, lifespan = CRITTER_STATS[critter_type]
                critters.append(Critter(critter_type, mushrooms, lifespan))
            except (ValueError, KeyError):
                print(f"Warning: Unknown critter type '{critter_name}', skipping")
                continue
        return critters
    
    def to_locations(self) -> List[Location]:
        """Convert location configs to Location objects"""
        if self.locations is None:
            # Use default locations
            locations = []
            for i, (location_type, mushroom_count) in enumerate(LOCATION_STATS.items()):
                locations.append(Location(i, location_type, mushroom_count))
            return locations
        
        locations = []
        for i, loc_config in enumerate(self.locations):
            try:
                location_type = LocationType(loc_config["type"].lower())
                mushroom_count = loc_config["mushrooms"]
                locations.append(Location(i, location_type, mushroom_count))
            except (ValueError, KeyError) as e:
                print(f"Warning: Invalid location config {loc_config}: {e}")
                continue
        return locations


class ConfigManager:
    """Manages loading and saving game configurations"""
    
    @staticmethod
    def load_config(filepath: str) -> GameConfig:
        """Load configuration from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return GameConfig(**data)
        except FileNotFoundError:
            print(f"Config file {filepath} not found, using default setup")
            return ConfigManager.get_default_config()
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}")
            return ConfigManager.get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            return ConfigManager.get_default_config()
    
    @staticmethod
    def save_config(config: GameConfig, filepath: str):
        """Save configuration to JSON file"""
        try:
            config_dict = {
                "critters": config.critters,
                "locations": config.locations
            }
            with open(filepath, 'w') as f:
                json.dump(config_dict, f, indent=2)
            print(f"Config saved to {filepath}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    @staticmethod
    def get_default_config() -> GameConfig:
        """Get the default random configuration"""
        import random
        critter_types = [ct.value for ct in CritterType]
        random_critters = random.choices(critter_types, k=8)
        return GameConfig(critters=random_critters)
    
    @staticmethod
    def create_example_configs():
        """Create example configuration files"""
        
        # Balanced team config
        balanced_config = GameConfig(
            critters=["frog", "frog", "rhino", "sheep", "penguin", "crocodile", "grizzly", "goose"],
            locations=[
                {"type": "beach", "mushrooms": 20},
                {"type": "canyon", "mushrooms": 21}, 
                {"type": "jungle", "mushrooms": 15}
            ]
        )
        ConfigManager.save_config(balanced_config, "configs/balanced.json")
        
        # High damage config
        damage_config = GameConfig(
            critters=["crocodile", "crocodile", "grizzly", "grizzly", "penguin", "rhino", "goose", "frog"],
            locations=[
                {"type": "beach", "mushrooms": 25},
                {"type": "canyon", "mushrooms": 25},
                {"type": "jungle", "mushrooms": 20}
            ]
        )
        ConfigManager.save_config(damage_config, "configs/high_damage.json")
        
        # Support heavy config
        support_config = GameConfig(
            critters=["rhino", "rhino", "sheep", "sheep", "penguin", "penguin", "gopher", "goose"],
            locations=[
                {"type": "beach", "mushrooms": 15},
                {"type": "canyon", "mushrooms": 15},
                {"type": "jungle", "mushrooms": 10}
            ]
        )
        ConfigManager.save_config(support_config, "configs/support.json")
        
        # Easy mode config
        easy_config = GameConfig(
            critters=["crocodile", "grizzly", "penguin", "rhino", "crocodile", "grizzly", "penguin", "rhino"],
            locations=[
                {"type": "beach", "mushrooms": 10},
                {"type": "canyon", "mushrooms": 10},
                {"type": "jungle", "mushrooms": 8}
            ]
        )
        ConfigManager.save_config(easy_config, "configs/easy.json")


def create_custom_config_interactive():
    """Interactive function to create a custom config"""
    print("Creating custom game configuration...")
    
    # Get critters
    print(f"\nAvailable critters: {', '.join([ct.value for ct in CritterType])}")
    critters = []
    
    for i in range(8):
        while True:
            critter = input(f"Enter critter {i+1}/8 (or 'random' for random): ").strip().lower()
            if critter == 'random':
                import random
                critter = random.choice([ct.value for ct in CritterType])
                print(f"  Selected: {critter}")
            
            if critter in [ct.value for ct in CritterType]:
                critters.append(critter)
                break
            else:
                print(f"Invalid critter: {critter}")
    
    # Get locations (optional)
    use_custom_locations = input("\nUse custom locations? (y/n, default: n): ").strip().lower() == 'y'
    locations = None
    
    if use_custom_locations:
        locations = []
        location_types = [lt.value for lt in LocationType]
        print(f"Available location types: {', '.join(location_types)}")
        
        for i in range(3):
            while True:
                loc_type = input(f"Location {i+1} type: ").strip().lower()
                if loc_type in location_types:
                    break
                print(f"Invalid location type: {loc_type}")
            
            while True:
                try:
                    mushrooms = int(input(f"Location {i+1} mushrooms: "))
                    if mushrooms > 0:
                        break
                    print("Mushrooms must be positive")
                except ValueError:
                    print("Please enter a valid number")
            
            locations.append({"type": loc_type, "mushrooms": mushrooms})
    
    # Create and save config
    config = GameConfig(critters=critters, locations=locations)
    
    filename = input("\nEnter config filename (without .json): ").strip()
    if not filename:
        filename = "custom"
    
    ConfigManager.save_config(config, f"configs/{filename}.json")
    print(f"Custom config created: configs/{filename}.json")
    return config


if __name__ == "__main__":
    import os
    
    # Create configs directory
    os.makedirs("configs", exist_ok=True)
    
    # Create example configs
    ConfigManager.create_example_configs()
    print("Example configurations created in configs/ directory")
    
    # Option to create custom config
    if input("\nCreate a custom config interactively? (y/n): ").strip().lower() == 'y':
        create_custom_config_interactive()