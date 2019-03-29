# Ships

Ships can be found in the `ships` folder. Each folder contains a `.blend` file with the 3D model, a `.txt` file containing handling information, and other assets like textures.

- [How to create a new ship](#creating-a-new-ship)
- [How to change a ship's handling](#tweaking-the-parameters-file)

## Creating a new Ship

Create a folder in the `ships` folder with a name that you like, for example `test_ship`.

Go inside that folder and create a new text file with the name of your ship for example `test_ship.txt`.

Open the file with a text editor and copy the following text into it:

```
[Main]
Name:           Test Ship
Model:          //ships/test_ship/test_ship.blend

[Handling]
TopSpeed:           200.0
TopThrust:          90.0
Thrust:             8.0

Grip:               0.6
GripAir:            1.0

SteerRate:          0.23
SteerMax:           0.06

StableThreshold:    0.001
StableStrength:     2.6

HoverHeight:        5.4
HoverStrength:      350.0
HoverDamping:       3.4

[Flare1]
x:                  0.0
y:                  -1.55737
z:                  -0.016694
```

Open Blender and save a .blend file in your ship's folder. The file name has to match the file specified in the .txt file.

> You can also copy an existing ship's .blend file and start tweaking it if you don't have much experience with Blender.

In Blender, create a new object and rename it to your ship's folder name. You're completely free to use any material features of the Blender Game Engine.

Resources of the game that you can use:

- **env.jpg** for reflections. Check the other ships' material setup of the texture called `env`.

If you created a new folder in `ships` added the parameter file (.txt) and filled it with content and created a .blend file with an object named after your ship's folder name, your ship should now show up in the game.

## Tweaking the Parameters File

Each ship can have its unique set of handling parameters. You're completely free to enter any values you'd like. Just don't go too far, extreme values might break the game!

### Main

**Name**: Name of the ship

**Model**: File path to a .blend file containing the ship model starting with `//`, relative from the game's folder.

### Handling

**TopSpeed**: Maximum speed of the ship

**TopThrust**: Strength of the ship's engine

**Thrust**: How quickly the ship reaches top thrust

**Grip**: How well the ship maintains sideways traction when going fast

**GripAir**: Grip in air

**SteerRate**: How quickly the ship turns

**SteerMax**: How much the ship can turn

**StableThreshold**: At which speed the stabilizer for sideways traction kicks in

**StableStrength**: Force of the sideways traction that keeps the ship going forward and not slide around

**HoverHeight**: How high the ship hovers above the ground

**HoverStrength**: Strength of the force

**HoverDamping**: Softness of the hover effect

## FlareX

You can add any number of engine flares to the ship. The section has to start with `[Flare` and can be followed by numbers or names. Check the ship `black_coffee` for an example.

You can specify the location of the engine flares, typically right inside the ship's exhaust:

**x**: left/right

**y**: forward/back

**z**: up/down