from bge import logic
from modules import global_constants as G
from math import pi
gD = logic.globalDict
sce = logic.getCurrentScene()

# p_data = gD["current"]["level"]["portal_data"]
def setup():
    pass

    # own = logic.getCurrentController().owner
    # id_num = own["id"]

    # # add portal to the global dict
    # p_data[own["id"]] = {}
    # p_data[own["id"]]["resets"] = []
    # p_data[own["id"]]["reference"] = own

    # # set the link reference from the link_id set in the editor
    # for obj in sce.objects:
    #     if "Block_Portal" in obj.name and own["link_id"] == obj["id"]:
    #         own["link_reference"] = obj

    # # send a message that the portal has been loaded
    # logic.sendMessage("portal.setup", str(own["id"]))

def main():
    pass

    # own = logic.getCurrentController().owner

    # # go through all ships and check if they're close enough
    # for ship in gD["current"]["ships"]:
    #     ship_ref = gD["current"]["ships"][ship]["reference"] # game obj of the ship

    #     # teleportation happens here
    #     if own.getDistanceTo(ship_ref) < G.PORTAL_DISTANCE and not ship in p_data[own["id"]]["resets"]:

    #         store_vel = ship_ref.worldLinearVelocity

    #         ship_ref.worldPosition = own["link_reference"].worldPosition # teleport ship
    #         ship_ref.worldOrientation = own["link_reference"].worldOrientation

    #         ship_ref.worldLinearVelocity = own["link_reference"].worldOrientation * store_vel

    #         gD["current"]["ships"][ship]["last_portal_id"] = own["link_id"] # deprecated?

    #         # add ship to the reset list of the destination portal so it doesn't get teleported back
    #         p_data[own["link_id"]]["resets"].append(ship)

    #         if G.DEBUG: print(own.name, ": Teleporting",ship,"from",own["id"],"to",own["link_id"])

    #     # when a ship is out of reach, reset the triggering
    #     elif ship in p_data[own["id"]]["resets"] and own.getDistanceTo(ship_ref) > G.PORTAL_DISTANCE:
    #         p_data[own["id"]]["resets"] = []
