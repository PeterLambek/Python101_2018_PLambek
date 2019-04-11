import maya.cmds as cmds

 

def L_Ik_armStretch():

    # get the position of the shoulder and wrist

    posTransShoulder = cmds.xform('L_Ik_shoulder_jnt', q=True, t=True, ws=True)
    posTransWrist = cmds.xform('L_Ik_wrist_jnt', q=True, t=True, ws=True)

    # create the distanceDimension by using the position

    dist = cmds.distanceDimension(startPoint=(posTransShoulder), endPoint=(posTransWrist))

    # rename the distanceDimension, and the locators

    armDist = cmds.rename("distanceDimension1", "L_Ik_shldrWrist_Dist")
    shldrDist = cmds.rename("locator1", "L_Ik_shldrDist_Loc")
    wristDist = cmds.rename("locator2", "L_Ik_wristDist_Loc")

    # place them in a group and place them in the hierarchy

    distGrp = cmds.group(armDist, shldrDist, wristDist, n="L_Ik_distanceSetup_Grp")

    # parentConstrint the locators to the joints

    cmds.parentConstraint('L_Ik_shoulder_jnt', 'L_Ik_shldrDist_Loc', maintainOffset=False)
    cmds.parentConstraint('L_Ik_wrist_jnt', 'L_Ik_wristDist_Loc', maintainOffset=False)

    # place the group in the main hierarchy

    cmds.parent(distGrp, "L_Ik_Grp")

    # create the nodes needed for the stretch

    L_remapV = cmds.shadingNode('remapValue', asUtility=True, n="L_Ik_arm_sS_RemapValue")
    L_sS_Md = cmds.shadingNode('multiplyDivide', asUtility=True, n="L_sS_Md")
    L_sS_Clamp = cmds.shadingNode('clamp', asUtility=True, n="L_sS_Clamp")
    L_sS_onOff_Cnd = cmds.shadingNode('condition', asUtility=True, n="L_sS_ONOFF_Cnd")
    L_SS_Cnd = cmds.shadingNode('condition', asUtility=True, n="L_SS_Cnd")
    L_offPost_Md =cmds.shadingNode('multiplyDivide', asUtility=True, n="L_offsetPost_Md")
    L_offPre_Md = cmds.shadingNode('multiplyDivide', asUtility=True, n="L_offsetPre_Md")
    L_wrist_transAbs_Md = cmds.shadingNode('multiplyDivide', asUtility=True, n="L_wrist_transAbs_Md")
    L_elbow_transAbs_Md = cmds.shadingNode('multiplyDivide', asUtility=True, n="L_elbow_transAbs_Md")
    L_postMid_Bta = cmds.shadingNode('blendTwoAttr', asUtility=True, n="L_postMid_Bta")
    L_preMid_Bta = cmds.shadingNode('blendTwoAttr', asUtility=True, n="L_preMid_Bta")

    # create the attributes on the ik hand control

    cmds.addAttr('L_Ik_arm_Ctl', longName=STRETCH, edit=True, attributeType='enum')

    # connect the nodes
    # connecting the distanceDim to the multiplyDivide, and set the attributes

    cmds.connectAttr(armDist+'.distance', L_sS_Md+'.input1X')
   

#naming_armSetup 

import maya.cmds as cmds
 

def L_rig_arm():   

    # select 5 joints, clavicle, shoulder, elbow, wrist, wristEnd in that order

    l_arm_sel = cmds.ls(selection=True)

    # make sure the selection is 5 by using the len() command

    if len(l_arm_sel) == 5:

        # rename the selected joints

        clavicle = cmds.rename(l_arm_sel[0], 'L_Rig_clavicle_jnt')

        shoulder = cmds.rename(l_arm_sel[1], 'L_Rig_shoulder_jnt')

        elbow = cmds.rename(l_arm_sel[2], 'L_Rig_elbow_jnt')

        wrist = cmds.rename(l_arm_sel[3], 'L_Rig_wrist_jnt')

        wristEnd = cmds.rename(l_arm_sel[4], 'L_Rig_wristEnd')

   

        cmds.select(clavicle)

        cmds.joint(e=True, oj='xyz', sao='zdown', ch=True, zso=True)

   

    else:

        print "select 5 joints - Clavicle, shoulder, elbow, wrist, wristEnd"

        return

 

    # place them in the group hierarchy if there is one

    placeInGroup = cmds.ls('main_Grp')

    # if it is there parent them respectly

    if placeInGroup:

        cmds.parent('L_Rig_clavicle_jnt', 'skeleton_Grp')

   

    else:

        return

   

def R_rig_arm_mirror():

   

    #easy mirror tool

    #should make it more correct, so you would not mirror it but set the orientation correct in case you dont have the

    

    r_arm_sel = cmds.ls(selection=True)

   

    cmds.mirrorJoint('L_Rig_clavicle_jnt', mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))

 

#L_IkFk_armSetup

 

import maya.cmds as cmds

 

def L_fk_arm():   

    # Duplicate the arm and add FK in the name

    fk_arm = cmds.duplicate('L_Rig_clavicle_jnt', renameChildren=True)   

    cmds.listRelatives(fk_arm, allDescendents=True)   

    fkClavicle = cmds.rename(fk_arm[0], 'L_Fk_clavicle_jnt')
    fkShoulder = cmds.rename(fk_arm[1], 'L_Fk_shoulder_jnt')
    fkElbow = cmds.rename(fk_arm[2], 'L_Fk_elbow_jnt')
    fkWrist = cmds.rename(fk_arm[3], 'L_Fk_wrist_jnt')
    fkWristEnd = cmds.rename(fk_arm[4], 'L_Fk_wristEnd_jnt')   

    # create Fk Rig
 

    # find the worldposition ws translate position of shoulder, elbow and wrist

    posTransShoulder = cmds.xform('L_Fk_shoulder_jnt', q=True, t=True, ws=True)
    posTransElbow = cmds.xform('L_Fk_elbow_jnt', q=True, t=True, ws=True)
    posTransWrist = cmds.xform('L_Fk_wrist_jnt', q=True, t=True, ws=True)

    # find the worldposition ws orient position of shoulder, elbow and wrist

    posOrientShoulder = cmds.xform('L_Fk_shoulder_jnt', q=True, ro=True, ws=True)
    posOrientElbow = cmds.xform('L_Fk_elbow_jnt', q=True, ro=True, ws=True)
    posOrientWrist = cmds.xform('L_Fk_wrist_jnt', q=True, ro=True, ws=True)

    # create a group for each limb (3)

    cmds.group(em=True, n='L_Fk_shoulder_Grp')
    cmds.group(em=True, n='L_Fk_elbow_Grp')
    cmds.group(em=True, n='L_Fk_wrist_Grp')

    # create a controller for each limb (3)

    cmds.circle(n='L_Fk_shoulder_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
    cmds.circle(n='L_Fk_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
    cmds.circle(n='L_Fk_wrist_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)

    # rotate the controls correctly

    cmds.xform('L_Fk_shoulder_Ctl', ro=(0, 90, 0), ws=True)
    cmds.xform('L_Fk_elbow_Ctl', ro=(0, 90, 0), ws=True)
    cmds.xform('L_Fk_wrist_Ctl', ro=(0, 90, 0), ws=True)

   # orient the group after the respected name

    cmds.xform('L_Fk_shoulder_Grp', ro=posOrientShoulder, ws=True)
    cmds.xform('L_Fk_elbow_Grp', ro=posOrientElbow, ws=True)
    cmds.xform('L_Fk_wrist_Grp', ro=posOrientWrist, ws=True)

    # parent the controller to the groups

    cmds.parent('L_Fk_shoulder_Ctl', 'L_Fk_shoulder_Grp')
    cmds.parent('L_Fk_elbow_Ctl', 'L_Fk_elbow_Grp')
    cmds.parent('L_Fk_wrist_Ctl', 'L_Fk_wrist_Grp')

    # freeze history and clear history of control

    cmds.makeIdentity('L_Fk_shoulder_Ctl', a=True)
    cmds.makeIdentity('L_Fk_elbow_Ctl', a=True)
    cmds.makeIdentity('L_Fk_wrist_Ctl', a=True)
    

    cmds.delete('L_Fk_shoulder_Ctl', ch=True)
    cmds.delete('L_Fk_elbow_Ctl', ch=True)
    cmds.delete('L_Fk_wrist_Ctl', ch=True)

    # move the groups to the respected names location

    cmds.xform('L_Fk_shoulder_jnt', t=posTransShoulder, ws=True)
    cmds.xform('L_Fk_elbow_jnt', t=posTransElbow, ws=True)
    cmds.xform('L_Fk_wrist_jnt', t=posTransWrist, ws=True)

    # freeze the orientation of the controllers

    cmds.makeIdentity('L_Fk_shoulder_Ctl', apply=True, r=True, t=True)
    cmds.makeIdentity('L_Fk_elbow_Ctl', apply=True, r=True, t=True)
    cmds.makeIdentity('L_Fk_wrist_Ctl', apply=True, r=True, t=True)

   # delete history of the controllers

    cmds.delete('L_Fk_shoulder_Ctl', ch=True)
    cmds.delete('L_Fk_elbow_Ctl', ch=True)
    cmds.delete('L_Fk_wrist_Ctl', ch=True)

    # position the groups to the limbs

    cmds.xform('L_Fk_shoulder_Grp', t=posTransShoulder, ws=True)
    cmds.xform('L_Fk_elbow_Grp', t=posTransElbow, ws=True)
    cmds.xform('L_Fk_wrist_Grp', t=posTransWrist, ws=True)

    # set the controllers to control the joint limbs

    cmds.parentConstraint('L_Fk_shoulder_Ctl', 'L_Fk_shoulder_jnt', mo=True)
    cmds.parentConstraint('L_Fk_elbow_Ctl', 'L_Fk_elbow_jnt', mo=True)
    cmds.parentConstraint('L_Fk_wrist_Ctl', 'L_Fk_wrist_jnt', mo=True)

    # parent the controllers and groups together

    cmds.parent('L_Fk_wrist_Grp', 'L_Fk_elbow_Ctl')
    cmds.parent('L_Fk_elbow_Grp', 'L_Fk_shoulder_Ctl')

    # lock and hide translate, scale and visibility

    # Shoulder

    cmds.setAttr('L_Fk_shoulder_Ctl.translateX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_shoulder_Ctl.translateY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_shoulder_Ctl.translateZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_shoulder_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_shoulder_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_shoulder_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_shoulder_Ctl.visibility', lock=True, channelBox=False, keyable=False)

    # Elbow

    cmds.setAttr('L_Fk_elbow_Ctl.translateX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_elbow_Ctl.translateY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_elbow_Ctl.translateZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_elbow_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_elbow_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_elbow_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_elbow_Ctl.visibility', lock=True, channelBox=False, keyable=False)

    # Wrist

    cmds.setAttr('L_Fk_wrist_Ctl.translateX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_wrist_Ctl.translateY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_wrist_Ctl.translateZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_wrist_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_wrist_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_wrist_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Fk_wrist_Ctl.visibility', lock=True, channelBox=False, keyable=False)
 

    # place them in the group hierarchy if there is one

    placeInGroup = cmds.ls('main_Grp')

    # if it is there parent them respectly

    if placeInGroup:
        cmds.parent('L_Fk_shoulder_Grp', 'L_Fk_Grp')       

    else:
        return
 

   

def L_ik_arm():

   

    # Duplicate the arm and add FK in the name

    ik_arm = cmds.duplicate('L_Rig_clavicle_jnt', renameChildren=True)   

    cmds.listRelatives(ik_arm, allDescendents=True)   

    ikClavicle = cmds.rename(ik_arm[0], 'L_Ik_clavicle_jnt')
    ikShoulder = cmds.rename(ik_arm[1], 'L_Ik_shoulder_jnt')
    ikElbow = cmds.rename(ik_arm[2], 'L_Ik_elbow_jnt')
    ikWrist = cmds.rename(ik_arm[3], 'L_Ik_wrist_jnt')
    ikWristEnd = cmds.rename(ik_arm[4], 'L_Ik_wristEnd_jnt')      

    # create Ik Rig 

    cmds.ikHandle(n='L_arm_Ikh', sj='L_Ik_shoulder_jnt', ee='L_Ik_wrist_jnt', sol='ikRPsolver', p=2, w=1)
    # find the worldspace ws translate position of the wrist
    posTransIk = cmds.xform('L_Ik_wrist_jnt', q=True, t=True, ws=True)
    # find the worldspace ws orientation position of the wrist
    posOrientIk = cmds.xform('L_Ik_wrist_jnt', q=True, ro=True, ws=True)
    # create the empty group
    cmds.group(em=True, n='L_Ik_arm_Grp')
    # create the control
    lIkControl = cmds.circle(n='L_Ik_arm_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.35)
    # orient the control to the wrist
    cmds.xform('L_Ik_arm_Ctl', ro=(0, 90, 0), ws=True)
    # orient the group to the wrist
    cmds.xform('L_Ik_arm_Grp', ro=posOrientIk, ws=True)
    # parent the control to the group
    cmds.parent('L_Ik_arm_Ctl', 'L_Ik_arm_Grp')
    # freeze history and clear history of control
    cmds.makeIdentity('L_Ik_arm_Ctl', a=True)
    cmds.delete('L_Ik_arm_Ctl', ch=True)
    # move the group to the wrist
    cmds.xform('L_Ik_arm_Grp', t=posTransIk, ws=True)
    # parent the Ikhandle to the controller
    cmds.parent('L_arm_Ikh', 'L_Ik_arm_Ctl')
    # getting controller to control the orient of the wrist
    cmds.orientConstraint('L_Ik_arm_Ctl', 'L_Ik_wrist_jnt', mo=True)
    # create a locator as a poleVector
    cmds.spaceLocator(n='L_arm_poleVec_Loc')
    # create a group as the group for a poleVector
    cmds.group(em=True, n='L_arm_poleVec_Grp')
    # parent locator to the group
    cmds.parent('L_arm_poleVec_Loc', 'L_arm_poleVec_Grp')
    # place the group between the shoulder and the wrist
    cmds.pointConstraint('L_Ik_shoulder_jnt', 'L_Ik_wrist_jnt', 'L_arm_poleVec_Grp')
    # aim the locator twoards the elbow
    cmds.aimConstraint('L_Ik_elbow_jnt', 'L_arm_poleVec_Grp', aim=(1, 0, 0), u=(0, 1, 0))
    # delete the constraints
    cmds.delete('L_arm_poleVec_Grp_pointConstraint1')
    cmds.delete('L_arm_poleVec_Grp_aimConstraint1')
    # place the locater out from the elbow using the X axis trans
    cmds.move(25, 'L_arm_poleVec_Loc', x=True, os=True, ws=False)
    # create controller for the polevector
    cmds.curve(n='L_Ik_elbow_Ctl', d = 1,p = [[0.5000000000000019, -0.250000000000001, 5.551115123125783e-17], [0.5000000000000019, 0.249999999999999, -5.551115123125783e-17],
    [0.25000000000000183, 0.24999999999999906, -5.551115123125783e-17],
    [0.25000000000000183, 0.4999999999999991, -1.1102230246251565e-16], [-0.2499999999999983, 0.49999999999999917, -1.1102230246251565e-16], [-0.2499999999999983, 0.2499999999999992, -5.551115123125783e-17],
    [-0.4999999999999984, 0.24999999999999922, -5.551115123125783e-17], [-0.4999999999999984, -0.2500000000000008, 5.551115123125783e-17], [-0.2499999999999983, -0.25000000000000083, 5.551115123125783e-17],
    [-0.2499999999999983, -0.5000000000000009, 1.1102230246251565e-16], [0.25000000000000183, -0.5000000000000009, 1.1102230246251565e-16], [0.25000000000000183, -0.25000000000000094, 5.551115123125783e-17],
    [0.5000000000000019, -0.250000000000001, 5.551115123125783e-17]],k = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0))
    # scale the controller a bit down
    cmds.scale(0.8, 0.8, 0.8, 'L_Ik_elbow_Ctl')
    # move parent the controller to the locator locatieon
    cmds.pointConstraint('L_arm_poleVec_Loc', 'L_Ik_elbow_Ctl')
    # delete pointConstraint from controller
    cmds.delete('L_Ik_elbow_Ctl_pointConstraint1')
    # parent controller to grp
    cmds.parent('L_Ik_elbow_Ctl', 'L_arm_poleVec_Grp')
    # freeze orientation on controller
    cmds.makeIdentity('L_Ik_elbow_Ctl', a=True)
    # parent poleVEc to controller
    cmds.parent('L_arm_poleVec_Loc', 'L_Ik_elbow_Ctl')
    # connect the polevector constraint to the ikhandle and the locator
    cmds.poleVectorConstraint('L_arm_poleVec_Loc', 'L_arm_Ikh')
    # hide locator
    cmds.hide('L_arm_poleVec_Loc')
    # lock and hide scale and visibility

    # ik hand ctl
    cmds.setAttr('L_Ik_arm_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Ik_arm_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Ik_arm_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Ik_arm_Ctl.visibility', lock=False, channelBox=False, keyable=False)

    # Elbow ik ctl
    cmds.setAttr('L_Ik_elbow_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Ik_elbow_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Ik_elbow_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('L_Ik_elbow_Ctl.visibility', lock=False, channelBox=False, keyable=False)

 

    # place them in the group hierarchy if there is one
    placeInGroup = cmds.ls('main_Grp')

    # if it is there parent them respectly
    if placeInGroup:
        cmds.parent('L_Ik_arm_Grp', 'L_Ik_Grp')
        cmds.parent('L_arm_poleVec_Grp', 'L_Ik_Grp')

       

    else:
        return

  

#groupHierarachy

# create a group hierarchy

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
 

#connection_armSetup

 

import maya.cmds as cmds


# connect the Ik and the Fk to the bind

def L_connectFk_armSetup():
    # this is done to many times, and should be boiled down when introducing class
    # find the worldposition ws translate position of shoulder, elbow and wrist
    posTransShoulder = cmds.xform('L_Fk_shoulder_jnt', q=True, t=True, ws=True)
    posTransElbow = cmds.xform('L_Fk_elbow_jnt', q=True, t=True, ws=True)
    posTransWrist = cmds.xform('L_Fk_wrist_jnt', q=True, t=True, ws=True)
    # find the worldposition ws orient position of shoulder, elbow and wrist
    posOrientShoulder = cmds.xform('L_Fk_shoulder_jnt', q=True, t=True, ws=True)
    posOrientElbow = cmds.xform('L_Fk_elbow_jnt', q=True, t=True, ws=True)
    posOrientWrist = cmds.xform('L_Fk_wrist_jnt', q=True, t=True, ws=True)
    # create or find 3 pairblend node to switch between ik and fk
    # shoulder connection
    shldrPairNode = cmds.ls('L_shoulder_Pb')
    # if there already is a pairBlend node connect them together
    if shldrPairNode:
        cmds.connectAttr('L_Fk_shoulder_jnt.rotate', 'L_shoulder_Pb.inRotate2', force=True)
    # if there are no pairBlend node then we create the node and connects them together
    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='L_shoulder_Pb')
        cmds.connectAttr('L_Fk_shoulder_jnt.rotate', 'L_shoulder_Pb.inRotate2', force=True)
    # elbow connection   
    elbowPairNode = cmds.ls('L_elbow_Pb')
    # if there already is a pairBlend node connect them together
    if elbowPairNode:
        cmds.connectAttr('L_Fk_elbow_jnt.rotate', 'L_elbow_Pb.inRotate2', force=True)
    # if there are no pairBlend node then we create the node and connects them together
    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='L_elbow_Pb')
        cmds.connectAttr('L_Fk_elbow_jnt.rotate', 'L_elbow_Pb.inRotate2', force=True)
    # wrist connection
    wristPairNode = cmds.ls('L_wrist_Pb')
    # if there already is a pairBlend node connect them together
    if wristPairNode:
        cmds.connectAttr('L_Fk_wrist_jnt.rotate', 'L_wrist_Pb.inRotate2', force=True)
    # if there are no pairBlend node then we create the node and connects them together
    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='L_wrist_Pb')
        cmds.connectAttr('L_Fk_wrist_jnt.rotate', 'L_wrist_Pb.inRotate2', force=True)     
    # connect the pairBlend node to the Rig joints
    # shoulder connection
    shldrConnect = cmds.listConnections('L_Rig_shoulder_jnt.rotate')
    if shldrConnect:
        print "this has a connection"
        return
    else:
        cmds.connectAttr('L_shoulder_Pb.outRotate', 'L_Rig_shoulder_jnt.rotate', f=True)      
    # elbow connection      
        elbowConnect = cmds.listConnections('L_Rig_elbow_jnt.rotate')
    if elbowConnect:
        print "this has a connection"
        return      
    else:
        cmds.connectAttr('L_elbow_Pb.outRotate', 'L_Rig_elbow_jnt.rotate', f=True)

    # wrist connection
    wristConnect = cmds.listConnections('L_Rig_wrist_jnt.rotate')
    if wristConnect:
        print "this has a connection"
        return      

    else:

        cmds.connectAttr('L_wrist_Pb.outRotate', 'L_Rig_wrist_jnt.rotate', f=True)

       

    # Find or create a control for switching between the Ik and Fk

   

    createCtl = cmds.ls('L_IkFkSwitch_Ctl')

   

    if createCtl:

        print "control is there"

        return

       

    else:

        cmds.circle(n='L_arm_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75)
        # create a group for the switch control
        cmds.group(em=True, n='L_arm_IkFkSwitch_Grp')
        # parent the switch controller to the group
        cmds.parent('L_arm_IkFkSwitch_Ctl', 'L_arm_IkFkSwitch_Grp')
        # place the group above the hand
        cmds.xform('L_arm_IkFkSwitch_Grp', t=posTransWrist, ws=True)
        cmds.xform('L_arm_IkFkSwitch_Grp', t=posOrientWrist, ws=True)
        # turn the control to be horizontal and move it up
        cmds.xform('L_arm_IkFkSwitch_Ctl', r=True, ro=(-90, 0, 0))
        cmds.xform('L_arm_IkFkSwitch_Ctl', r=True, t=(0, 2, 0))
        # freeze the controlle
        cmds.makeIdentity('L_arm_IkFkSwitch_Ctl', a=True)
        # remove history
        cmds.delete('L_arm_IkFkSwitch_Ctl', ch=True) 
        # create attributes on the controller for ik fk switch, and the visibility
        cmds.addAttr('L_arm_IkFkSwitch_Ctl', ln="ikFkSwitch", at='enum', en='Ik:Fk:', k=True)
        cmds.addAttr('L_arm_IkFkSwitch_Ctl', ln="ikFkVisibility", at='enum', en='auto:both:', k=True)
        # connect the pairBlend to the ikFkSwitch
        cmds.connectAttr('L_arm_IkFkSwitch_Ctl.ikFkSwitch', 'L_shoulder_Pb.weight')
        cmds.connectAttr('L_arm_IkFkSwitch_Ctl.ikFkSwitch', 'L_elbow_Pb.weight')
        cmds.connectAttr('L_arm_IkFkSwitch_Ctl.ikFkSwitch', 'L_wrist_Pb.weight')
        # hide controls based on the selection ikFkVisibility attribute
        # create condition node and two reverse nodes for the setup
        cmds.shadingNode('reverse', n="L_arm_ikFkVisibility01_Rev", au=True)
        cmds.shadingNode('reverse', n="L_arm_ikFkVisibility02_Rev", au=True)
        cmds.shadingNode('condition', n="L_arm_ikFkVisibility_Cnd", au=True)
        # set attributes on the condition node
        cmds.setAttr('L_arm_ikFkVisibility_Cnd.operation', 0)
        cmds.setAttr('L_arm_ikFkVisibility_Cnd.colorIfTrueR', 1)
        cmds.setAttr('L_arm_ikFkVisibility_Cnd.colorIfTrueG', 1)
        # connect the ikFkSwitch to the nodes
        cmds.connectAttr('L_arm_IkFkSwitch_Ctl.ikFkSwitch', "L_arm_ikFkVisibility01_Rev.input.inputX")
        cmds.connectAttr('L_arm_IkFkSwitch_Ctl.ikFkSwitch', "L_arm_ikFkVisibility_Cnd.colorIfFalseR")
        cmds.connectAttr('L_arm_IkFkSwitch_Ctl.ikFkVisibility', "L_arm_ikFkVisibility02_Rev.input.inputX")
        # connect the reverse nodes to the condition
        cmds.connectAttr("L_arm_ikFkVisibility01_Rev.output.outputX", "L_arm_ikFkVisibility_Cnd.colorIfFalseG")
        cmds.connectAttr("L_arm_ikFkVisibility02_Rev.output.outputX", "L_arm_ikFkVisibility_Cnd.firstTerm")
        # connect the condition node to ik and fk control top groups, outColorG = Ik outColorR = Fk
        cmds.connectAttr('L_arm_ikFkVisibility_Cnd.outColorG', 'L_Ik_arm_Grp.visibility')
        cmds.connectAttr('L_arm_ikFkVisibility_Cnd.outColorG', 'L_arm_poleVec_Grp.visibility')
        cmds.connectAttr('L_arm_ikFkVisibility_Cnd.outColorG', 'L_Ik_shoulder_jnt.visibility')
        cmds.connectAttr('L_arm_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_Grp.visibility')
        cmds.connectAttr('L_arm_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_jnt.visibility')
        # lock and hide the translate, rotate, scale and hide visibility
        #translate
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.translateX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.translateY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.translateZ', lock=True, channelBox=False, keyable=False)
        #rotate
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.rotateX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.rotateY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.rotateZ', lock=True, channelBox=False, keyable=False)
        #scale
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('L_arm_IkFkSwitch_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
        #visibility
        cmds.setAttr('L_IkFkSwitch_Ctl.visibility', lock=False, channelBox=False, keyable=False)
        # parent the group respectively
        cmds.parent('L_arm_IkFkSwitch_Grp', 'L_Ik_Grp')
        # get the control to follow the hand by getting the top group parentConstrainted
        cmds.parentConstraint('L_Rig_wrist_jnt', 'L_arm_IkFkSwitch_Grp', maintainOffset=True)
 

    

def L_connectIk_armSetup():

    # this is done to many times, and should be boiled down when introducing class

    # find the worldposition ws translate position of shoulder, elbow and wrist

    posTransShoulder = cmds.xform('L_Ik_shoulder_jnt', q=True, t=True, ws=True)

    posTransElbow = cmds.xform('L_Ik_elbow_jnt', q=True, t=True, ws=True)

    posTransWrist = cmds.xform('L_Ik_wrist_jnt', q=True, t=True, ws=True)

    # find the worldposition ws orient position of shoulder, elbow and wrist

    posOrientShoulder = cmds.xform('L_Fk_shoulder_jnt', q=True, t=True, ws=True)

    posOrientElbow = cmds.xform('L_Ik_elbow_jnt', q=True, t=True, ws=True)

    posOrientWrist = cmds.xform('L_Ik_wrist_jnt', q=True, t=True, ws=True)

    # create or find 3 pairblend node to connect the fk joints to

   

    # shoulder connection

    shldrPairNode = cmds.ls('L_shoulder_Pb')

    # if there already is a pairBlend node connect them together

    if shldrPairNode:

        cmds.connectAttr('L_Ik_shoulder_jnt.rotate', 'L_shoulder_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='L_shoulder_Pb')

        cmds.connectAttr('L_Ik_shoulder_jnt.rotate', 'L_shoulder_Pb.inRotate1', force=True)

       

    # elbow connection   

    elbowPairNode = cmds.ls('L_elbow_Pb')

    # if there already is a pairBlend node connect them together

    if elbowPairNode:

        cmds.connectAttr('L_Ik_elbow_jnt.rotate', 'L_elbow_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='L_elbow_Pb')

        cmds.connectAttr('L_Ik_elbow_jnt.rotate', 'L_elbow_Pb.inRotate1', force=True)

   

    # wrist connection   

    wristPairNode = cmds.ls('L_wrist_Pb')

    # if there already is a pairBlend node connect them together

    if wristPairNode:

        cmds.connectAttr('L_Ik_wrist_jnt.rotate', 'L_wrist_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='L_wrist_Pb')

        cmds.connectAttr('L_Ik_wrist_jnt.rotate', 'L_wrist_Pb.inRotate1', force=True)

       

    # connect the pairBlend node to the Rig joints

    # shoulder connection

    shldrConnect = cmds.listConnections('L_Rig_shoulder_jnt.rotate')

    if shldrConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('L_shoulder_Pb.outRotate', 'L_Rig_shoulder_jnt.rotate', f=True)

       

    # elbow connection      

        elbowConnect = cmds.listConnections('L_Rig_elbow_jnt.rotate')

    if elbowConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('L_elbow_Pb.outRotate', 'L_Rig_elbow_jnt.rotate', f=True)

 

    # wrist connection

    wristConnect = cmds.listConnections('L_Rig_wrist_jnt.rotate')

    if wristConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('L_wrist_Pb.outRotate', 'L_Rig_wrist_jnt.rotate', f=True)

       

    # Find or create a control for switching between the Ik and Fk

   

    createCtl = cmds.ls('L_IkFkSwitch_Ctl')

   

    if createCtl:

        print "control is there"

        return

       

    else:

        cmds.circle(n='L_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75)

        # create a group for the switch control

        cmds.group(em=True, n='L_IkFkSwitch_Grp')

        # parent the switch controller to the group

        cmds.parent('L_IkFkSwitch_Ctl', 'L_IkFkSwitch_Grp')

        # place the group above the hand

        cmds.xform('L_IkFkSwitch_Grp', t=posTransWrist, ws=True)

        cmds.xform('L_IkFkSwitch_Grp', t=posOrientWrist, ws=True)

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

        cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_shoulder_Pb.weight')

        cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_elbow_Pb.weight')

        cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_wrist_Pb.weight')

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

        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_arm_poleVec_Grp.visibility')

        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_Ik_shoulder_jnt.visibility')

        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_Grp.visibility')

        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_jnt.visibility')

       

        # lock and hide the translate, rotate, scale and hide visibility

        #translate

        cmds.setAttr('L_IkFkSwitch_Ctl.translateX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('L_IkFkSwitch_Ctl.translateY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('L_IkFkSwitch_Ctl.translateZ', lock=True, channelBox=False, keyable=False)

        #rotate

        cmds.setAttr('L_IkFkSwitch_Ctl.rotateX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('L_IkFkSwitch_Ctl.rotateY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('L_IkFkSwitch_Ctl.rotateZ', lock=True, channelBox=False, keyable=False)

        #scale

        cmds.setAttr('L_IkFkSwitch_Ctl.scaleX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('L_IkFkSwitch_Ctl.scaleY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('L_IkFkSwitch_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)

        #visibility

        cmds.setAttr('L_IkFkSwitch_Ctl.visibility', lock=False, channelBox=False, keyable=False)

        # parent the group respectively

        cmds.parent('L_IkFkSwitch_Grp', 'L_Ik_Grp')

        # get the control to follow the hand by getting the top group parentConstrainted

        cmds.parentConstraint('L_Rig_wrist_jnt', 'L_IkFkSwitch_Grp', maintainOffset=True)


 

                  

 

# connect the Ik and the Fk to the bind

def R_connectFk_armSetup():

    # this is done to many times, and should be boiled down when introducing class

    # find the worldposition ws translate position of shoulder, elbow and wrist

    posTransShoulder = cmds.xform('R_Fk_shoulder_jnt', q=True, t=True, ws=True)

    posTransElbow = cmds.xform('R_Fk_elbow_jnt', q=True, t=True, ws=True)

    posTransWrist = cmds.xform('R_Fk_wrist_jnt', q=True, t=True, ws=True)

    # find the worldposition ws orient position of shoulder, elbow and wrist

    posOrientShoulder = cmds.xform('R_Fk_shoulder_jnt', q=True, t=True, ws=True)

    posOrientElbow = cmds.xform('R_Fk_elbow_jnt', q=True, t=True, ws=True)

    posOrientWrist = cmds.xform('R_Fk_wrist_jnt', q=True, t=True, ws=True)

    # create or find 3 pairblend node to switch between ik and fk

    # shoulder connection

    shldrPairNode = cmds.ls('R_shoulder_Pb')

    # if there already is a pairBlend node connect them together

    if shldrPairNode:

        cmds.connectAttr('R_Fk_shoulder_jnt.rotate', 'R_shoulder_Pb.inRotate2', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='R_shoulder_Pb')

        cmds.connectAttr('R_Fk_shoulder_jnt.rotate', 'R_shoulder_Pb.inRotate2', force=True)

       

    # elbow connection   

    elbowPairNode = cmds.ls('R_elbow_Pb')

    # if there already is a pairBlend node connect them together

    if elbowPairNode:

        cmds.connectAttr('R_Fk_elbow_jnt.rotate', 'R_elbow_Pb.inRotate2', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='R_elbow_Pb')

        cmds.connectAttr('R_Fk_elbow_jnt.rotate', 'R_elbow_Pb.inRotate2', force=True)

   

    # wrist connection   

    wristPairNode = cmds.ls('R_wrist_Pb')

    # if there already is a pairBlend node connect them together

    if wristPairNode:

        cmds.connectAttr('R_Fk_wrist_jnt.rotate', 'R_wrist_Pb.inRotate2', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='R_wrist_Pb')

        cmds.connectAttr('R_Fk_wrist_jnt.rotate', 'R_wrist_Pb.inRotate2', force=True)

       

    # connect the pairBlend node to the Rig joints

    # shoulder connection

    shldrConnect = cmds.listConnections('R_Rig_shoulder_jnt.rotate')

    if shldrConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('R_shoulder_Pb.outRotate', 'R_Rig_shoulder_jnt.rotate', f=True)

       

    # elbow connection      

        elbowConnect = cmds.listConnections('R_Rig_elbow_jnt.rotate')

    if elbowConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('R_elbow_Pb.outRotate', 'R_Rig_elbow_jnt.rotate', f=True)

 

    # wrist connection

    wristConnect = cmds.listConnections('R_Rig_wrist_jnt.rotate')

    if wristConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('R_wrist_Pb.outRotate', 'R_Rig_wrist_jnt.rotate', f=True)

       

    # Find or create a control for switching between the Ik and Fk

   

    createCtl = cmds.ls('R_IkFkSwitch_Ctl')

   

    if createCtl:

        print "control is there"

        return

       

    else:

        cmds.circle(n='R_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75)

        # create a group for the switch control

        cmds.group(em=True, n='R_IkFkSwitch_Grp')

        # parent the switch controller to the group

        cmds.parent('R_IkFkSwitch_Ctl', 'R_IkFkSwitch_Grp')

        # place the group above the hand

        cmds.xform('R_IkFkSwitch_Grp', t=posTransWrist, ws=True)

        cmds.xform('R_IkFkSwitch_Grp', t=posOrientWrist, ws=True)

        # turn the control to be horizontal and move it up

        cmds.xform('R_IkFkSwitch_Ctl', r=True, ro=(-90, 0, 0))

        cmds.xform('R_IkFkSwitch_Ctl', r=True, t=(0, 2, 0))

        # freeze the controlle

        cmds.makeIdentity('R_IkFkSwitch_Ctl', a=True)

        # remove history

        cmds.delete('R_IkFkSwitch_Ctl', ch=True)   

        # create attributes on the controller for ik fk switch, and the visibility

        cmds.addAttr('R_IkFkSwitch_Ctl', ln="ikFkSwitch", at='enum', en='Ik:Fk:', k=True)

        cmds.addAttr('R_IkFkSwitch_Ctl', ln="ikFkVisibility", at='enum', en='auto:both:', k=True)

        # connect the pairBlend to the ikFkSwitch

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkSwitch', 'R_shoulder_Pb.weight')

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkSwitch', 'R_elbow_Pb.weight')

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkSwitch', 'R_wrist_Pb.weight')

        # hide controls based on the selection ikFkVisibility attribute

        # create condition node and two reverse nodes for the setup

        cmds.shadingNode('reverse', n="R_ikFkVisibility01_Rev", au=True)

        cmds.shadingNode('reverse', n="R_ikFkVisibility02_Rev", au=True)

        cmds.shadingNode('condition', n="R_ikFkVisibility_Cnd", au=True)

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

        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'L_arm_poleVec_Grp.visibility')

        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_Ik_shoulder_jnt.visibility')

        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_Grp.visibility')

        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_jnt.visibility')

        # lock and hide the translate, rotate, scale and hide visibility

        #translate

        cmds.setAttr('R_IkFkSwitch_Ctl.translateX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.translateY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.translateZ', lock=True, channelBox=False, keyable=False)

        #rotate

        cmds.setAttr('R_IkFkSwitch_Ctl.rotateX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.rotateY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.rotateZ', lock=True, channelBox=False, keyable=False)

        #scale

        cmds.setAttr('R_IkFkSwitch_Ctl.scaleX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.scaleY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)

        #visibility

        cmds.setAttr('R_IkFkSwitch_Ctl.visibility', lock=False, channelBox=False, keyable=False)

        # parent the group respectively

        cmds.parent('R_IkFkSwitch_Grp', 'L_Ik_Grp')

        # get the control to follow the hand by getting the top group parentConstrainted

        cmds.parentConstraint('R_Rig_wrist_jnt', 'R_IkFkSwitch_Grp', maintainOffset=True)

 

   

     

def R_connectIk_armSetup():

    # this is done to many times, and should be boiled down when introducing class

    # find the worldposition ws translate position of shoulder, elbow and wrist

    posTransShoulder = cmds.xform('R_Ik_shoulder_jnt', q=True, t=True, ws=True)

    posTransElbow = cmds.xform('R_Ik_elbow_jnt', q=True, t=True, ws=True)

    posTransWrist = cmds.xform('R_Ik_wrist_jnt', q=True, t=True, ws=True)

    # find the worldposition ws orient position of shoulder, elbow and wrist

    posOrientShoulder = cmds.xform('R_Fk_shoulder_jnt', q=True, t=True, ws=True)

    posOrientElbow = cmds.xform('R_Ik_elbow_jnt', q=True, t=True, ws=True)

    posOrientWrist = cmds.xform('R_Ik_wrist_jnt', q=True, t=True, ws=True)

    # create or find 3 pairblend node to connect the fk joints to

   

    # shoulder connection

    shldrPairNode = cmds.ls('R_shoulder_Pb')

    # if there already is a pairBlend node connect them together

    if shldrPairNode:

        cmds.connectAttr('R_Ik_shoulder_jnt.rotate', 'R_shoulder_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='R_shoulder_Pb')

        cmds.connectAttr('R_Ik_shoulder_jnt.rotate', 'R_shoulder_Pb.inRotate1', force=True)

       

    # elbow connection   

    elbowPairNode = cmds.ls('R_elbow_Pb')

    # if there already is a pairBlend node connect them together

    if elbowPairNode:

        cmds.connectAttr('R_Ik_elbow_jnt.rotate', 'R_elbow_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='R_elbow_Pb')

        cmds.connectAttr('R_Ik_elbow_jnt.rotate', 'R_elbow_Pb.inRotate1', force=True)

   

    # wrist connection   

    wristPairNode = cmds.ls('R_wrist_Pb')

    # if there already is a pairBlend node connect them together

    if wristPairNode:

        cmds.connectAttr('R_Ik_wrist_jnt.rotate', 'R_wrist_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='R_wrist_Pb')

        cmds.connectAttr('R_Ik_wrist_jnt.rotate', 'R_wrist_Pb.inRotate1', force=True)

       

    # connect the pairBlend node to the Rig joints

    # shoulder connection

    shldrConnect = cmds.listConnections('R_Rig_shoulder_jnt.rotate')

    if shldrConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('R_shoulder_Pb.outRotate', 'R_Rig_shoulder_jnt.rotate', f=True)

       

    # elbow connection      

        elbowConnect = cmds.listConnections('R_Rig_elbow_jnt.rotate')

    if elbowConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('R_elbow_Pb.outRotate', 'R_Rig_elbow_jnt.rotate', f=True)

 

    # wrist connection

    wristConnect = cmds.listConnections('R_Rig_wrist_jnt.rotate')

    if wristConnect:

        print "this has a connection"

        return       

    else:

        cmds.connectAttr('R_wrist_Pb.outRotate', 'R_Rig_wrist_jnt.rotate', f=True)

       

    # Find or create a control for switching between the Ik and Fk

   

    createCtl = cmds.ls('R_IkFkSwitch_Ctl')

   

    if createCtl:

        print "control is there"

        return

       

    else:

        cmds.circle(n='R_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75)

        # create a group for the switch control

        cmds.group(em=True, n='R_IkFkSwitch_Grp')

        # parent the switch controller to the group

        cmds.parent('R_IkFkSwitch_Ctl', 'R_IkFkSwitch_Grp')

        # place the group above the hand

        cmds.xform('R_IkFkSwitch_Grp', t=posTransWrist, ws=True)

        cmds.xform('R_IkFkSwitch_Grp', t=posOrientWrist, ws=True)

        # turn the control to be horizontal and move it up

        cmds.xform('R_IkFkSwitch_Ctl', r=True, ro=(-90, 0, 0))

        cmds.xform('R_IkFkSwitch_Ctl', r=True, t=(0, 2, 0))

        # freeze the controlle

        cmds.makeIdentity('R_IkFkSwitch_Ctl', a=True)

        # remove history

        cmds.delete('R_IkFkSwitch_Ctl', ch=True)   

        # create attributes on the controller for ik fk switch, and the visibility

        cmds.addAttr('R_IkFkSwitch_Ctl', ln="ikFkSwitch", at='enum', en='Ik:Fk:', k=True)

        cmds.addAttr('R_IkFkSwitch_Ctl', ln="ikFkVisibility", at='enum', en='auto:both:', k=True)

        # connect the pairBlend to the ikFkSwitch

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkSwitch', 'R_shoulder_Pb.weight')

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkSwitch', 'R_elbow_Pb.weight')

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkSwitch', 'R_wrist_Pb.weight')

        # hide controls based on the selection ikFkVisibility attribute

        # create condition node and two reverse nodes for the setup

        cmds.shadingNode('reverse', n="R_ikFkVisibility01_Rev", au=True)

        cmds.shadingNode('reverse', n="R_ikFkVisibility02_Rev", au=True)

        cmds.shadingNode('condition', n="R_ikFkVisibility_Cnd", au=True)

        # set attributes on the condition node

        cmds.setAttr('R_ikFkVisibility_Cnd.operation', 0)

        cmds.setAttr('R_ikFkVisibility_Cnd.colorIfTrueR', 1)

        cmds.setAttr('R_ikFkVisibility_Cnd.colorIfTrueG', 1)

        # connect the ikFkSwitch to the nodes

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkSwitch', "R_ikFkVisibility01_Rev.input.inputX")

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkSwitch', "R_ikFkVisibility_Cnd.colorIfFalseR")

        cmds.connectAttr('R_IkFkSwitch_Ctl.ikFkVisibility', "R_ikFkVisibility02_Rev.input.inputX")

        # connect the reverse nodes to the condition

        cmds.connectAttr("R_ikFkVisibility01_Rev.output.outputX", "R_ikFkVisibility_Cnd.colorIfFalseG")

        cmds.connectAttr("R_ikFkVisibility02_Rev.output.outputX", "R_ikFkVisibility_Cnd.firstTerm")

        # connect the condition node to ik and fk control top groups, outColorG = Ik outColorR = Fk

        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_Ik_arm_Grp.visibility')

        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_poleVec_Grp.visibility')

        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_Ik_shoulder_jnt.visibility')

        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorR', 'R_Fk_shoulder_Grp.visibility')

        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorR', 'R_Fk_shoulder_jnt.visibility')

        # lock and hide the translate, rotate, scale and hide visibility

        #translate

        cmds.setAttr('R_IkFkSwitch_Ctl.translateX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.translateY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.translateZ', lock=True, channelBox=False, keyable=False)

        #rotate

        cmds.setAttr('R_IkFkSwitch_Ctl.rotateX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.rotateY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.rotateZ', lock=True, channelBox=False, keyable=False)

        #scale

        cmds.setAttr('R_IkFkSwitch_Ctl.scaleX', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.scaleY', lock=True, channelBox=False, keyable=False)

        cmds.setAttr('R_IkFkSwitch_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)

        #visibility

        cmds.setAttr('R_IkFkSwitch_Ctl.visibility', lock=False, channelBox=False, keyable=False)

        # parent the group respectively

        cmds.parent('R_IkFkSwitch_Grp', 'L_Ik_Grp')

        # get the control to follow the hand by getting the top group parentConstrainted

        cmds.parentConstraint('R_Rig_wrist_jnt', 'R_IkFkSwitch_Grp', maintainOffset=True)