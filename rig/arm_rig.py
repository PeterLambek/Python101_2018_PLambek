import maya.cmds as cmds


def createJoint():
    # create joints and name em
    #
    jnt_list = {'LJNTS': [['shoulder_jnt', [1.0, 0, 0]], ['elbow_jnt', [3.0, 0, -1.0]], ['wrist_jnt', [5.0, 0, 0]], ['wristEnd_jnt', [6.0, 0, 0.0]]],
                'RJNTS': [['shoulder_jnt', [-1.0, 0, 0]], ['elbow_jnt', [-3.0, 0, -1.0]], ['wrist_jnt', [-5.0, 0, 0]],['wristEnd_jnt', [-6.0, 0, 0]]]}
    # set the definition for the joints
    arm_list = ['Rig_', 'Ik_', 'Fk_']

    # left side joint setup
    # 

    for item in arm_list:
        for jnt in jnt_list['LJNTS']:
            jnt_name = 'L_' + item + jnt[0]
            cmds.joint(n=jnt_name, p=jnt[1], radius=1)

        cmds.select(d=True)

    # right side joint setup

    for item in arm_list:
        for jnt in jnt_list['RJNTS']:
            jnt_name = 'R_' + item + jnt[0]
            cmds.joint(n=jnt_name, p=jnt[1], radius=1)

        cmds.select(d=True)

createJoint()

def create_ik():


    # create Ik Rig
    #ik handle
    cmds.ikHandle(n='L_arm_Ikh', sj='L_Ik_shoulder_jnt', ee='L_Ik_wrist_jnt', sol='ikRPsolver', p=2, w=1)
    # find the worldspace ws translate position of the wrist
    pos_trans_ik = cmds.xform('L_Ik_wrist_jnt', q=True, t=True, ws=True)
    # find the worldspace ws orientation position of the wrist
    pos_orient_ik = cmds.xform('L_Ik_wrist_jnt', q=True, ro=True, ws=True)
    # create the empty group
    cmds.group(em=True, n='L_Ik_arm_Grp')
    # create the control
    cmds.circle(n='L_Ik_arm_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.35 )
    # orient the group to the wrist
    cmds.xform('L_Ik_arm_Grp', ro=pos_orient_ik, ws=True)
    # parent the control to the group
    cmds.parent('L_Ik_arm_Ctl', 'L_Ik_arm_Grp')
    # move the group to the wrist
    cmds.xform('L_Ik_arm_Grp', t=pos_trans_ik, ws=True)
    # parent the Ikhandle to the controller
    cmds.parent('L_arm_Ikh', 'L_Ik_arm_Ctl')
    # getting controller to control the orient of the wrist
    cmds.orientConstraint('L_Ik_arm_Ctl', 'L_Ik_wrist_jnt', mo=True)
    # create a locator as a poleVector
    cmds.spaceLocator(n='L_poleVec_Loc')
    # create a group as the group for a poleVector
    cmds.group(em=True, n='L_poleVec_Grp')
    # parent locator to the group
    cmds.parent('L_poleVec_Loc', 'L_poleVec_Grp')
    # place the group between the shoulder and the wrist
    cmds.pointConstraint('L_Ik_shoulder_jnt', 'L_Ik_wrist_jnt', 'L_poleVec_Grp')
    # aim the locator twoards the elbow
    cmds.aimConstraint('L_Ik_elbow_jnt', 'L_poleVec_Grp', aim=(1,0,0), u=(0,1,0))
    # delete the constraints
    cmds.delete('L_poleVec_Grp_pointConstraint1')
    cmds.delete('L_poleVec_Grp_aimConstraint1')
    # place the locater out from the elbow using the X axis trans
    cmds.move(-5, 'L_poleVec_Loc', z=True, a=True)
    #create controller for the polevector
    cmds.circle(n='L_Ik_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5 )
    # move parent the controller to the locator locatieon
    cmds.pointConstraint('L_poleVec_Loc', 'L_Ik_elbow_Ctl')
    # delete pointConstraint from controller
    cmds.delete('L_Ik_elbow_Ctl_pointConstraint1')
    # parent controller to grp
    cmds.parent('L_Ik_elbow_Ctl', 'L_poleVec_Grp')
    # freeze orientation on controller
    cmds.makeIdentity('L_Ik_elbow_Ctl', a=True)
    # parent poleVEc to controller
    cmds.parent('L_poleVec_Loc', 'L_Ik_elbow_Ctl')
    # connect the polevector constraint to the ikhandle and the locator
    cmds.poleVectorConstraint('L_poleVec_Loc', 'L_arm_Ikh')
    # hide locator
    cmds.hide('L_poleVec_Loc')

create_ik()


def create_fk():

    l_pos_trans_shoulder = cmds.xform('L_Fk_shoulder_jnt', q=True, t=True, ws=True)
    l_pos_trans_elbow = cmds.xform('L_Fk_elbow_jnt', q=True, t=True, ws=True)
    l_pos_trans_wrist = cmds.xform('L_Fk_wrist_jnt', q=True, t=True, ws=True)
    # find the worldposition ws orient position of shoulder, elbow and wrist
    l_pos_orient_shoulder = cmds.xform('L_Fk_shoulder_jnt', q=True, t=True, ws=True)
    l_pos_orient_elbow = cmds.xform('L_Fk_elbow_jnt', q=True, t=True, ws=True)
    l_pos_orient_wrist = cmds.xform('L_Fk_wrist_jnt', q=True, t=True, ws=True)

    r_pos_trans_shoulder = cmds.xform('R_Fk_shoulder_jnt', q=True, t=True, ws=True)
    r_pos_trans_elbow = cmds.xform('R_Fk_elbow_jnt', q=True, t=True, ws=True)
    r_pos_trans_wrist = cmds.xform('R_Fk_wrist_jnt', q=True, t=True, ws=True)
    # find the worldposition ws orient position of shoulder, elbow and wrist
    r_pos_orient_shoulder = cmds.xform('R_Fk_shoulder_jnt', q=True, t=True, ws=True)
    r_pos_orient_elbow = cmds.xform('R_Fk_elbow_jnt', q=True, t=True, ws=True)
    r_pos_orient_wrist = cmds.xform('R_Fk_wrist_jnt', q=True, t=True, ws=True)

    ctl_list = ['_Ctl', '_Grp']
    jnt_list = {'LFKJNTS': [['L_Fk_shoulder_jnt', [l_pos_trans_shoulder], [l_pos_orient_shoulder]], ['L_Fk_elbow_jnt', [l_pos_trans_elbow], [l_pos_orient_elbow]], ['L_Fk_wrist_jnt', [l_pos_trans_wrist], [l_pos_orient_wrist]]],
                'RFKJNTS': [['R_Fk_shoulder_jnt', [r_pos_trans_shoulder], [r_pos_orient_shoulder]], ['R_Fk_elbow_jnt', [r_pos_trans_elbow], [r_pos_orient_elbow]], ['R_Fk_wrist_jnt', [r_pos_trans_wrist], [r_pos_orient_wrist]]]}

    for s in jnt_list['LFKJNTS']:
        cmds.circle(n=s[0], nr=(0, 0, 1), c=(0, 0, 0), r=0.75)
        cmds.xform(s, ro=l_pos_orient_shoulder, ws=True)

    # create a group for each limb (3)
    cmds.group(em=True, n='L_Fk_shoulder_Grp')
    cmds.group(em=True, n='L_Fk_elbow_Grp')
    cmds.group(em=True, n='L_Fk_wrist_Grp')
    # create a controller for each limb (3)
    cmds.circle(n='L_Fk_shoulder_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75  )
    cmds.circle(n='L_Fk_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75 )
    cmds.circle(n='L_Fk_wrist_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75 )
    # orient the group after the respected name
    cmds.xform('L_Fk_shoulder_Grp', ro=l_pos_orient_shoulder, ws=True)
    cmds.xform('L_Fk_elbow_Grp', ro=l_pos_orient_elbow, ws=True)
    cmds.xform('L_Fk_wrist_Grp', ro=l_pos_orient_wrist, ws=True)
    # parent the controller to the groups
    cmds.parent('L_Fk_shoulder_Ctl','L_Fk_shoulder_Grp')
    cmds.parent('L_Fk_elbow_Ctl','L_Fk_elbow_Grp')
    cmds.parent('L_Fk_wrist_Ctl','L_Fk_wrist_Grp')
    # move the groups to the respected names location
    cmds.xform('L_Fk_shoulder_jnt', t=l_pos_trans_shoulder, ws=True)
    cmds.xform('L_Fk_elbow_jnt', t=l_pos_trans_elbow, ws=True)
    cmds.xform('L_Fk_wrist_jnt', t=l_pos_trans_wrist, ws=True)
    # freeze the orientation of the controllers
    cmds.makeIdentity('L_Fk_shoulder_Ctl', apply=True, r=True, t=True)
    cmds.makeIdentity('L_Fk_elbow_Ctl', apply=True, r=True, t=True)
    cmds.makeIdentity('L_Fk_wrist_Ctl', apply=True, r=True, t=True)
    # delete history of the controllers
    cmds.delete('L_Fk_shoulder_Ctl', ch=True)
    cmds.delete('L_Fk_elbow_Ctl', ch=True)
    cmds.delete('L_Fk_wrist_Ctl', ch=True)
    # position the groups to the limbs
    cmds.xform('L_Fk_shoulder_Grp', t=l_pos_trans_shoulder, ws=True)
    cmds.xform('L_Fk_elbow_Grp', t=l_pos_trans_elbow, ws=True)
    cmds.xform('L_Fk_wrist_Grp', t=l_pos_trans_wrist, ws=True)
    # set the controllers to control the joint limbs
    cmds.parentConstraint('L_Fk_shoulder_Ctl', 'L_Fk_shoulder_jnt', mo=True)
    cmds.parentConstraint('L_Fk_elbow_Ctl', 'L_Fk_elbow_jnt', mo=True)
    cmds.parentConstraint('L_Fk_wrist_Ctl', 'L_Fk_wrist_jnt', mo=True)
    # parent the controllers and groups together
    cmds.parent('L_Fk_wrist_Grp', 'L_Fk_elbow_Ctl')
    cmds.parent('L_Fk_elbow_Grp','L_Fk_shoulder_Ctl' )

create_fk()

    # connect the Ik and the Fk to the bind

def combine_ik_fk():

    # find the worldposition ws translate position of shoulder, elbow and wrist
    pos_trans_wrist = cmds.xform('L_Fk_wrist_jnt', q=True, t=True, ws=True)
    # find the worldposition ws orient position of shoulder, elbow and wrist
    pos_orient_wrist = cmds.xform('L_Fk_wrist_jnt', q=True, t=True, ws=True)

    # create 3 pairblend node to switch between ik and fk
    cmds.shadingNode('pairBlend', au=True, n='L_Rig_shoulder_Pb')
    cmds.shadingNode('pairBlend', au=True, n='L_Rig_elbow_Pb')
    cmds.shadingNode('pairBlend', au=True, n='L_Rig_wrist_Pb')
    # connect the Ik to the pairblend node
    cmds.connectAttr('L_Ik_shoulder_jnt.rotate','L_Rig_shoulder_Pb.inRotate1', f=True)
    cmds.connectAttr('L_Ik_elbow_jnt.rotate','L_Rig_elbow_Pb.inRotate1', f=True)
    cmds.connectAttr('L_Ik_wrist_jnt.rotate','L_Rig_wrist_Pb.inRotate1', f=True)
    # connect the fk to the pairblend node
    cmds.connectAttr('L_Fk_shoulder_jnt.rotate','L_Rig_shoulder_Pb.inRotate2', f=True)
    cmds.connectAttr('L_Fk_elbow_jnt.rotate','L_Rig_elbow_Pb.inRotate2', f=True)
    cmds.connectAttr('L_Fk_wrist_jnt.rotate','L_Rig_wrist_Pb.inRotate2', f=True)
    # connect the pairblend node to the rig
    cmds.connectAttr('L_Rig_shoulder_Pb.outRotate','L_Rig_shoulder_jnt.rotate', f=True)
    cmds.connectAttr('L_Rig_elbow_Pb.outRotate','L_Rig_elbow_jnt.rotate', f=True)
    cmds.connectAttr('L_Rig_wrist_Pb.outRotate','L_Rig_wrist_jnt.rotate', f=True)
    # create control to switch between the ik and fk
    cmds.circle(n='L_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75  )
    # create a group for the switch control
    cmds.group(em=True, n='L_IkFkSwitch_Grp')
    # parent the switch controller to the group
    cmds.parent('L_IkFkSwitch_Ctl', 'L_IkFkSwitch_Grp')
    # place the group above the hand
    cmds.xform('L_IkFkSwitch_Grp', t=pos_trans_wrist, ws=True)
    cmds.xform('L_IkFkSwitch_Grp', t=pos_orient_wrist, ws=True)
    # turn the control to be horizontal and move it up
    cmds.xform('L_IkFkSwitch_Ctl', r=True, ro=(-90, 0, 0))
    cmds.xform('L_IkFkSwitch_Ctl', r=True, t=(0, 2, 0))
    # freeze the controlle
    cmds.makeIdentity('L_IkFkSwitch_Ctl', a=True)
    # remove history
    cmds.delete('L_IkFkSwitch_Ctl', ch=True)
    # create attributes on the controller for ik fk switch, and the visibility
    cmds.addAttr('L_IkFkSwitch_Ctl', ln="ikFkSwitch", at='enum', en='Ik:Fk:', k=True)
    cmds.addAttr('L_IkFkSwitch_Ctl', ln="ikFkVisibility", at='enum', en='auto:both:', k=True)
    # connect the pairBlend to the ikFkSwitch
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_Rig_shoulder_Pb.weight')
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_Rig_elbow_Pb.weight')
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_Rig_wrist_Pb.weight')
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
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', "L_ikFkVisibility01_Rev.input.inputX")
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', "L_ikFkVisibility_Cnd.colorIfFalseR")
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkVisibility', "L_ikFkVisibility02_Rev.input.inputX")
    # connect the reverse nodes to the condition
    cmds.connectAttr("L_ikFkVisibility01_Rev.output.outputX", "L_ikFkVisibility_Cnd.colorIfFalseG")
    cmds.connectAttr("L_ikFkVisibility02_Rev.output.outputX", "L_ikFkVisibility_Cnd.firstTerm")
    # connect the condition node to ik and fk control top groups, outColorG = Ik outColorR = Fk
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_Ik_arm_Grp.visibility')
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_poleVec_Grp.visibility')
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_Ik_shoulder_jnt.visibility')
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_Grp.visibility')
    cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_jnt.visibility')

combine_ik_fk()

