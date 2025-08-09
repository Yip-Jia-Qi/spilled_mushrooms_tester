# Spilled Mushrooms

A card puzzle game about delivering mushrooms using a squad of friendly animals.

## How to Play

Collect all mushrooms within 7 days to win! Each turn, choose one of two available critters and send them to one of three locations to collect mushrooms.

## Quick Start

```bash
# Play with default random setup
python3 main.py

# Play with a specific configuration
python3 main.py configs/balanced.json

# Run automated demo
python3 simple_game.py configs/easy.json
```

## Configuration System

You can customize your game by creating configuration files that specify exactly which critters and locations you want.

### Using Existing Configurations

Pre-made configurations are available in the `configs/` directory:

- **balanced.json** - A well-rounded team with variety
- **high_damage.json** - Heavy damage dealers with more mushrooms  
- **support.json** - Support-heavy team with synergistic critters
- **easy.json** - Fewer mushrooms for easier wins

### Creating Custom Configurations

Configuration files use JSON format:

```json
{
  "critters": [
    "crocodile", "crocodile", "penguin", "rhino", 
    "sheep", "grizzly", "goose", "frog"
  ],
  "locations": [
    {"type": "beach", "mushrooms": 15},
    {"type": "canyon", "mushrooms": 18}, 
    {"type": "jungle", "mushrooms": 12}
  ]
}
```

#### Available Critters (mushrooms per day / lifespan):
- **frog** (1/5) - No special effects
- **crocodile** (3/2) - Can only gather mushrooms when alone at an area
- **gopher** (1/4) - At night, move to the next area  
- **penguin** (2/3) - Swap any effects that change this critter's stats
- **rhino** (1/4) - When another critter enters the area, give this critter +1 mushrooms per day
- **grizzly** (3/2) - When played, give -1 mushrooms per day to other critters at the area
- **goose** (1/2) - When played, summon additional copies until the area is full
- **sheep** (1/4) - When another critter enters the area give this critter +1 lifespan

#### Available Locations:
- **beach** - Critters do not use lifespan when gathering here
- **canyon** - When a critter enters here, give it +1 mushrooms per day and +1 lifespan
- **jungle** - Only critters with 2 mushrooms per day or more can gather mushrooms here

### Interactive Config Creation

```bash
# Create example configs and optionally make a custom one
python3 config.py
```

## Game Files

- `main.py` - Interactive game with player input
- `simple_game.py` - Automated demo version
- `config.py` - Configuration management and creation
- `models.py` - Game data structures  
- `game_engine.py` - Core game logic and rules
- `game_ui.py` - Text-based user interface
- `test_config.py` - Configuration system tests

## Examples

```bash
# Play the balanced configuration interactively  
python3 main.py configs/balanced.json

# Watch the easy configuration play automatically
python3 simple_game.py configs/easy.json

# Test all configurations
python3 test_config.py
```