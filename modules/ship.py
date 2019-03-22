from bge import logic, events

import os
import aud
import mathutils
import configparser
from random import randint

from modules import helpers, sound, global_constants as G
from modules.helpers import clamp

uim = logic.uim
kbd = logic.keyboard

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

class Ship():
    def __init__(self, game_obj, identifier, player_id):

        self.go = game_obj
        self.id = logic.game.register_ship(self)

        # Meta
        self.name = ""
        self.identifier = identifier
        self.player_id = player_id

        # Assets
        self.ship_path = logic.expandPath(
            "//ships/"+identifier)
        self.inf_path = logic.expandPath(
            "//ships/"+identifier+"/"+identifier+".inf")

        # Parameters
        self.top_speed = 1.0
        self.top_thrust = 1.0
        self.thrust = 1.0
        self.grip = 1.0
        self.grip_air = 1.0
        self.steer_rate = 1.0
        self.steer_max = 1.0
        self.stable_threshold = 1.0
        self.stable_strength = 1.0
        self.shield = 1.0
        self.hover_height = 1.0
        self.hover_strength = 1.0
        self.hover_damping = 1.0

        # Controls
        self.key_thrust = None
        self.key_thrust_reverse = None
        self.key_steer_left = None
        self.key_steer_right = None
        self.key_boost = None
        self.key_activate_weapon = None
        self.key_deactivate_stabilizer = None
        self.key_absorb_weapon = None
        self.key_pause = None

        # Current values
        self.current_steer = 0.0
        self.current_thrust = 0.0
        self.current_boost = 0.0
        self.current_velocity = 0.0
        self.on_ground = False
        self.gravity = 150

        # Directional objects
        self.whl_fl = self.go.children["whl_fl"]
        self.whl_fr = self.go.children["whl_fr"]
        self.whl_bl = self.go.children["whl_bl"]
        self.whl_br = self.go.children["whl_br"]

        self.dir_neg_whl_fl = self.go.children["dir_neg_whl_fl"]
        self.dir_neg_whl_fr = self.go.children["dir_neg_whl_fr"]
        self.dir_neg_whl_bl = self.go.children["dir_neg_whl_bl"]
        self.dir_neg_whl_br = self.go.children["dir_neg_whl_br"]

        self.dir_z_neg = self.go.children["dir_z_neg"]
        self.dir_z_pos = self.go.children["dir_z_pos"]

        self.init = False
        self.init_mesh = False
        self.sounds = {}

        self.particles = []
        self.particles_used = []

        self.load(identifier)

    def load(self, ship_name):
        inf = configparser.ConfigParser()
        scene = logic.getCurrentScene()

        if os.path.isfile(self.inf_path):
            inf.read(self.inf_path)
            if G.DEBUG: print("Loaded ship information file.")
        else:
            helpers.fatal_error(
                "Could not find ship information file at {}".format(self.inf_path))

        for category in inf:
            for key in inf[category]:

                if key == "name":
                    self.name = str(inf[category][key])

                elif key == "topspeed":
                    self.top_speed = float(inf[category][key])
                elif key == "topthrust":
                    self.top_thrust = float(inf[category][key])
                elif key == "thrust":
                    self.thrust = float(inf[category][key])
                elif key == "grip":
                    self.grip = float(inf[category][key])
                elif key == "gripair":
                    self.grip_air = float(inf[category][key])
                elif key == "steerrate":
                    self.steer_rate = float(inf[category][key])
                elif key == "steermax":
                    self.steer_max = float(inf[category][key])
                elif key == "stablethreshold":
                    self.stable_threshold = float(inf[category][key])
                elif key == "stablestrength":
                    self.stable_strength = float(inf[category][key])
                elif key == "shield":
                    self.shield = float(inf[category][key])
                elif key == "hoverheight":
                    self.hover_height = float(inf[category][key])
                elif key == "hoverstrength":
                    self.hover_strength = float(inf[category][key])
                elif key == "hoverdamping":
                    self.hover_damping = float(inf[category][key])

        # Sets controls
        c_stt = logic.settings["Controls_Player1"]

        self.key_thrust = getattr(
            events, c_stt["ship_thrust"]
        )
        self.key_thrust_reverse = getattr(
            events, c_stt["ship_thrust_reverse"]
        )
        self.key_steer_left = getattr(
            events, c_stt["ship_steer_left"]
        )
        self.key_steer_right = getattr(
            events, c_stt["ship_steer_right"]
        )
        self.key_boost = getattr(
            events, c_stt["ship_boost"]
        )
        self.key_deactivate_stabilizer = getattr(
            events, c_stt["ship_deactivate_stabilizer"]
        )

        self.go.setVisible(False, False)  # sets self invisible, not recursive
        # replaces the physics mesh
        self.go.replaceMesh(ship_name, False, True)
        # replaces the display mesh
        self.go.children["Mesh"].replaceMesh(ship_name, True, False)

        for x in range(int(logic.settings["Video"]["num_particles"])):
            self.particles.append(scene.addObject("particle_spark", self.go))
        self.go.collisionCallbacks.append(self.on_collision_sparks)

        self.init = True

    def run(self):

        camera = logic.getCurrentScene().objects["Camera_Ship"]

        if not "init_sound_engine" in self.go:

            self.sounds["engine_idle"] = sound.play("engine_idle")
            self.sounds["engine_idle"].relative = False
            self.sounds["engine_idle"].loop_count = -1
            self.sounds["engine_idle"].relative = False
            self.sounds["engine_idle"].distance_maximum = 64

            self.sounds["boost_low"] = sound.play("boost_low")
            self.sounds["boost_low"].relative = False
            self.sounds["boost_low"].volume = 0.0
            self.sounds["boost_low"].loop_count = -1
            self.sounds["boost_low"].relative = False
            self.sounds["boost_low"].distance_maximum = 64

            self.sounds["boost_high"] = sound.play("boost_high")
            self.sounds["boost_high"].relative = False
            self.sounds["boost_high"].volume = 0.0
            self.sounds["boost_high"].loop_count = -1
            self.sounds["boost_high"].relative = False
            self.sounds["boost_high"].distance_maximum = 64

            self.sounds["engine"] = sound.play("engine_loop")
            self.sounds["engine"].relative = False
            self.sounds["engine"].loop_count = -1
            self.sounds["engine"].relative = False
            self.sounds["engine"].distance_maximum = 64

            self.sounds["engine_top"] = sound.play("engine_top")
            self.sounds["engine_top"].relative = False
            self.sounds["engine_top"].loop_count = -1
            self.sounds["engine_top"].relative = False
            self.sounds["engine_top"].distance_maximum = 64

            self.sounds["air"] = sound.play("wind")
            self.sounds["air"].loop_count = -1
            self.sounds["air"].volume = 0.0
            self.sounds["air"].relative = False
            self.sounds["air"].distance_maximum = 32
            self.sounds["air"].distance_reference = 0


            self.go["init_sound_engine"] = True
            logic.device.distance_model = aud.AUD_DISTANCE_MODEL_LINEAR

        self.current_velocity = self.go.localLinearVelocity[1]

        # Collision
        if self.particles_used and self.particles_used[-1]["timer"] > 1.0:
            self.particles.append(self.particles_used[-1])
            self.particles_used = self.particles_used[:-1]
        self.go.childrenRecursive["flare"].worldScale = [self.current_thrust / self.top_thrust + .5 for x in range(3)]

        logic.device.listener_location = camera.worldPosition
        logic.device.listener_orientation = camera.worldOrientation.to_quaternion()

        logic.game.go["radial"] = clamp((self.current_velocity - (self.top_speed-10)) /  (self.top_speed+50) * 0.7, 0, 0.15)

        self.sounds["engine"].volume = clamp((self.current_thrust / self.top_thrust), 0, 2)
        self.sounds["engine_idle"].volume = clamp(1 - self.current_thrust / self.top_thrust, 0, 2)
        self.sounds["engine"].pitch = 1 + (.3 * self.current_velocity / self.top_speed)
        self.sounds["engine_top"].volume = clamp((self.current_velocity - self.top_speed) /  self.top_speed , 0, 2)
        self.sounds["air"].volume = clamp((abs(self.go.getLinearVelocity(True)[0] + (self.go.getLinearVelocity(True)[1]/2) + self.go.getLinearVelocity(True)[2]))/200, 0, 2)

        self.sounds["engine_idle"].location = self.go.worldPosition
        self.sounds["engine_top"].location = self.go.worldPosition
        self.sounds["engine"].location = self.go.worldPosition
        self.sounds["air"].location = self.go.worldPosition

        if logic.uim.focus == "ship":
            self.controls()
        else:
            self.sounds["boost_high"].volume = 0
            self.sounds["boost_low"].volume = 0

        # Generates boost
        if abs(self.go.localLinearVelocity[0]) > 70:

            # smoke = logic.getCurrentScene().addObject("Smoke", self.go)
            # smoke.color[3] = sum([abs(c) for c in self.go.localLinearVelocity]) / self.top_speed
            if self.current_boost < 500:
                self.current_boost += abs(self.go.localLinearVelocity[0])/120
            else:
                self.current_boost = 500


        if not ACTIVE in [kbd.events[self.key_thrust_reverse], kbd.events[self.key_thrust]]:
            self.center_thrust()
        if not ACTIVE in [kbd.events[self.key_steer_right], kbd.events[self.key_steer_left]]:
            self.center_steering()

        obj, point, normal = self.go.rayCast(
            self.dir_z_neg, self.go, 2 * self.hover_height, "mag"
        )

        self.on_ground = True
        if obj != None:
            normalmed = mathutils.Vector((0,0,0))
            for whl in [(self.whl_fr, self.dir_neg_whl_fr), (self.whl_fl, self.dir_neg_whl_fl), (self.whl_bl, self.dir_neg_whl_bl), (self.whl_br, self.dir_neg_whl_br)]:
                obj, point, normal = self.go.rayCast(whl[1], whl[0], 2 * self.hover_height, "mag")
                if obj != None:
                    normalmed += normal
            if obj != None:
                actual_dist = -whl[0].getDistanceTo(point)
                distance = (actual_dist + self.hover_height)
                cancel = -whl[0].localLinearVelocity.z * self.hover_damping * (distance + self.hover_height)
                force = distance * self.hover_strength + cancel
                self.go.applyForce([0, 0, force], True)
                self.go.alignAxisToVect(normalmed, 2, .2)
        else:
            self.on_ground = False
            self.go.applyForce([0, 0, -self.gravity], True)

        # Ship behavior that does not necessarily depend on controls
        self.go.applyRotation((0,0, self.current_steer), True) #actual steering happens here


        self.go["turn"] = self.current_steer
        # # Catch OOB TODO: Fix
        # level = logic.game.get_level()
        # cube_size = level.get_cube_size()
        # if cube_size > 0:
        #     if self.go.worldPosition.z < -16:
        #         self.go.worldPosition.z += 32
        #     if self.go.worldPosition.z > cube_size * 32 - 16:
        #         self.go.worldPosition.z += 32

        #     if self.go.worldPosition.y > cube_size * 32 - 16:
        #         self.go.worldPosition.y -= 32
        #     if self.go.worldPosition.y < -16:
        #         self.go.worldPosition.y += 32

        #     if self.go.worldPosition.x > cube_size * 32 - 16:
        #         self.go.worldPosition.x -= 32
        #     if self.go.worldPosition.x < -16:
        #         self.go.worldPosition.x += 32

    def controls(self):
        """ Controls only work when the uim focus is set to 'ship' """

        if kbd.events[self.key_steer_left] == ACTIVE:
            self.steer(-1) # also accepts floats for analog controls

        if kbd.events[self.key_steer_right] == ACTIVE:
            self.steer(1) # also accepts floats for analog controls

        # Sets the thrust
        if kbd.events[self.key_thrust] == ACTIVE:
            self.add_thrust(1)

        if kbd.events[self.key_thrust_reverse] == ACTIVE:
            self.add_thrust(-1)

        # Applies the thrust
        if abs(max(self.go.getLinearVelocity(True))) < self.top_speed:
            self.go.applyForce([0, self.current_thrust, 0], True)

        # Boost
        if kbd.events[self.key_boost] == JUST_ACTIVATED:
            sound.play("boost_kick")


        if kbd.events[self.key_boost] == ACTIVE and self.current_boost > 10:
            allow_boost = max(self.go.getLinearVelocity(True)) < self.top_speed * 1.5
            if allow_boost:
                self.go.applyForce((0, self.thrust * 18, 0), True)
                self.current_boost -= 2.5
            # smoke = logic.getCurrentScene().addObject("Smoke", self.go)

            self.sounds["boost_low"].pitch = clamp(self.current_velocity / self.top_speed + 1, 1.0, 3)
            self.sounds["boost_high"].volume = 0.25
            self.sounds["boost_low"].volume = clamp(self.current_velocity / self.top_speed, 0, 0.65)

        else:
            self.sounds["boost_low"].volume = 0.0
            self.sounds["boost_low"].pitch = 1.0
            self.sounds["boost_high"].volume = 0.0


        # Stabilizer
        if kbd.events[self.key_deactivate_stabilizer] == ACTIVE or not self.on_ground:
            pass
        else:
            self.stabilize()

    def get_grip(self):
        if self.on_ground and not kbd.events[self.key_deactivate_stabilizer] == ACTIVE:
            return abs(1 - (self.go.localLinearVelocity[1]/self.top_speed) + self.grip)
        else:
            return self.grip_air

    def steer(self, d):

        delta = logic.getLogicTicRate()

        if self.go.localLinearVelocity[1] < 0 and kbd.events[self.key_thrust_reverse] == ACTIVE:
            d *= -1 # inverse steering when going reverse


        # Smoothly center steering.
        if self.current_steer > 0: #currently steering left
            if d < 0: # player wants left
                if abs(self.current_steer) <= self.steer_max:
                    self.current_steer += (1/delta * self.steer_rate * self.get_grip())* -d

            elif d > 0: # player wants right
                self.center_steering()
                pass

        # Smoothly center steering.
        elif self.current_steer < 0: #currently steering right
            if d < 0: # player wants left
                self.center_steering()
                pass
            elif d > 0: # player wants right
                if abs(self.current_steer) <= self.steer_max:
                    self.current_steer += (1/delta * self.steer_rate * self.get_grip())* -d

        else:
            if abs(self.current_steer) <= self.steer_max:
                self.current_steer += (1/delta * self.steer_rate* self.get_grip())* -d


    def add_thrust(self, d):
        delta = logic.getLogicTicRate()
        if abs(self.current_thrust) <= abs(self.top_thrust) and max(self.go.getLinearVelocity(True)) < self.top_speed:
            self.current_thrust += 1/delta * self.thrust * d * 10

    def stabilize(self):
        if abs(self.go.localLinearVelocity[0]) >= self.stable_threshold:
            self.go.applyForce(
                [-self.go.localLinearVelocity[0] * self.stable_strength * self.get_grip(),0,0],
                True
            )
            self.go.applyForce(
                [0,abs(self.go.localLinearVelocity[0]) * self.get_grip() / 2 ,0],
                True
            )

    def center_steering(self):
        delta = logic.getLogicTicRate()

        if abs(self.current_steer) < abs(1/delta * self.steer_rate): self.current_steer = 0

        if self.current_steer > 0:
            self.current_steer -= (1/delta * self.steer_rate)
        elif self.current_steer < 0:
            self.current_steer += (1/delta * self.steer_rate)
        else:
            pass


    def center_thrust(self):
        delta = logic.getLogicTicRate()

        if self.current_thrust > 0:
            self.current_thrust -= self.thrust * 1/delta * 60
        else:
            self.current_thrust += self.thrust * 1/delta * 60

    def on_collision_sparks(self, obj, point, normal):
        scene = logic.getCurrentScene()

        if self.particles:
            p = self.particles.pop()
            p["timer"] = 0.7
            p.worldPosition = point
            for x in range(1):
                normal[x] += randint(0, 10) * 0.1
            normal[2] += randint(-10, 10) * 0.2
            p.setLinearVelocity(normal * randint(-15, 10))
            self.particles_used.append(p)
        # print(obj, point, normal)

def setup():
    """ Runs once after loading the component """

    game_obj = logic.getCurrentController().owner

    level = logic.game.get_level()

    # for player in game.players:

    player_id = logic.game.players[0]

    identifier = logic.settings["Player{}".format(player_id)]["ship"]

    ship = Ship(game_obj, identifier, player_id)

    ship.gravity = 0 if level.cube_size == 0 else 150

    logic.game.assign_ship_to_player(ship.id, player_id)

    ship.go.worldPosition = level.get_start_pos()
    ship_orientation = ship.go.worldOrientation.to_euler() # we need an euler matrix
    start_orientation = level.get_start_orientation()
    for x in [0, 1, 2]:
        ship_orientation[x] = start_orientation[x]
    ship.go.worldOrientation = ship_orientation.to_matrix()

    logic.components.mark_loaded("ship")


def main():
    """ Runs every logic tick """

    if logic.game.ships[0].init:
        logic.game.ships[0].run()


