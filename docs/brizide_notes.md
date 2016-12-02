# BriZide Notes
This document will cover most things about the code and game structure.
I am aiming for a rather complete pydoc documentation in the code itself.
So this will explain the structure itself, rather than how things work.

## File Types
The folder structure and file types are mostly inspired from the game _Re-Volt_.
Re-Volt already is a highly moddable game. With BriZide, I am trying to take
it even further by keeping everything open.

### `.inf`
These files contain meta-data (names, strings, paths, etc.) and parameters for
components (e.g. ship parameters). Python's configparser module is used to
read them.
The name is borrowed from Re-Volt's track information files (ini-like).

### `.blend`
Most `.blend` files are loaded via the LibLoad features of the BGE.
They can either be loaded for game logic containing a controller object
that runs a python module (game modes and some core components)
or for a 3D mesh (ships, building blocks).

### `.blk`
Block files exported from the track editor and contain level data.
At the moment, they are pickled dictionaries. I am planning to write them to
binary files to make the level loading procedure more secure.i

## Core Components
Core components are located in the `components` folder. These files can be
used in any game mode and must not be changed.

The ship prototype, for example, is `ship.blend`. It can be loaded several times
with different parameters each time, resulting in multiple ships, one for each
player.

Another example is the cube that surrounds a level (`cube.blend`).
The main python module `init_game.py` (via game modes) loads them with BGE's 
LibLoad commands.

For more information on the core components, take a look at the source of the
modules located in `modules`.

## Content

### Game Modes
Looking at game modes, there is only a thin line between source and user
content. 

Game modes are located in the `modes` folder. Each mode has its own
folder which usually contains a `.inf` file (basically a .ini containing meta
data) and a `.blend` file that contains a Controller object that loads the
provided module. 

The python module (`module.py`) should be located in the same folder.
Game modes are similar to core components.

Custom game modes are potentially dangerous since they could execute whatever
arbitrary code they contain.

### Levels
Levels are located in the `levels` folder. Each level gets its own folder.
Included files are a `.inf` containing meta-data and a `.blk` for the level
itself.
Not feature-complete yet.

### Ships
Ships should include a `.inf` file with the same name as the folder.
This file includes all parameters for the ship component.
A .blend file can be linked in the `.inf` to load a custom 3D mesh.
Not yet implemented: Custom ship sounds, etc.

#### Parameters
_Parameters_ refer to the ship attributes: Handling, 3D models and other
information used by the ship component.
