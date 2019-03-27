# Configuration

## Game Menu

Some options can be configured via the in-game menu.

**Fullscreen**: Runs the game in fullscreen mode.

**Detailed Level Cube**: Adds windows to the large cube (poor performance).

**Bloom**: Turns the bloom filter on or off.

**Blur**: Turns the radial blur filter (appears when going very fast) on or off.

**Lights**: Turns light effects on or off.

**Extra Textures**: Turns textures that are affected by light on or off.

The menu will restart and apply the changes when selecting _Back_.

## config.ini

More advanced settings can be found in the file called `config.ini`

### Game

**leveldir**: Name of the last played level (without `.json`)

**mode**: Name of the game mode

**version**: Version of the game

### Player

**name**: Name of the player used for saving highscores

**ship**: Selected ship

### Audio

**master**: Overall sound volume (0.0 to 1.0)

**music**: Music volume (0.0 to 1.0)

**effects**: Menu, engine and wind sounds (0.0 to 1.0)

### Video

**width**: Width of the game's resolution

**height**: Height of the game's resolution

**num_particles**: Amount of spark particles for collisions

### Dev

**debug**: True or False. Enables development features.

## Controls_Player1

See the [bge docs](https://docs.blender.org/api/2.79b/bge.events.html#keys-constants) for available keys.

**ship_thrust**: Key for going forward

**ship_thrust_reverse**: Key for going backward

**ship_steer_left**: Key for steering left

**ship_steer_right**: Key for steering right

**ship_boost**: Key for engaging boost

**ship_deactivate_stabilizer**: Key for drifting

**ship_pause**: Key for the pause menu

## Editor

Not used anymore
