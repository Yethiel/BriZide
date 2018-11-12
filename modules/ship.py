from bge import logic

import os
import mathutils
import configparser

from modules import helpers



uim = logic.uim
settigns = logic.settings
kbd = logic.keyboard

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

class Ship():
    def __init__(self, identifier, player_id):

        self.load(identifier)

        # Meta
        self.name = ""
        self.identifier = self.identifier
        self.player_id = player_id

        # Assets
        self.model_path = ""
        self.texture_path = ""
        self.ship_path = logic.expandPath(
            "//ships/"+identifier)
        self.inf_path = logic.expandPath(
            "//ships/"+identifier+"/"+identifier+".inf")

        # Parameters
        self.top_speed = 0.0
        self.top_thrust = 0.0
        self.thrust = 0.0
        self.grip = 0.0
        self.grip_air = 0.0
        self.steer_rate = 0.0
        self.steer_max = 0.0
        self.stable_threshold = 0.0
        self.stable_strength = 0.0
        self.shield = 0.0
        self.hover_height = 0.0
        self.hover_strength = 0.0
        self.hover_damping = 0.0

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
        self.current_thrust = 0.0
        self.current_boost = 0.0

    def load(self, ship_name):
        inf = configparser.ConfigParser()

        if os.path.isfile(self.inf_path):
            inf.read(self.inf_path)
            if G.DEBUG: print("Loaded ship information file.")
        else:
            helpers.fatal_error(
                "Could not find ship information file at {}".format(self.inf_path))

        for category in inf:
            for key in inf[category]:

                if key == "Name":
                    self.name = str(key)
                elif key == "Model":
                    self.model_path = str(key)
                elif key == "Texture":
                    self.texture_path = str(key)

                elif key == "TopSpeed": 
                    self.top_speed = float(key)
                elif key == "TopThrust": 
                    self.top_thrust = float(key)
                elif key == "Thrust": 
                    self.thrust = float(key)
                elif key == "Grip": 
                    self.grip = float(key)
                elif key == "GripAir": 
                    self.grip_air = float(key)
                elif key == "SteerRate": 
                    self.steer_rate = float(key)
                elif key == "SteerMax": 
                    self.steer_max = float(key)
                elif key == "StableThreshold": 
                    self.stable_threshold = float(key)
                elif key == "StableStrength": 
                    self.stable_strength = float(key)
                elif key == "Shield": 
                    self.shield = float(key)
                elif key == "HoverHeight": 
                    self.hover_height = float(key)
                elif key == "HoverStrength": 
                    self.hover_strength = float(key)
                elif key == "HoverDamping": 
                    self.hover_damping = float(key)

        # Sets controls
        c_stt = settings["Controls_Player1"]

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

    def run(self):
        own = logic.getCurrentController().owner
        
        # "recenters" thrust if not controlled
        if self.current_thrust > 0:
            self.current_thrust -= self.thrust
        else:
            self.current_thrust += self.thrust

    def controls(self):
        
        own = logic.getCurrentController().owner

        # Sets the thrust
        if kbd.events[self.key_thrust] == ACTIVE:
            thrust(1)
        
        if kbd.events[self.key_thrust_reverse] == ACTIVE:
            thrust(-1)

        # Applies the thrust
        if abs(max(own.getLinearVelocity(True))) < self.top_speed:
            own.applyForce([0, self.current_thrust, 0], True)

        # Boost
        if kbd.events[self.key_boost] == ACTIVE:
            allow_boost = max(own.getLinearVelocity(True)) < self.top_speed * 1.5

            if self.current_boost > 10 and allow_boost:
                own.applyForce((0, self.thrust * 2, 0), True)
                self.current_boost -= 2.5

        # Stabilizer
        if kbd.events[self.key_deactivate_stabilizer] == ACTIVE or not own["on_ground"]:
            pass:
        else:
            self.stabilize()

    def stabilize(self):
        own = logic.getCurrentController().owner

        if abs(own.localLinearVelocity[0]) >= self.stable_threshold:
            own.applyForce(
                [-own.localLinearVelocity[0] * self.stable_strength * self.get_grip(),0,0], 
                True
            )
            own.applyForce(
                [0,abs(own.localLinearVelocity[0]) * self.get_grip(),0], 
                True
            )


