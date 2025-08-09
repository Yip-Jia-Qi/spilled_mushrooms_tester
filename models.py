from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class CritterType(Enum):
    FROG = "frog"
    CROCODILE = "crocodile"
    GOPHER = "gopher"
    PENGUIN = "penguin"
    RHINO = "rhino"
    GRIZZLY = "grizzly"
    GOOSE = "goose"
    SHEEP = "sheep"


class LocationType(Enum):
    BEACH = "beach"
    CANYON = "canyon"
    JUNGLE = "jungle"


@dataclass
class Critter:
    type: CritterType
    base_mushrooms_per_day: int
    base_lifespan: int
    current_mushrooms_per_day: int = 0
    current_lifespan: int = 0
    current_location_id: Optional[int] = None
    
    def __post_init__(self):
        if self.current_mushrooms_per_day == 0:
            self.current_mushrooms_per_day = self.base_mushrooms_per_day
        if self.current_lifespan == 0:
            self.current_lifespan = self.base_lifespan
    
    def __str__(self):
        location = f" at location {self.current_location_id}" if self.current_location_id is not None else ""
        return f"{self.type.value.title()} ({self.current_mushrooms_per_day}/{self.current_lifespan}){location}"


@dataclass
class Location:
    id: int
    type: LocationType
    mushrooms: int
    max_critters: int = 3
    critters: List[Critter] = field(default_factory=list)
    
    def is_full(self) -> bool:
        return len(self.critters) >= self.max_critters
    
    def __str__(self):
        critter_info = ", ".join([f"{c.type.value.title()}({c.current_mushrooms_per_day}/{c.current_lifespan})" 
                                for c in self.critters]) if self.critters else "Empty"
        return f"{self.type.value.title()}: {self.mushrooms} mushrooms [{critter_info}]"


CRITTER_STATS = {
    CritterType.FROG: (1, 5),
    CritterType.CROCODILE: (3, 2),
    CritterType.GOPHER: (1, 4),
    CritterType.PENGUIN: (2, 3),
    CritterType.RHINO: (1, 4),
    CritterType.GRIZZLY: (3, 2),
    CritterType.GOOSE: (1, 2),
    CritterType.SHEEP: (1, 4),
}

LOCATION_STATS = {
    LocationType.BEACH: 20,
    LocationType.CANYON: 21,
    LocationType.JUNGLE: 15,
}