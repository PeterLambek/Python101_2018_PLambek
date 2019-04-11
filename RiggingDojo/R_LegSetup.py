import maya.cmds as cmds


def R_rig_leg():

    # select 5 joints, femur, knee, ankle, ball, toeEnd in that order
    r_leg_sel = cmds.ls(selection=True)

    # make sure the selection is 5 by using the len() command
    if len(r_leg_sel) == 5:

        # rename the selected joints
        femur = cmds.rename(r_leg_sel[0], 'R_Rig_femur_jnt')
        knee = cmds.rename(r_leg_sel[1], 'R_Rig_knee_jnt')
        ankle = cmds.rename(r_leg_sel[2], 'R_Rig_ankle_jnt')
        ball = cmds.rename(r_leg_sel[3], 'R_Rig_ball_jnt')
        toeEnd = cmds.rename(r_leg_sel[4], 'R_Rig_toeEnd')

        cmds.select(femur)

        cmds.joint(e=True, oj='xyz', sao='zdown', ch=True, zso=True)

    else:
        print "select 5 joints - femur, knee, ankle, ball, toeEnd"
        return



    # place them in the group hierarchy if there is one
    placeInGroup = cmds.ls('main_Grp')

    # if it is there parent them respectly
    if placeInGroup:
        cmds.parent('R_Rig_femur_jnt', 'skeleton_Grp')


    else:

        return



def L_rig_leg_mirror():

    #easy mirror tool
    #should make it more correct, so you would not mirror it but set the orientation correct in case you dont have the

    r_leg_sel = cmds.ls(selection=True)

    cmds.mirrorJoint('R_Rig_femur_jnt', mirrorYZ=True, mirrorBehavior=True, searchReplace=("R_", "L_"))
    
def R_fk_leg():   

    # Duplicate the arm and add FK in the name

    fk_leg = cmds.duplicate('R_Rig_femur_jnt', renameChildren=True)   

    cmds.listRelatives(fk_leg, allDescendents=True)   

    fkFemur = cmds.rename(fk_leg[0], 'R_Fk_femur_jnt')
    fkKnee = cmds.rename(fk_leg[1], 'R_Fk_knee_jnt')
    fkAnkle = cmds.rename(fk_leg[2], 'R_Fk_ankle_jnt')
    fkBall = cmds.rename(fk_leg[3], 'R_Fk_ball_jnt')
    fkToeEnd = cmds.rename(fk_leg[4], 'R_Fk_toeEnd_jnt')   

    # create Fk Rig 

    # find the worldposition ws translate position of knee, ankle and ball
    posTransfemur = cmds.xform('R_Fk_femur_jnt', q=True, t=True, ws=True)
    posTransknee = cmds.xform('R_Fk_knee_jnt', q=True, t=True, ws=True)
    posTransankle = cmds.xform('R_Fk_ankle_jnt', q=True, t=True, ws=True)
    posTransball = cmds.xform('R_Fk_ball_jnt', q=True, t=True, ws=True)

    # find the worldposition ws orient position of knee, ankle and ball
    posOrientfemur = cmds.xform('R_Fk_femur_jnt', q=True, ro=True, ws=True)
    posOrientknee = cmds.xform('R_Fk_knee_jnt', q=True, ro=True, ws=True)
    posOrientankle = cmds.xform('R_Fk_ankle_jnt', q=True, ro=True, ws=True)
    posOrientball = cmds.xform('R_Fk_ball_jnt', q=True, ro=True, ws=True)

    # create a group for each limb (3)
    cmds.group(em=True, n='R_Fk_femur_Grp')
    cmds.group(em=True, n='R_Fk_knee_Grp')
    cmds.group(em=True, n='R_Fk_ankle_Grp')
    cmds.group(em=True, n='R_Fk_ball_Grp')

    # create a controller for each limb (3)
    cmds.circle(n='R_Fk_femur_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.0)
    cmds.circle(n='R_Fk_knee_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.0)
    cmds.circle(n='R_Fk_ankle_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.0)
    cmds.circle(n='R_Fk_ball_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.0)
    
    # rotate the controls correctly
    cmds.xform('R_Fk_femur_Ctl', ro=(90, 0, 0), ws=True)
    cmds.xform('R_Fk_knee_Ctl', ro=(90, 0, 0), ws=True)
    cmds.xform('R_Fk_ankle_Ctl', ro=(90, 0, 0), ws=True)
    cmds.xform('R_Fk_ball_Ctl', ro=(0, 0, 90), ws=True)
    
   # orient the group after the respected name
    cmds.xform('R_Fk_femur_Grp', ro=posOrientfemur, ws=True)
    cmds.xform('R_Fk_knee_Grp', ro=posOrientknee, ws=True)
    cmds.xform('R_Fk_ankle_Grp', ro=posOrientankle, ws=True)
    cmds.xform('R_Fk_ball_Grp', ro=posOrientball, ws=True)

    # parent the controller to the groups
    cmds.parent('R_Fk_femur_Ctl', 'R_Fk_femur_Grp')
    cmds.parent('R_Fk_knee_Ctl', 'R_Fk_knee_Grp')
    cmds.parent('R_Fk_ankle_Ctl', 'R_Fk_ankle_Grp')
    cmds.parent('R_Fk_ball_Ctl', 'R_Fk_ball_Grp')

    # freeze history and clear history of control
    cmds.makeIdentity('R_Fk_femur_Ctl', a=True)
    cmds.makeIdentity('R_Fk_knee_Ctl', a=True)
    cmds.makeIdentity('R_Fk_ankle_Ctl', a=True)
    cmds.makeIdentity('R_Fk_ball_Ctl', a=True)
    
    cmds.delete('R_Fk_femur_Ctl', ch=True)
    cmds.delete('R_Fk_knee_Ctl', ch=True)
    cmds.delete('R_Fk_ankle_Ctl', ch=True)
    cmds.delete('R_Fk_ball_Ctl', ch=True)

    # move the groups to the respected names location
    cmds.xform('R_Fk_femur_jnt', t=posTransfemur, ws=True)
    cmds.xform('R_Fk_knee_jnt', t=posTransknee, ws=True)
    cmds.xform('R_Fk_ankle_jnt', t=posTransankle, ws=True)
    cmds.xform('R_Fk_ball_jnt', t=posTransball, ws=True)

    # freeze the orientation of the controllers
    cmds.makeIdentity('R_Fk_femur_Ctl', apply=True, r=True, t=True)
    cmds.makeIdentity('R_Fk_knee_Ctl', apply=True, r=True, t=True)
    cmds.makeIdentity('R_Fk_ankle_Ctl', apply=True, r=True, t=True)
    cmds.makeIdentity('R_Fk_ball_Ctl', apply=True, r=True, t=True)

   # delete history of the controllers
    cmds.delete('R_Fk_femur_Ctl', ch=True)
    cmds.delete('R_Fk_knee_Ctl', ch=True)
    cmds.delete('R_Fk_ankle_Ctl', ch=True)
    cmds.delete('R_Fk_ball_Ctl', ch=True)

    # position the groups to the limbs
    cmds.xform('R_Fk_femur_Grp', t=posTransfemur, ws=True)
    cmds.xform('R_Fk_knee_Grp', t=posTransknee, ws=True)
    cmds.xform('R_Fk_ankle_Grp', t=posTransankle, ws=True)
    cmds.xform('R_Fk_ball_Grp', t=posTransball, ws=True)

    # set the controllers to control the joint limbs
    cmds.parentConstraint('R_Fk_femur_Ctl', 'R_Fk_femur_jnt', mo=True)
    cmds.parentConstraint('R_Fk_knee_Ctl', 'R_Fk_knee_jnt', mo=True)
    cmds.parentConstraint('R_Fk_ankle_Ctl', 'R_Fk_ankle_jnt', mo=True)
    cmds.parentConstraint('R_Fk_ball_Ctl', 'R_Fk_ball_jnt', mo=True)

    # parent the controllers and groups together

    cmds.parent('R_Fk_ball_Grp', 'R_Fk_ankle_Ctl')
    cmds.parent('R_Fk_ankle_Grp', 'R_Fk_knee_Ctl')
    cmds.parent('R_Fk_knee_Grp', 'R_Fk_femur_Ctl')

    # lock and hide translate, scale and visibility
    
    # femur

    cmds.setAttr('R_Fk_femur_Ctl.translateX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_femur_Ctl.translateY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_femur_Ctl.translateZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_femur_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_femur_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_femur_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_femur_Ctl.visibility', lock=True, channelBox=False, keyable=False)
    # knee

    cmds.setAttr('R_Fk_knee_Ctl.translateX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_knee_Ctl.translateY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_knee_Ctl.translateZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_knee_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_knee_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_knee_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_knee_Ctl.visibility', lock=True, channelBox=False, keyable=False)

    # ankle

    cmds.setAttr('R_Fk_ankle_Ctl.translateX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ankle_Ctl.translateY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ankle_Ctl.translateZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ankle_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ankle_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ankle_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ankle_Ctl.visibility', lock=True, channelBox=False, keyable=False)

    # ball

    cmds.setAttr('R_Fk_ball_Ctl.translateX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ball_Ctl.translateY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ball_Ctl.translateZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ball_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ball_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ball_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)
    cmds.setAttr('R_Fk_ball_Ctl.visibility', lock=True, channelBox=False, keyable=False)
 

    # place them in the group hierarchy if there is one

    placeInGroup = cmds.ls('main_Grp')

    # if it is there parent them respectly

    if placeInGroup:
        cmds.parent('R_Fk_femur_Grp', 'R_Fk_Grp')       

    else:
        return
        
def R_ik_leg():
    # create the Ik arm by duplicating
    ik_leg = cmds.duplicate('R_Rig_femur_jnt', rc=True)
    
    cmds.listRelatives(ik_leg, ad=True)
    
    ik_femur = cmds.rename(ik_leg[0], 'R_Ik_femur_jnt')
    ik_knee = cmds.rename(ik_leg[1], 'R_Ik_knee_jnt')
    ik_ankle = cmds.rename(ik_leg[2], 'R_Ik_ankle_jnt')
    ik_ball = cmds.rename(ik_leg[3], 'R_Ik_ball_jnt')
    ik_toe = cmds.rename(ik_leg[4], 'R_Ik_toe_jnt')
    # create Ik Rig
    #create Rotate ikHandle between the femur and ankle
    ik_hdl_femur = cmds.ikHandle(n='R_femurAnkle_Ikh', sj=ik_femur, ee=ik_ankle, sol='ikRPsolver', p=2, w=1)
    #create Single ikHandle between the ankle and ball
    ik_hdl_ball = cmds.ikHandle(n='R_ankleBall_Ikh', sj=ik_ankle, ee=ik_ball, sol='ikSCsolver', p=2, w=1)
    #create Single ikHandle between the ball and toe
    ik_hdl_toe = cmds.ikHandle(n='R_ballToe_Ikh', sj=ik_ball, ee=ik_toe, sol='ikSCsolver', p=2, w=1)
    # find the worldspace ws translate position of the ankle
    pos_trans_ankle_ik = cmds.xform(ik_ankle, q=True, t=True, ws=True)
    pos_trans_ball_ik = cmds.xform(ik_ball, q=True, t=True, ws=True)
    pos_trans_toe_ik = cmds.xform(ik_toe, q=True, t=True, ws=True)
    # find the worldspace ws orientation position of the ankle
    pos_orient_ankle_ik = cmds.xform(ik_ankle, q=True, ro=True, ws=True)
    pos_orient_ball_ik = cmds.xform(ik_ball, q=True, ro=True, ws=True)
    pos_orient_toe_ik = cmds.xform(ik_toe, q=True, ro=True, ws=True)
    # create the empty group
    ik_grp = cmds.group(em=True, n='R_Ik_leg_Grp')
    # create the control
    ik_foot_ctl = cmds.circle(n='R_Ik_foot_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.0 )
    cmds.xform(ik_foot_ctl, ro=(90, 0, 0), ws=True)
    # create the offset control
    ik_footOffset_ctl = cmds.circle(n='R_Ik_footOffset_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.25 )
    cmds.xform(ik_footOffset_ctl, ro=(90, 0, 0), ws=True)
    # orient the group to the ankle
    cmds.xform(ik_grp, ro=(-90, -90, -90), ws=True)
    # parent offset control to control
    cmds.parent('R_Ik_footOffset_Ctl', 'R_Ik_foot_Ctl')
    # parent the control to the group
    cmds.parent('R_Ik_foot_Ctl', 'R_Ik_leg_Grp')
    # freeze ik ctl
    cmds.makeIdentity(ik_foot_ctl, r=True, a=True)
    # remove history
    cmds.delete(ik_foot_ctl, constructionHistory=True)
    # move the group to the wrist
    cmds.xform(ik_grp, t=pos_trans_ankle_ik, ws=True)
    #create groups for the ikhandles
    peel_heel_grp = cmds.group(em=True, n="R_peelheel_Grp")
    toe_tap_grp = cmds.group(em=True, n="R_toeTap_Grp")
    toe_tap_footRoll_grp = cmds.group(em=True, n="R_toeTap_footRoll_ball_Grp")
    stand_tip_grp = cmds.group(em=True, n="R_standTip_Grp")
    stand_tip_footRoll_grp = cmds.group(em=True, n="R_standTip_footRoll_Toe_Grp")
    heel_pivot_grp = cmds.group(em=True, n="R_heelPivot_Grp")
    heel_pivot_footRoll_grp = cmds.group(em=True, n="R_heel_pivot_footRoll_Grp")
    peel_heel_footRoll_grp = cmds.group(em=True, n="R_peel_heel_footRoll_Grp")
    twist_heel_grp = cmds.group(em=True, n="R_twistHeel_Grp")
    twist_ball_grp = cmds.group(em=True, n="R_twistBall_Grp")
    twist_toe_grp = cmds.group(em=True, n="R_twistToe_Grp")
    left_bank_grp = cmds.group(em=True, n="R_leftBank_Grp")
    right_bank_grp = cmds.group(em=True, n="R_rightBank_Grp")
    foot_attr_grp = cmds.group(em=True, n="R_footAttr_Grp")
    gimbal_grp = cmds.group(em=True, n="R_foot_gimbal_Grp")
    
    #place the groups
    
    cmds.xform(peel_heel_grp, t=pos_trans_ball_ik, ws=True)
    cmds.xform(toe_tap_grp, t=pos_trans_ball_ik, ws=True)
    cmds.xform(stand_tip_grp, t=pos_trans_toe_ik, ws=True)
    cmds.xform(heel_pivot_grp, t=pos_trans_ankle_ik, ws=True)
    cmds.xform(heel_pivot_footRoll_grp, t=pos_trans_ankle_ik, ws=True)
    cmds.xform(toe_tap_footRoll_grp, t=pos_trans_ball_ik, ws=True)
    cmds.xform(stand_tip_footRoll_grp, t=pos_trans_toe_ik, ws=True)
    cmds.xform(heel_pivot_footRoll_grp, t=pos_trans_ankle_ik, ws=True)
    cmds.xform(twist_heel_grp, t=pos_trans_ankle_ik, ws=True)
    cmds.xform(twist_ball_grp, t=pos_trans_ball_ik, ws=True)
    cmds.xform(twist_toe_grp, t=pos_trans_toe_ik, ws=True)
    cmds.xform(left_bank_grp, t=pos_trans_ball_ik, ws=True)
    cmds.xform(right_bank_grp, t=pos_trans_ball_ik, ws=True)
    cmds.xform(foot_attr_grp, t=pos_trans_ball_ik, ws=True)
    cmds.xform(gimbal_grp, t=pos_trans_ankle_ik, ws=True)
    
    # parent the groups together to make the correct movement
    cmds.parent("R_peelheel_Grp", "R_toeTap_footRoll_ball_Grp")
    cmds.parent("R_toeTap_footRoll_ball_Grp", "R_peel_heel_footRoll_Grp")
    cmds.parent("R_peel_heel_footRoll_Grp", "R_standTip_Grp")
    cmds.parent("R_toeTap_Grp", "R_standTip_Grp")
    cmds.parent("R_standTip_Grp", "R_standTip_footRoll_Toe_Grp")
    cmds.parent("R_standTip_footRoll_Toe_Grp", "R_heelPivot_Grp")
    cmds.parent("R_heelPivot_Grp", "R_heel_pivot_footRoll_Grp")
    cmds.parent("R_heel_pivot_footRoll_Grp", "R_twistHeel_Grp")
    cmds.parent("R_twistHeel_Grp", "R_twistBall_Grp")
    cmds.parent("R_twistBall_Grp", "R_twistToe_Grp")
    cmds.parent("R_twistToe_Grp", "R_leftBank_Grp")
    cmds.parent("R_leftBank_Grp", "R_rightBank_Grp")
    cmds.parent("R_rightBank_Grp", "R_footAttr_Grp")
    cmds.parent("R_footAttr_Grp", "R_foot_gimbal_Grp")
    
    # parent the ikhandles to the groups
    cmds.parent('R_femurAnkle_Ikh', peel_heel_grp)
    cmds.parent('R_ankleBall_Ikh', toe_tap_grp)
    cmds.parent('R_ballToe_Ikh', toe_tap_grp)
    # parent the Ikhandle GROUP to the controller
    cmds.parent("R_foot_gimbal_Grp", 'R_Ik_footOffset_Ctl')
    
    #create the attributes for the foot control
    
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "gimbalX", at= "double")
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "gimbalY", at= "double")
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "gimbalZ", at= "double")
    #
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, readable=False, ln= "seperator1", nn= "__", min= 0, max= 0, en= "__________", at="enum")
    #
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "PvControl", min=0, max=1, en="off:on", at= "enum")
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "legTwist", at= "float")
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "offsetVis", min=0, max=1, en="off:on", at= "enum")
    #
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, readable=False, ln= "seperator2", nn= "__", min= 0, max= 0, en= "__________", at="enum")   
    #
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "footFollow", min=0, max=3, en="Fk ctl:hip:cog:world", at= "enum")
    #
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, readable=False, ln= "seperator3", nn= "__", min= 0, max= 0, en= "__________", at="enum") 
    #
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "footRoll", at= "float")
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "toeBreak", at= "float")
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, ln= "toeStraight", at= "double")
    cmds.setAttr('R_Ik_foot_Ctl.toeBreak', 20)
    cmds.setAttr('R_Ik_foot_Ctl.toeStraight', 70)
    #
    cmds.addAttr('R_Ik_foot_Ctl', keyable=True, readable=False, ln= "seperator4", nn= "__", min= 0, max= 0, en= "__________", at="enum") 
    #
    cmds.addAttr('R_Ik_foot_Ctl',keyable=True, ln="heelUp", min=-10, max=10, at="float")
    cmds.addAttr('R_Ik_foot_Ctl',keyable=True, ln="peelHeel", at="double")
    cmds.addAttr('R_Ik_foot_Ctl',keyable=True, ln="standTip", min=0, max=10, at="float")
    cmds.addAttr('R_Ik_foot_Ctl',keyable=True, ln="toeTap", min=-10, max=10, at="float")
    cmds.addAttr('R_Ik_foot_Ctl',keyable=True, ln="twistHeel", min=-10, max=10, at="float")
    cmds.addAttr('R_Ik_foot_Ctl',keyable=True, ln="twistBall", min=-10, max=10, at="float")
    cmds.addAttr('R_Ik_foot_Ctl',keyable=True, ln="twistToes", min=-10, max=10, at="float")
    cmds.addAttr('R_Ik_foot_Ctl',keyable=True, ln="footBank", min=-10, max=10, at="float")
    #
    
    # getting controller to control the orient of the wrist
    cmds.orientConstraint('R_Ik_footOffset_Ctl', 'R_Ik_ankle_jnt', mo=True)
    
    #Create Pole vec
        
    # create a locator as a poleVector
    pv_loc = cmds.spaceLocator(n='R_poleVec_Loc')
    # create a group as the group for a poleVector
    pv_grp = cmds.group(em=True, n='R_poleVec_Grp')
    # parent locator to the group
    cmds.parent('R_poleVec_Loc', 'R_poleVec_Grp')
    # place the group between the shoulder and the wrist
    cmds.pointConstraint(ik_femur, ik_ankle, pv_grp)
    # aim the locator twoards the elbow
    cmds.aimConstraint(ik_knee, pv_grp, aim=(1,0,0), u=(0,1,0))
    # delete the constraints
    cmds.delete('R_poleVec_Grp_pointConstraint1')
    cmds.delete('R_poleVec_Grp_aimConstraint1')
    # place the locater out from the elbow using the X axis trans
    cmds.move(5, pv_loc, x=True, os=True, ws=False)
    #create controller for the polevector
    ik_knee_ctl = cmds.circle(n='R_Ik_knee_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5 )
    # rotate the controller
    #cmds.rotate(0, '90deg', 0, ik_knee_ctl)
    # move parent the controller to the locator locatieon
    cmds.pointConstraint(pv_loc, ik_knee_ctl)
    # delete pointConstraint from controller
    cmds.delete('R_Ik_knee_Ctl_pointConstraint1')
    # parent controller to grp
    cmds.parent('R_Ik_knee_Ctl', 'R_poleVec_Grp')
    # freeze orientation on controller
    cmds.makeIdentity(ik_knee_ctl, a=True)
    # delete history on ctl
    cmds.delete(ik_knee_ctl, ch=True)
    # parent poleVEc to controller
    cmds.parent('R_poleVec_Loc', 'R_Ik_knee_Ctl')
    # connect the polevector constraint to the ikhandle and the locator
    cmds.poleVectorConstraint(pv_loc, 'R_femurAnkle_Ikh')
    # hide locator
    cmds.hide(pv_loc)
    # hide scale from ik control
    cmds.setAttr('R_Ik_foot_Ctl.scaleX', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_foot_Ctl.scaleY', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_foot_Ctl.scaleZ', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_foot_Ctl.v', keyable=False, ch=False, lock=True)
    # hide scale from ik offset control
    cmds.setAttr('R_Ik_footOffset_Ctl.scaleX', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_footOffset_Ctl.scaleY', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_footOffset_Ctl.scaleZ', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_footOffset_Ctl.v', keyable=False, ch=False, lock=True)
    #hide rotate and scale from knee ik control
    cmds.setAttr('R_Ik_knee_Ctl.rotateX', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_knee_Ctl.rotateY', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_knee_Ctl.rotateZ', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_knee_Ctl.scaleX', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_knee_Ctl.scaleY', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_knee_Ctl.scaleZ', keyable=False, ch=False, lock=True)
    cmds.setAttr('R_Ik_knee_Ctl.v', keyable=False, ch=False, lock=True)
    #delete history on the ik control
    cmds.delete('R_Ik_foot_Ctl', ch=True)
    
    # place them in the group hierarchy if there is one
    placeInGroup = cmds.ls('main_Grp')

    # if it is there parent them respectly

    if placeInGroup:
        cmds.parent('R_Ik_leg_Grp', 'R_Ik_Grp')
        cmds.parent('R_poleVec_Grp', 'R_Ik_Grp')       

    else:
        return    
    


def R_connectFk_legSetup():

    # this is done to many times, and should be boiled down when introducing class
    # find the worldposition ws translate position of femur, knee and ankle

    posTransAnkle = cmds.xform('R_Fk_ankle_jnt', q=True, t=True, ws=True)

    # find the worldposition ws orient position of femur, knee and ankle

    posOrientAnkle = cmds.xform('R_Fk_ankle_jnt', q=True, t=True, ws=True)

    # create or find 3 pairblend node to switch between ik and fk
    # femur connection

    femurPairNode = cmds.ls('R_femur_Pb')

    # if there already is a pairBlend node connect them together

    if femurPairNode:
        cmds.connectAttr('R_Fk_femur_jnt.rotate', 'R_femur_Pb.inRotate2', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='R_femur_Pb')
        cmds.connectAttr('R_Fk_femur_jnt.rotate', 'R_femur_Pb.inRotate2', force=True)

       

    # knee connection   
    kneePairNode = cmds.ls('R_knee_Pb')

    # if there already is a pairBlend node connect them together

    if kneePairNode:
        cmds.connectAttr('R_Fk_knee_jnt.rotate', 'R_knee_Pb.inRotate2', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:

        cmds.shadingNode('pairBlend', asUtility=True, name='R_knee_Pb')
        cmds.connectAttr('R_Fk_knee_jnt.rotate', 'R_knee_Pb.inRotate2', force=True)
   

    # ankle connection   
    anklePairNode = cmds.ls('R_ankle_Pb')
    # if there already is a pairBlend node connect them together
    if anklePairNode:
        cmds.connectAttr('R_Fk_ankle_jnt.rotate', 'R_ankle_Pb.inRotate2', force=True)
    # if there are no pairBlend node then we create the node and connects them together
    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='R_ankle_Pb')
        cmds.connectAttr('R_Fk_ankle_jnt.rotate', 'R_ankle_Pb.inRotate2', force=True)

    # ball connection
    ballPairNode = cmds.ls('R_ball_Pb')
    # if there already is a pairBlend node connect them together
    if ballPairNode:
        cmds.connectAttr('R_Fk_ball_jnt.rotate', 'R_ball_Pb.inRotate2', force=True)
    # if there are no pairBlend node then we create the node and connects them together
    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='R_ball_Pb')
        cmds.connectAttr('R_Fk_ball_jnt.rotate', 'R_ball_Pb.inRotate2', force=True)

       

    # connect the pairBlend node to the Rig joints
    # femur connection
    shldrConnect = cmds.listConnections('R_Rig_femur_jnt.rotate')
    if shldrConnect:
        print "this has a connection"
        return       
    else:
        cmds.connectAttr('R_femur_Pb.outRotate', 'R_Rig_femur_jnt.rotate', f=True)

       

    # knee connection      

        kneeConnect = cmds.listConnections('R_Rig_knee_jnt.rotate')

    if kneeConnect:
        print "this has a connection"
        return      

    else:

        cmds.connectAttr('R_knee_Pb.outRotate', 'R_Rig_knee_jnt.rotate', f=True)

 

    # ankle connection

    ankleConnect = cmds.listConnections('R_Rig_ankle_jnt.rotate')
    if ankleConnect:
        print "this has a connection"
        return       

    else:

        cmds.connectAttr('R_ankle_Pb.outRotate', 'R_Rig_ankle_jnt.rotate', f=True)

    # ball connection

    ballConnect = cmds.listConnections('R_Rig_ball_jnt.rotate')
    if ballConnect:
        print "this has a connection"
        return

    else:

        cmds.connectAttr('R_ball_Pb.outRotate', 'R_Rig_ball_jnt.rotate', f=True)

       

    # Find or create a control for switching between the Ik and Fk

   

    createCtl = cmds.ls('R_leg_IkFkSwitch_Ctl')
   

    if createCtl:
        print "control is there"
        return
       

    else:
        cmds.circle(n='R_leg_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75)

        # create a group for the switch control
        cmds.group(em=True, n='R_leg_IkFkSwitch_Grp')

        # parent the switch controller to the group
        cmds.parent('R_leg_IkFkSwitch_Ctl', 'R_leg_IkFkSwitch_Grp')

        # place the group above the hand
        cmds.xform('R_leg_IkFkSwitch_Grp', t=posTransAnkle, ws=True)
        cmds.xform('R_leg_IkFkSwitch_Grp', t=posOrientAnkle, ws=True)

        # turn the control to be horizontal and move it up
        cmds.xform('R_leg_IkFkSwitch_Ctl', r=True, ro=(-90, 0, 0))
        cmds.xform('R_leg_IkFkSwitch_Ctl', r=True, t=(0, 2, 0))

        # freeze the controlle
        cmds.makeIdentity('R_leg_IkFkSwitch_Ctl', a=True)

        # remove history
        cmds.delete('R_leg_IkFkSwitch_Ctl', ch=True)   

        # create attributes on the controller for ik fk switch, and the visibility
        cmds.addAttr('R_leg_IkFkSwitch_CtlShape', ln="ikFkSwitch", at='enum', en='Ik:Fk:', k=True)
        cmds.addAttr('R_leg_IkFkSwitch_CtlShape', ln="ikFkVisibility", at='enum', en='auto:both:', k=True)

        # connect the pairBlend to the ikFkSwitch

        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', 'R_femur_Pb.weight')
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', 'R_knee_Pb.weight')
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', 'R_ankle_Pb.weight')

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
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', "R_ikFkVisibility01_Rev.input.inputX")

        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', "R_ikFkVisibility_Cnd.colorIfFalseR")
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkVisibility', "R_ikFkVisibility02_Rev.input.inputX")

        # connect the reverse nodes to the condition

        cmds.connectAttr("R_ikFkVisibility01_Rev.output.outputX", "R_ikFkVisibility_Cnd.colorIfFalseG")
        cmds.connectAttr("R_ikFkVisibility02_Rev.output.outputX", "R_ikFkVisibility_Cnd.firstTerm")

        # connect the condition node to ik and fk control top groups, outColorG = Ik outColorR = Fk

        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_Ik_leg_Grp.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_poleVec_Grp.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_Ik_femur_jnt.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorR', 'R_Fk_femur_Grp.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorR', 'R_Fk_femur_jnt.visibility')

        # lock and hide the translate, rotate, scale and hide visibility

        #translate

        cmds.setAttr('R_leg_IkFkSwitch_Ctl.translateX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.translateY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.translateZ', lock=True, channelBox=False, keyable=False)

        #rotate

        cmds.setAttr('R_leg_IkFkSwitch_Ctl.rotateX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.rotateY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.rotateZ', lock=True, channelBox=False, keyable=False)

        #scale

        cmds.setAttr('R_leg_IkFkSwitch_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)

        #visibility
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.visibility', lock=False, channelBox=False, keyable=False)

        # parent the group respectively
        cmds.parent('R_leg_IkFkSwitch_Grp', 'R_Ik_Grp')

        # get the control to follow the hand by getting the top group parentConstrainted
        cmds.parentConstraint('R_Rig_ankle_jnt', 'R_leg_IkFkSwitch_Grp', maintainOffset=True)

 

    

def R_connectIk_legSetup():

    # this is done to many times, and should be boiled down when introducing class

    # find the worldposition ws translate position of femur, knee and ankle

    posTransfemur = cmds.xform('R_Ik_femur_jnt', q=True, t=True, ws=True)
    posTransknee = cmds.xform('R_Ik_knee_jnt', q=True, t=True, ws=True)
    posTransankle = cmds.xform('R_Ik_ankle_jnt', q=True, t=True, ws=True)

    # find the worldposition ws orient position of femur, knee and ankle

    posOrientfemur = cmds.xform('R_Fk_femur_jnt', q=True, t=True, ws=True)
    posOrientknee = cmds.xform('R_Ik_knee_jnt', q=True, t=True, ws=True)
    posOrientankle = cmds.xform('R_Ik_ankle_jnt', q=True, t=True, ws=True)

    # create or find 3 pairblend node to connect the fk joints to

   

    # femur connection
    femurPairNode = cmds.ls('R_femur_Pb')

    # if there already is a pairBlend node connect them together
    if femurPairNode:
        cmds.connectAttr('R_Ik_femur_jnt.rotate', 'R_femur_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together
    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='R_femur_Pb')
        cmds.connectAttr('R_Ik_femur_jnt.rotate', 'R_femur_Pb.inRotate1', force=True)

       

    # knee connection  
    kneePairNode = cmds.ls('R_knee_Pb')

    # if there already is a pairBlend node connect them together
    if kneePairNode:
        cmds.connectAttr('R_Ik_knee_jnt.rotate', 'R_knee_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together

    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='R_knee_Pb')
        cmds.connectAttr('R_Ik_knee_jnt.rotate', 'R_knee_Pb.inRotate1', force=True)   

    # ankle connection   
    anklePairNode = cmds.ls('R_ankle_Pb')

    # if there already is a pairBlend node connect them together
    if anklePairNode:
        cmds.connectAttr('R_Ik_ankle_jnt.rotate', 'R_ankle_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together
    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='R_ankle_Pb')
        cmds.connectAttr('R_Ik_ankle_jnt.rotate', 'R_ankle_Pb.inRotate1', force=True)


    # ball connection
    ballPairNode = cmds.ls('R_ball_Pb')

    # if there already is a pairBlend node connect them together
    if ballPairNode:
        cmds.connectAttr('R_Ik_ball_jnt.rotate', 'R_ball_Pb.inRotate1', force=True)

    # if there are no pairBlend node then we create the node and connects them together
    else:
        cmds.shadingNode('pairBlend', asUtility=True, name='R_ball_Pb')
        cmds.connectAttr('R_Ik_ball_jnt.rotate', 'R_ball_Pb.inRotate1', force=True)

       

    # connect the pairBlend node to the Rig joints

    # femur connection

    shldrConnect = cmds.listConnections('R_Rig_femur_jnt.rotate')
    if shldrConnect:
        print "this has a connection"

        return       

    else:

        cmds.connectAttr('R_femur_Pb.outRotate', 'R_Rig_femur_jnt.rotate', f=True)
       

    # knee connection      

        kneeConnect = cmds.listConnections('R_Rig_knee_jnt.rotate')
    if kneeConnect:

        print "this has a connection"
        return       
    else:
        cmds.connectAttr('R_knee_Pb.outRotate', 'R_Rig_knee_jnt.rotate', f=True)

 

    # ankle connection

    ankleConnect = cmds.listConnections('R_Rig_ankle_jnt.rotate')
    if ankleConnect:
        print "this has a connection"
        return      

    else:
        cmds.connectAttr('R_ankle_Pb.outRotate', 'R_Rig_ankle_jnt.rotate', f=True)


    # ball connection

    ballConnect = cmds.listConnections('R_Rig_ball_jnt.rotate')
    if ballConnect:
        print "this has a connection"

        return

    else:

        cmds.connectAttr('R_ball_Pb.outRotate', 'R_Rig_ball_jnt.rotate', f=True)

    # Find or create a control for switching between the Ik and Fk

   

    createCtl = cmds.ls('R_leg_IkFkSwitch_Ctl')
   

    if createCtl:

        print "control is there"

        return       

    else:
        cmds.circle(n='R_leg_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75)

        # create a group for the switch control
        cmds.group(em=True, n='R_leg_IkFkSwitch_Grp')

        # parent the switch controller to the group
        cmds.parent('R_leg_IkFkSwitch_Ctl', 'R_leg_IkFkSwitch_Grp')

        # place the group above the hand
        cmds.xform('R_leg_IkFkSwitch_Grp', t=posTransankle, ws=True)
        cmds.xform('R_leg_IkFkSwitch_Grp', t=posOrientankle, ws=True)

        # turn the control to be horizontal and move it up
        cmds.xform('R_leg_IkFkSwitch_Ctl', r=True, ro=(-90, 0, 0))
        cmds.xform('R_leg_IkFkSwitch_Ctl', r=True, t=(0, 2, 0))

        # freeze the controlle
        cmds.makeIdentity('R_leg_IkFkSwitch_Ctl', a=True)

        # remove history
        cmds.delete('R_leg_IkFkSwitch_Ctl', ch=True)   

        # create attributes on the controller for ik fk switch, and the visibility
        cmds.addAttr('R_leg_IkFkSwitch_CtlShape', ln="ikFkSwitch", at='enum', en='Ik:Fk:', k=True)
        cmds.addAttr('R_leg_IkFkSwitch_CtlShape', ln="ikFkVisibility", at='enum', en='auto:both:', k=True)

        # connect the pairBlend to the ikFkSwitch
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', 'R_femur_Pb.weight')
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', 'R_knee_Pb.weight')
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', 'R_ankle_Pb.weight')

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
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', "R_ikFkVisibility01_Rev.input.inputX")
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkSwitch', "R_ikFkVisibility_Cnd.colorIfFalseR")
        cmds.connectAttr('R_leg_IkFkSwitch_CtlShape.ikFkVisibility', "R_ikFkVisibility02_Rev.input.inputX")

        # connect the reverse nodes to the condition
        cmds.connectAttr("R_ikFkVisibility01_Rev.output.outputX", "R_ikFkVisibility_Cnd.colorIfFalseG")
        cmds.connectAttr("R_ikFkVisibility02_Rev.output.outputX", "R_ikFkVisibility_Cnd.firstTerm")

        # connect the condition node to ik and fk control top groups, outColorG = Ik outColorR = Fk
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_Ik_leg_Grp.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_poleVec_Grp.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_Ik_femur_jnt.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorR', 'R_Fk_femur_Grp.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorR', 'R_Fk_femur_jnt.visibility')

       

        # lock and hide the translate, rotate, scale and hide visibility
        #translate

        cmds.setAttr('R_leg_IkFkSwitch_Ctl.translateX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.translateY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.translateZ', lock=True, channelBox=False, keyable=False)

        #rotate

        cmds.setAttr('R_leg_IkFkSwitch_Ctl.rotateX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.rotateY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.rotateZ', lock=True, channelBox=False, keyable=False)

        #scale

        cmds.setAttr('R_leg_IkFkSwitch_Ctl.scaleX', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.scaleY', lock=True, channelBox=False, keyable=False)
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.scaleZ', lock=True, channelBox=False, keyable=False)

        #visibility
        cmds.setAttr('R_leg_IkFkSwitch_Ctl.visibility', lock=False, channelBox=False, keyable=False)

        # parent the group respectively
        cmds.parent('R_leg_IkFkSwitch_Grp', 'R_Ik_Grp')

        # get the control to follow the hand by getting the top group parentConstrainted
        cmds.parentConstraint('R_Rig_ankle_jnt', 'R_leg_IkFkSwitch_Grp', maintainOffset=True)
