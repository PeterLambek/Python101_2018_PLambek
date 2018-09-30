import maya.cmds as cmds
from rig import arm_rig_test

print "My Rig UI"

def l_rig_arm(*args):
    print "L_Rig_Arm"
    import rig.arm_rig_test as arm_rig
    reload(arm_rig)
    arm_rig = arm_rig_test.Rig_Arm()
    arm_rig.l_arm_rig()

def r_rig_arm(*args):
    print "R_Rig_Arm"
    import rig.arm_rig_test as arm_rig
    reload(arm_rig)
    arm_rig = arm_rig_test.Rig_Arm()
    arm_rig.r_arm_rig()

def l_connect(*args):
    print "L_Connect"
    import rig.arm_rig_test as arm_rig
    reload(arm_rig)
    arm_rig = arm_rig_test.Rig_Arm()
    arm_rig.lconnect()

def r_connect(*args):
    print "R_Connect"
    import rig.arm_rig_test as arm_rig
    reload(arm_rig)
    arm_rig = arm_rig_test.Rig_Arm()
    arm_rig.rconnect()


menuarray = cmds.window('MayaWindow', q=True, ma=True)
if 'RDojo_Menu' not in menuarray:
    mymenu = cmds.menu('RDojo_Menu', l='RDMenu', to=True, p='MayaWindow')
    cmds.menuItem(label='L_Rig_Arm', p=mymenu, command=l_rig_arm)
    cmds.menuItem(label='R_Rig_Arm', p=mymenu, command=r_rig_arm)
    cmds.menuItem(label='L_Connect_Ik_Fk', p=mymenu, command=l_connect)
    cmds.menuItem(label='R_Connect_Ik_Fk', p=mymenu, command=r_connect)

