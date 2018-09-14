import maya.cmds as cmds

print "My Rig UI"

def rig_arm(*args):
    print "Rig_Arm"
    import rig.arm_rig as arm_rig
    reload(arm_rig)

mymenu = cmds.menu('RDojo_Menu', l='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig_Arm', p=mymenu, command=rig_arm)

