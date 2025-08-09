## Overview
Spilled Mushrooms is a card puzzle game about delivering mushrooms using a squad of friendly animals.

Puzzles are framed as mushroom deliveries gone awry, requiring the player to strategically request assistance from their arsenal of critter companions to collect the lost mushrooms before the delivery deadline in one week. Each turn represents one day, so a puzzle is exactly seven turns. Each turn, the player must choose between two animals to send to one of the three areas they've dropped their mushrooms in; the other animal is placed at the bottom of the deck and will be available again on a later turn. The player must collect all of the mushrooms in all of the areas before the end of day 7 in order to complete the puzzle.

Puzzles are procedurally generated and are guaranteed to be solvable.

Critters have two stats, baskets and time, and up to two traits. The baskets represent how many mushrooms that critter will collect per turn, and the time represents how many turns the critter will be active for. Many traits will modify a critter's stats or impact their ability to collect mushrooms each day.

Areas have one stat, the number of mushrooms remaining, and up to one trait.

Each location and each critter has different characteristics

## Critters
Each criter has a number of days it will be deployed (lifespan) and a number of mushrooms it can collect each day

Example Criters(mushrooms per day / lifespan) and traits
Frog (1/5) - no special effects
Crocodile (3/2) - Can only cather mushrooms when this critter is alone at an area
Gopher (1/4) - At night, move to the next area
Penguin (2/3) - Swap any effects that change this critter's stats (e.g. +1 mushrooms per day becomes +1 lifespan)
Rhino (1/4) - When another critter enters the area, give this critter +1 mushrooms per day
Grizzly (3/2) - When played, give -1 mushrooms per day to other critters at the area
Goose (1/2) - When played, summon additional copies until the area is full
Sheep (1/4)- When another critter enters the area give this critter +1 lifespan

## Locations
Locations are initialised with some number of mushrooms, and applies certain rules that are applied to the criters at the location

Beach - 20 mushrooms - When gathering mushrooms here, critters do not use lifespan
Canyon - 21 mushrooms - When a critter enters here, give it +1 mushrooms per day and +1 lifespan
Jungle - 15 mushrooms - Only critters with 2 mushrooms per day or more can gather mushrooms here

## Program setup
1. 3 locations, each with a different number of mushrooms to collect
2. a queue with 8 critters

## Program flow
1. user selects a criter and a valid location (option will not be given to user if location is full)
2. Process rules based on the criter placement
3. Whoever is not chose in the day, moves to the back of the critter queue
4. Calculate the mushrooms collected based on the critters at each location and update counts
5. If final mushroom count goes to zero or below, remove location and all critters at the location
6. Move criters if necessary
7. Reduce criter lifespance and Advance day