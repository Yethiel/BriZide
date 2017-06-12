from bge import logic

gD = logic.globalDict

def delete_block(argument=None):
    if not "undeletable" in gD["editor"]["active_block"]:
        gD["editor"]["active_block"].endObject()
    else:
        if G.DEBUG: print(own.name, "Cannot delete block.")
