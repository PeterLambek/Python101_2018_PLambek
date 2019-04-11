#groupHierarachy
# create a group hierarchy

import maya.cmds as cmds

def hierarchySetup():

    # see if there alrady is a group hierarchy
    groupSetup = cmds.ls('main_Grp')
    # if the group is already there do nothing
    if groupSetup:
        print "Group already there"
        return      
    else:
        # create first main group
        cmds.group(n="main_Grp", empty=True, world=True)
        # create 1 sub groups
        cmds.group(n="output_Grp", empty=True, parent="main_Grp")
        cmds.group(n="dummy_Grp", empty=True, parent="main_Grp")
        cmds.group(n="geo_Grp", empty=True, parent="main_Grp")
        cmds.group(n="skeleton_Grp", empty=True, parent="main_Grp")
        cmds.group(n="rig_Grp", empty=True, parent="main_Grp")
        # create 2 sub group under main_Grp/rig_Grp
        cmds.group(n="extra_Grp", empty=True, parent="rig_Grp")
        cmds.group(n="space_Grp", empty=True, parent="rig_Grp")
        cmds.group(n="C_global_Grp", empty=True, parent="rig_Grp")
        # create 3 sub group under main_Grp/rig_Grp/space_Grp
        cmds.group(n="world_Spa", empty=True, parent="space_Grp")
        cmds.group(n="entity_Spa", empty=True, parent="space_Grp")
        # create 3 sub group under main_Grp/rig_Grp/C_global_Grp
        cmds.group(n="C_driven_Ctl", empty=True, parent="C_global_Grp")
        # create 4 sub group under main_Grp/rig_Grp/C_global_Grp
        cmds.group(n="C_entity_Ctl", empty=True, parent="C_driven_Ctl")
        # create 5 sub group under main_Grp/rig_Grp/C_global_Grp
        cmds.group(n="L_Ik_Grp", empty=True, parent="C_entity_Ctl")
        cmds.group(n="L_Fk_Grp", empty=True, parent="C_entity_Ctl")
        cmds.group(n="R_Ik_Grp", empty=True, parent="C_entity_Ctl")
        cmds.group(n="R_Fk_Grp", empty=True, parent="C_entity_Ctl")
        cmds.group(n="C_Ik_Grp", empty=True, parent="C_entity_Ctl")
        cmds.group(n="C_Fk_Grp", empty=True, parent="C_entity_Ctl")
 
