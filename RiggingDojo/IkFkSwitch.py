# creates a control that will switch between the ik and fk

import maya.cmds as cmds

# create the left control switch
def L_IkFkSwitchControl():
    
    # find the worldposition ws translate position of shoulder, elbow and wrist
    posTransShoulder = cmds.xform('L_Rig_shoulder_jnt', q=True, t=True, ws=True)
    posTransElbow = cmds.xform('L_Rig_elbow_jnt', q=True, t=True, ws=True)
    posTransWrist = cmds.xform('L_Rig_wrist_jnt', q=True, t=True, ws=True)
    # find the worldposition ws orient position of shoulder, elbow and wrist
    posOrientShoulder = cmds.xform('L_Rig_shoulder_jnt', q=True, t=True, ws=True)
    posOrientElbow = cmds.xform('L_Rig_elbow_jnt', q=True, t=True, ws=True)
    posOrientWrist = cmds.xform('L_Rig_wrist_jnt', q=True, t=True, ws=True)
    
    # create the empty group
    cmds.group(em=True, n='L_IkFkSwitch_Grp') 
    # create the control   
    cmds.circle(n='L_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.35)
    # parent the control to the group
    cmds.parent('L_IkFkSwitch_Ctl', 'L_IkFkSwitch_Grp')
    # freeze history and clear history of control
    cmds.makeIdentity('L_IkFkSwitch_Ctl', apply=True)
    cmds.delete('L_IkFkSwitch_Ctl', ch=True)
    # freeze the orientation of the controllers
    cmds.makeIdentity('L_IkFkSwitch_Ctl', apply=True, r=True, t=True)
    # delete history of the controllers
    cmds.delete('L_IkFkSwitch_Ctl', ch=True) 
    # create attributes on the controller for ik fk switch, and the visibility
    cmds.addAttr('L_IkFkSwitch_CtlShape', ln="lArmSwitch", at='enum', en='_________', k=True)
    #cmds.setAttr('L_IkFkSwitch_CtlShape.seperator1', e=True, ch=True) 
    cmds.addAttr('L_IkFkSwitch_CtlShape', ln="lArmikFkSwitch", at='enum', en='Ik:Fk:', k=True)
    cmds.addAttr('L_IkFkSwitch_CtlShape', ln="lArmCtlVis", at='enum', en='auto:both:', k=True)
    # connect the pairBlend to the ikFkSwitch
    cmds.connectAttr('L_IkFkSwitch_CtlShape.lArmikFkSwitch', 'L_shoulder_Pb.weight')
    cmds.connectAttr('L_IkFkSwitch_CtlShape.lArmikFkSwitch', 'L_elbow_Pb.weight')
    cmds.connectAttr('L_IkFkSwitch_CtlShape.lArmikFkSwitch', 'L_wrist_Pb.weight')
    # hide controls based on the selection ikFkVisibility attribute
    # create condition node and two reverse nodes for the setup
    cmds.shadingNode('reverse', n="L_ikFkVisibility01_Rev", au=True)
    cmds.shadingNode('reverse', n="L_ikFkVisibility02_Rev", au=True)
    cmds.shadingNode('condition', n="L_ikFkVisibility_Cnd", au=True)
    # set attributes on the condition node
    cmds.setAttr('L_ikFkVisibility_Cnd.operation', 0)
    cmds.setAttr('L_ikFkVisibility_Cnd.colorIfTrueR', 1)
    cmds.setAttr('L_ikFkVisibility_Cnd.colorIfTrueG', 1)
    # connect the ikFkSwitch to the nodes
    cmds.connectAttr('L_IkFkSwitch_CtlShape.lArmikFkSwitch', "L_ikFkVisibility01_Rev.input.inputX")
    cmds.connectAttr('L_IkFkSwitch_CtlShape.lArmikFkSwitch', "L_ikFkVisibility_Cnd.colorIfFalseR")
    cmds.connectAttr('L_IkFkSwitch_CtlShape.lArmCtlVis', "L_ikFkVisibility02_Rev.input.inputX")
    # connect the reverse nodes to the condition
    cmds.connectAttr("L_ikFkVisibility01_Rev.output.outputX", "L_ikFkVisibility_Cnd.colorIfFalseG")
    cmds.connectAttr("L_ikFkVisibility02_Rev.output.outputX", "L_ikFkVisibility_Cnd.firstTerm")
    # connect the condition node to ik and fk control top groups, outColorG = Ik outColorR = Fk
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_Ik_arm_Grp.visibility')
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_poleVec_Grp.visibility')
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_Ik_shoulder_jnt.visibility')
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_Grp.visibility')
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_jnt.visibility')
    # parent the shape node to the controls
    # ik controls
    cmds.parent('L_IkFkSwitch_CtlShape',  'L_Ik_arm_Ctl', add=True, s=True)
    cmds.parent('L_IkFkSwitch_CtlShape',  'L_Ik_elbow_Ctl', add=True, s=True)
    # fk controls
    cmds.parent('L_IkFkSwitch_CtlShape',  'L_Fk_shoulder_Ctl', add=True, s=True)
    cmds.parent('L_IkFkSwitch_CtlShape',  'L_Fk_elbow_Ctl', add=True, s=True)
    cmds.parent('L_IkFkSwitch_CtlShape',  'L_Fk_wrist_Ctl', add=True, s=True)
    #visibility
    cmds.setAttr('L_IkFkSwitch_CtlShape.visibility', 0)    
    # parent the group respectively
    cmds.parent('L_IkFkSwitch_Grp', 'L_Ik_Grp')