# globalDict Structure


* globalDict
  + input
    - focus
  + settings (settings loaded from config.ini)
    - Game
      * Name
      * LevelDir
      * ShipDir
      * Version
    - dev
      * debug
    - Controls_1 (list of available controls and their bindings)
      * test
  + current
    - level (pyObj:modules.level.Level, things nested below are depr.)
      * name
      * lap
      * cube_size
      * block_list (dicts of the blocks in use)
        + [block{type, position, orientation}, ...]
      * start_pos
      * start_orientation

      * checkpoint_count
      * checkpoint_data
      * checkpoint_count_registered

      * portal_data
        {portal_id : {reference : ref}
      * race_complete bool
			* cp_data
        + {'name': 'Block_Checkpoint', 'reference': Block_Checkpoint, 'times': {}}
    - ships
      * id (as dict key)
        + last_checkpoint
        + last_portal_id
        + reference
    - block_list (available blocks)
  + editor
    - selected_block
    - rotation
      * axis
  + content
    - (list of) levels
    - (list of) modes
    - (list of) ships
