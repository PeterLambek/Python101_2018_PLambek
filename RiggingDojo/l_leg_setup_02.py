import maya.cmds as cmds
import os
import json
from PySide2 import QtWidgets, QtCore, QtGui

# create first the joints - shoulder, knee, wrist, wristEnd (no need for naming)
# selection to a variable

L_Leg_Setup = l_leg_setup()
L_Leg_Setup.L_ik_leg()


class utillity():

    def create_space_groups(self, name=None):

        """
        creates space groups if not already in the scene
        :param name: group name
        :type name: str
        """

        if cmds.objExists(name):
            return
        else:
            cmds.group(empty=True, name=name)


class l_leg_setup():

    def __init__(self):
        self.util = utillity()

    def L_bind_leg(self):
        l_leg_sel = cmds.ls(selection=True)

        femur = cmds.rename(l_leg_sel[0], 'L_femur_jnt')
        knee = cmds.rename(l_leg_sel[1], 'L_knee_jnt')
        ankle = cmds.rename(l_leg_sel[2], 'L_ankle_jnt')
        ball = cmds.rename(l_leg_sel[3], 'L_ball_jnt')
        toe = cmds.rename(l_leg_sel[4], 'L_toe_jnt')

        cmds.select(femur)
        cmds.joint(e=True, oj='xyz', sao='zdown', ch=True, zso=True)

    def L_fk_leg(self):
        # create the Fk arm by duplicating
        fk_leg = cmds.duplicate('L_femur_jnt', rc=True)

        cmds.listRelatives(fk_leg, ad=True)

        fkFemur = cmds.rename(fk_leg[0], 'L_Fk_femur_jnt')
        fkKnee = cmds.rename(fk_leg[1], 'L_Fk_knee_jnt')
        fkAnkle = cmds.rename(fk_leg[2], 'L_Fk_ankle_jnt')
        fkBall = cmds.rename(fk_leg[3], 'L_Fk_ball_jnt')
        fkToe = cmds.rename(fk_leg[4], 'L_Fk_toe_jnt')
        # create Fk Rig
        # find the worldposition ws translate position of shoulder, knee and wrist
        posTransFemur = cmds.xform(fkFemur, q=True, t=True, ws=True)
        posTransKnee = cmds.xform(fkKnee, q=True, t=True, ws=True)
        posTransAnkle = cmds.xform(fkAnkle, q=True, t=True, ws=True)
        posTransBall = cmds.xform(fkBall, q=True, t=True, ws=True)
        # find the worldposition ws orient position of shoulder, knee and wrist
        posOrientFemur = cmds.xform(fkFemur, q=True, ro=True, ws=True)
        posOrientKnee = cmds.xform(fkKnee, q=True, ro=True, ws=True)
        posOrientAnkle = cmds.xform(fkAnkle, q=True, ro=True, ws=True)
        posOrientBall = cmds.xform(fkBall, q=True, ro=True, ws=True)
        # create a group for each limb (3)
        lFkFemurGrp = cmds.group(em=True, n='L_Fk_femur_Grp')
        lFkKneeGrp = cmds.group(em=True, n='L_Fk_knee_Grp')
        lFkAnkleGrp = cmds.group(em=True, n='L_Fk_ankle_Grp')
        lFkBallGrp = cmds.group(em=True, n='L_Fk_ball_Grp')
        # create a controller for each limb (3)
        lFemurCtl = cmds.circle(n='L_Fk_femur_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        lKneeCtl = cmds.circle(n='L_Fk_knee_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        lAnkleCtl = cmds.circle(n='L_Fk_ankle_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        lBallCtl = cmds.circle(n='L_Fk_ball_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        # parent the controller to the groups
        cmds.parent('L_Fk_femur_Ctl', lFkFemurGrp)
        cmds.parent('L_Fk_knee_Ctl', lFkKneeGrp)
        cmds.parent('L_Fk_ankle_Ctl', lFkAnkleGrp)
        cmds.parent('L_Fk_ball_Ctl', lFkBallGrp)
        # freeze the orientation of the controllers
        cmds.makeIdentity('L_Fk_femur_Grp', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_knee_Grp', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_ankle_Grp', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_ball_Grp', apply=True, r=True, t=True)
        # delete history of the controllers
        cmds.delete('L_Fk_femur_Grp', ch=True)
        cmds.delete('L_Fk_knee_Grp', ch=True)
        cmds.delete('L_Fk_ankle_Grp', ch=True)
        cmds.delete('L_Fk_ball_Grp', ch=True)
        # move the group after the respected name
        cmds.xform(lFkFemurGrp, t=posTransFemur, ws=True)
        cmds.xform(lFkKneeGrp, t=posTransKnee, ws=True)
        cmds.xform(lFkAnkleGrp, t=posTransAnkle, ws=True)
        cmds.xform(lFkBallGrp, t=posTransBall, ws=True)
        # orient the group after the respected name
        cmds.xform(lFkFemurGrp, ro=posOrientFemur, ws=True)
        cmds.xform(lFkKneeGrp, ro=posOrientKnee, ws=True)
        cmds.xform(lFkAnkleGrp, ro=posOrientAnkle, ws=True)
        cmds.xform(lFkBallGrp, ro=posOrientBall, ws=True)
        # rotate the controls correctly
        cmds.rotate(0, 90, 0, 'L_Fk_femur_Ctl', relative=True)
        cmds.rotate(0, 90, 0, 'L_Fk_knee_Ctl', relative=True)
        cmds.rotate(0, 90, 0, 'L_Fk_ball_Ctl', relative=True)
        cmds.rotate(0, 90, 0, 'L_Fk_ankle_Ctl', relative=True)
        # freeze the orientation of the controllers
        cmds.makeIdentity('L_Fk_femur_Ctl', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_knee_Ctl', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_ball_Ctl', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_ankle_Ctl', apply=True, r=True, t=True)
        # delete history of the controllers
        cmds.delete('L_Fk_femur_Ctl', ch=True)
        cmds.delete('L_Fk_knee_Ctl', ch=True)
        cmds.delete('L_Fk_ankle_Ctl', ch=True)
        cmds.delete('L_Fk_ball_Ctl', ch=True)
        """
        # move the groups to the respected names location
        cmds.xform(fkFemur, t=posOrientFemur, ws=True)
        cmds.xform(fkKnee, t=posOrientKnee, ws=True)
        cmds.xform(fkAnkle, t=posOrientAnkle, ws=True)
        cmds.xform(fkBall, t=posOrientBall, ws=True)
        # freeze the orientation of the controllers
        cmds.makeIdentity('L_Fk_femur_Ctl', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_knee_Ctl', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_ankle_Ctl', apply=True, r=True, t=True)
        cmds.makeIdentity('L_Fk_ball_Ctl', apply=True, r=True, t=True)
        # delete history of the controllers
        cmds.delete('L_Fk_femur_Ctl', ch=True)
        cmds.delete('L_Fk_knee_Ctl', ch=True)
        cmds.delete('L_Fk_ankle_Ctl', ch=True)
        cmds.delete('L_Fk_ball_Ctl', ch=True)
        # position the groups to the limbs
        cmds.xform(lFkFemurGrp, t=posTransFemur, ws=True)
        cmds.xform(lFkKneeGrp, t=posTransKnee, ws=True)
        cmds.xform(lFkAnkleGrp, t=posTransAnkle, ws=True)
        cmds.xform(lFkBallGrp, t=posTransBall, ws=True)
        """
        # set the controllers to control the joint limbs
        cmds.parentConstraint('L_Fk_femur_Ctl', 'L_Fk_femur_jnt', mo=True)
        cmds.parentConstraint('L_Fk_knee_Ctl', 'L_Fk_knee_jnt', mo=True)
        cmds.parentConstraint('L_Fk_ankle_Ctl', 'L_Fk_ankle_jnt', mo=True)
        cmds.parentConstraint('L_Fk_ball_Ctl', 'L_Fk_ball_jnt', mo=True)
        # parent the controllers and groups together
        cmds.parent('L_Fk_ball_Grp', 'L_Fk_ankle_Ctl')
        cmds.parent('L_Fk_ankle_Grp', 'L_Fk_knee_Ctl')
        cmds.parent('L_Fk_knee_Grp', 'L_Fk_femur_Ctl')

    def L_ik_leg(self):
        # create the Ik arm by duplicating
        ik_leg = cmds.duplicate('L_femur_jnt', rc=True)

        cmds.listRelatives(ik_leg, ad=True)

        ik_femur = cmds.rename(ik_leg[0], 'L_Ik_femur_jnt')
        ik_knee = cmds.rename(ik_leg[1], 'L_Ik_knee_jnt')
        ik_ankle = cmds.rename(ik_leg[2], 'L_Ik_ankle_jnt')
        ik_ball = cmds.rename(ik_leg[3], 'L_Ik_ball_jnt')
        ik_toe = cmds.rename(ik_leg[4], 'L_Ik_toe_jnt')
        # create Ik Rig
        # create Rotate ikHandle between the femur and ankle
        ik_hdl_femur = cmds.ikHandle(n='L_femurAnkle_Ikh', sj=ik_femur, ee=ik_ankle, sol='ikRPsolver', p=2, w=1)
        # create Single ikHandle between the ankle and ball
        ik_hdl_ball = cmds.ikHandle(n='L_ankleBall_Ikh', sj=ik_ankle, ee=ik_ball, sol='ikSCsolver', p=2, w=1)
        # create Single ikHandle between the ball and toe
        ik_hdl_toe = cmds.ikHandle(n='L_ballToe_Ikh', sj=ik_ball, ee=ik_toe, sol='ikSCsolver', p=2, w=1)
        # find the worldspace ws translate position of the wrist
        pos_trans_ankle_ik = cmds.xform(ik_ankle, q=True, t=True, ws=True)
        pos_trans_ball_ik = cmds.xform(ik_ball, q=True, t=True, ws=True)
        pos_trans_toe_ik = cmds.xform(ik_toe, q=True, t=True, ws=True)
        # find the worldspace ws orientation position of the wrist
        pos_orient_ankle_ik = cmds.xform(ik_ankle, q=True, ro=True, ws=True)
        pos_orient_ball_ik = cmds.xform(ik_ball, q=True, ro=True, ws=True)
        pos_orient_toe_ik = cmds.xform(ik_toe, q=True, ro=True, ws=True)
        # create the empty group
        ik_grp = cmds.group(em=True, n='L_Ik_foot_Grp')
        # create the empty extra Null group
        ik_Null = cmds.group(em=True, n='L_Ik_foot_Null')
        # parent the null to the group
        cmds.parent('L_Ik_foot_Null', 'L_Ik_foot_Grp')
        # create the control
        ik_foot_ctl = cmds.circle(n='L_Ik_foot_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.0)
        ik_offset_foot_ctl = cmds.circle(n='L_Ik_offsetFoot_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.25)
        # parent the control to the group
        cmds.parent('L_Ik_offsetFoot_Ctl', 'L_Ik_foot_Ctl')
        cmds.parent('L_Ik_foot_Ctl', 'L_Ik_foot_Null')
        # change rotation order for offset control
        cmds.setAttr("L_Ik_foot_Ctl.rotateOrder", k=True, lock=True)
        cmds.setAttr("L_Ik_offsetFoot_Ctl.rotateOrder", 2)
        cmds.setAttr("L_Ik_offsetFoot_Ctl.rotateOrder", k=True, lock=True)
        # freeze ik ctl's
        # cmds.makeIdentity(ik_grp, r=True, a=True)
        # clear history of the control's
        # cmds.delete(ik_grp, ch=True)
        # move the group to the wrist
        cmds.xform(ik_grp, t=pos_trans_ankle_ik, ws=True)
        # orient the group to the wrist
        cmds.rotate(-90, -90, -90, 'L_Ik_foot_Grp', relative=True)
        cmds.rotate(90, 90, 0, 'L_Ik_foot_Ctl', relative=True)
        # cmds.xform(ik_grp, ro=pos_orient_ankle_ik, ws=True)
        # freeze ik ctl's
        cmds.makeIdentity('L_Ik_foot_Ctl', r=True, a=True)
        # clear history of the control's
        cmds.delete('L_Ik_foot_Ctl', ch=True)
        # move the group to the wrist
        cmds.xform(ik_grp, t=pos_trans_ankle_ik, ws=True)
        # create groups for the ikhandles
        peel_heel_grp = cmds.group(em=True, n="L_peelheel_Grp")
        toe_tap_grp = cmds.group(em=True, n="L_toeTap_Grp")
        toe_tap_footRoll_grp = cmds.group(em=True, n="L_toeTap_footRoll_ball_Grp")
        stand_tip_grp = cmds.group(em=True, n="L_standTip_Grp")
        stand_tip_footRoll_grp = cmds.group(em=True, n="L_standTip_footRoll_Toe_Grp")
        heel_pivot_grp = cmds.group(em=True, n="L_heelPivot_Grp")
        heel_pivot_footRoll_grp = cmds.group(em=True, n="L_heelPivot_footRoll_heel_Grp")
        twist_heel_grp = cmds.group(em=True, n="L_twistHeel_Grp")
        twist_ball_grp = cmds.group(em=True, n="L_twistBall_Grp")
        twist_toe_grp = cmds.group(em=True, n="L_twistToe_Grp")
        left_bank_grp = cmds.group(em=True, n="L_leftBank_Grp")
        right_bank_grp = cmds.group(em=True, n="L_rightBank_Grp")
        foot_attr_grp = cmds.group(em=True, n="L_footAttr_Grp")
        gimbal_grp = cmds.group(em=True, n="L_foot_gimbal_Grp")
        # place the groups
        cmds.xform(peel_heel_grp, t=pos_trans_ball_ik, ws=True)
        cmds.xform(toe_tap_grp, t=pos_trans_ball_ik, ws=True)
        cmds.xform(stand_tip_grp, t=pos_trans_toe_ik, ws=True)
        cmds.xform(heel_pivot_grp, t=pos_trans_ankle_ik, ws=True)
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
        cmds.parent(toe_tap_grp, stand_tip_grp)
        cmds.parent(toe_tap_footRoll_grp, stand_tip_grp)
        cmds.parent(peel_heel_grp, toe_tap_footRoll_grp)
        cmds.parent(stand_tip_grp, stand_tip_footRoll_grp)
        cmds.parent(stand_tip_footRoll_grp, heel_pivot_grp)
        cmds.parent(heel_pivot_grp, heel_pivot_footRoll_grp)
        cmds.parent(heel_pivot_footRoll_grp, twist_heel_grp)
        cmds.parent(twist_heel_grp, twist_ball_grp)
        cmds.parent(twist_ball_grp, twist_toe_grp)
        cmds.parent(twist_toe_grp, left_bank_grp)
        cmds.parent(left_bank_grp, right_bank_grp)
        cmds.parent(right_bank_grp, foot_attr_grp)
        cmds.parent(foot_attr_grp, gimbal_grp)
        # parent the ikhandles to the groups
        cmds.parent('L_femurAnkle_Ikh', peel_heel_grp)
        cmds.parent('L_ankleBall_Ikh', toe_tap_grp)
        cmds.parent('L_ballToe_Ikh', toe_tap_grp)
        # parent the Ikhandle GROUP to the controller
        cmds.parent("L_foot_gimbal_Grp", "L_Ik_offsetFoot_Ctl")
        # create the attributes for the foot control
        cmds.setAttr('L_Ik_foot_Ctl.visibility', e=True, k=False)
        cmds.setAttr('L_Ik_foot_Ctl.scaleX', e=True, k=False, lock=True)
        cmds.setAttr('L_Ik_foot_Ctl.scaleY', e=True, k=False, lock=True)
        cmds.setAttr('L_Ik_foot_Ctl.scaleZ', e=True, k=False, lock=True)
        # add gimbal X and set the gimbal attr keyable and editable
        cmds.addAttr('L_Ik_foot_Ctl', ln="gimbalX", at="double", dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.gimbalX', e=True, k=True)
        # add gimbal Y
        cmds.addAttr('L_Ik_foot_Ctl', ln="gimbalY", at="double", dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.gimbalY', e=True, k=True)
        # add gimbal Z
        cmds.addAttr('L_Ik_foot_Ctl', ln="gimbalZ", at="double", dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.gimbalZ', e=True, k=True)
        # break __ ___________
        cmds.addAttr('L_Ik_foot_Ctl', ln='seperator1', nn='__', at='enum', en='__________')
        cmds.setAttr('L_Ik_foot_Ctl.seperator1', e=True, k=True, lock=True)
        # PoleVector control
        cmds.addAttr('L_Ik_foot_Ctl', ln='pvControl', at='enum', en='off:on')
        cmds.setAttr('L_Ik_foot_Ctl.pvControl', e=True, k=True)
        # Leg twist
        cmds.addAttr('L_Ik_foot_Ctl', ln='legTwist', at='double', dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.legTwist', e=True, k=True)
        # offset vis
        cmds.addAttr('L_Ik_foot_Ctl', ln='offsetVis', at='enum', en='off:on')
        cmds.setAttr('L_Ik_foot_Ctl.offsetVis', e=True, k=True)
        # break __ ___________
        cmds.addAttr('L_Ik_foot_Ctl', ln='seperator2', nn='__', at='enum', en='__________')
        cmds.setAttr('L_Ik_foot_Ctl.seperator2', e=True, k=True, lock=True)
        # foot follow
        cmds.addAttr('L_Ik_foot_Ctl', ln='footFollow', at='enum', en='hip:cog:world')
        cmds.setAttr('L_Ik_foot_Ctl.footFollow', e=True, k=True)
        # break __ ___________
        cmds.addAttr('L_Ik_foot_Ctl', ln='seperator3', nn='__', at='enum', en='__________')
        cmds.setAttr('L_Ik_foot_Ctl.seperator3', e=True, k=True, lock=True)
        # foot roll, Toe break, Toe straight
        cmds.addAttr('L_Ik_foot_Ctl', ln='footRoll', at='double', dv=0)
        cmds.addAttr('L_Ik_foot_Ctl', ln='toeBreak', at='double', dv=20)
        cmds.addAttr('L_Ik_foot_Ctl', ln='toeStraight', at='double', dv=70)
        cmds.setAttr('L_Ik_foot_Ctl.footRoll', e=True, k=True)
        cmds.setAttr('L_Ik_foot_Ctl.toeBreak', e=True, k=True)
        cmds.setAttr('L_Ik_foot_Ctl.toeStraight', e=True, k=True)
        # break __ ___________
        cmds.addAttr('L_Ik_foot_Ctl', ln='seperator4', nn='__', at='enum', en='__________')
        cmds.setAttr('L_Ik_foot_Ctl.seperator4', e=True, k=True, lock=True)
        # Heel up / heel rotate up/down
        cmds.addAttr('L_Ik_foot_Ctl', ln='heelPivot', at='double', min=-10, max=10, dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.heelPivot', e=True, k=True)
        # Peel heel / heel up
        cmds.addAttr('L_Ik_foot_Ctl', ln='heelUp', at='double', min=-10, max=10, dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.heelUp', e=True, k=True)
        # Stand Tip
        cmds.addAttr('L_Ik_foot_Ctl', ln='standTip', at='double', min=-10, max=10, dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.standTip', e=True, k=True)
        # Toe Tap
        cmds.addAttr('L_Ik_foot_Ctl', ln='toeTap', at='double', min=-10, max=10, dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.toeTap', e=True, k=True)
        # Foot Bank
        cmds.addAttr('L_Ik_foot_Ctl', ln='footBank', at='double', min=-10, max=10, dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.footBank', e=True, k=True)
        # Twist Heel
        cmds.addAttr('L_Ik_foot_Ctl', ln='twistHeel', at='double', min=-10, max=10, dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.twistHeel', e=True, k=True)
        # Twist Ball
        cmds.addAttr('L_Ik_foot_Ctl', ln='twistBall', at='double', min=-10, max=10, dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.twistBall', e=True, k=True)
        # Twist Toe
        cmds.addAttr('L_Ik_foot_Ctl', ln='twistToe', at='double', min=-10, max=10, dv=0)
        cmds.setAttr('L_Ik_foot_Ctl.twistToe', e=True, k=True)

        # create the Nodes for connecting all the attributes to the control
        # Nodes for foot roll - multiplyDivide and Clamp node
        # Nodes for the space switch
        cmds.shadingNode('condition', n='L_Ik_footSpace_world_Cnd', au=True)
        cmds.shadingNode('condition', n='L_Ik_footSpace_hip_Cnd', au=True)
        cmds.shadingNode('condition', n='L_Ik_footSpace_cog_Cnd', au=True)
        cmds.setAttr('L_Ik_footSpace_world_Cnd.colorIfFalseR', 0)
        cmds.setAttr('L_Ik_footSpace_hip_Cnd.colorIfFalseR', 0)
        cmds.setAttr('L_Ik_footSpace_cog_Cnd.colorIfFalseR', 0)
        cmds.setAttr('L_Ik_footSpace_world_Cnd.colorIfTrueR', 1)
        cmds.setAttr('L_Ik_footSpace_hip_Cnd.colorIfTrueR', 1)
        cmds.setAttr('L_Ik_footSpace_cog_Cnd.colorIfTrueR', 1)
        cmds.setAttr('L_Ik_footSpace_world_Cnd.secondTerm', 2)
        cmds.setAttr('L_Ik_footSpace_hip_Cnd.secondTerm', 1)
        cmds.setAttr('L_Ik_footSpace_cog_Cnd.secondTerm', 0)
        # heel
        cmds.shadingNode('condition', n='L_heelRevFoot_Cnd', au=True)
        cmds.setAttr('L_heelRevFoot_Cnd.operation', 4)
        cmds.setAttr('L_heelRevFoot_Cnd.colorIfFalseR', 0)
        # ball
        cmds.shadingNode('setRange', n='L_ballRevFoot_Sr', au=True)
        cmds.shadingNode('plusMinusAverage', n='L_ballRevFoot_Pma', au=True)
        cmds.setAttr('L_ballRevFoot_Pma.operation', 2)
        cmds.setAttr('L_ballRevFoot_Pma.input1D[0]', 1)
        cmds.shadingNode('condition', n='L_ballRevFoot_Cnd', au=True)
        cmds.shadingNode('multiplyDivide', n='L_ballRevFoot_footRoll_Md', au=True)
        cmds.setAttr('L_ballRevFoot_footRoll_Md.operation', 1)
        # toe
        cmds.shadingNode('setRange', n='L_tipRevFoot_Sr', au=True)
        cmds.shadingNode('multiplyDivide', n='L_tipRoll_footRoll_Md', au=True)
        # Nodes for Heel up - multiplyDivide and Clamp node
        cmds.shadingNode('multiplyDivide', n='L_heelUp_Md', au=True, )
        cmds.shadingNode('clamp', n='L_heelUp_Clp', au=True)
        cmds.setAttr('L_heelUp_Md.input2X', 5)
        cmds.setAttr('L_heelUp_Clp.minR', -50)
        cmds.setAttr('L_heelUp_Clp.maxR', 50)
        # nodes for peel heel - multiplyDivide and Clamp node
        cmds.shadingNode('multiplyDivide', n='L_peelHeel_Md', au=True, )
        cmds.shadingNode('clamp', n='L_peelHeel_Clp', au=True)
        cmds.setAttr('L_peelHeel_Md.input2X', 9)
        cmds.setAttr('L_peelHeel_Clp.minR', -90)
        cmds.setAttr('L_peelHeel_Clp.maxR', 90)
        # node for stand tip - multiplyDivide and Clamp node
        cmds.shadingNode('multiplyDivide', n='L_standTip_Md', au=True, )
        cmds.shadingNode('clamp', n='L_standTip_Clp', au=True)
        cmds.setAttr('L_standTip_Md.input2X', 9)
        cmds.setAttr('L_standTip_Clp.minR', -120)
        cmds.setAttr('L_standTip_Clp.maxR', 90)
        # nodes for toe tap - multiplyDivide and Clamp node
        cmds.shadingNode('multiplyDivide', n='L_toeTap_Md', au=True, )
        cmds.shadingNode('clamp', n='L_toeTap_Clp', au=True)
        cmds.setAttr('L_toeTap_Md.input2X', 9)
        cmds.setAttr('L_toeTap_Clp.minR', -90)
        cmds.setAttr('L_toeTap_Clp.maxR', 90)
        # nodes for foot bank - multiplyDivide and Clamp node
        cmds.shadingNode('multiplyDivide', n='L_footBank_Md', au=True, )
        cmds.shadingNode('clamp', n='L_leftFootBank_Clp', au=True)
        cmds.shadingNode('clamp', n='L_rightFootBank_Clp', au=True)
        cmds.setAttr('L_footBank_Md.input2X', 9)
        cmds.setAttr('L_footBank_Md.input2Y', 9)
        cmds.setAttr('L_leftFootBank_Clp.minR', -90)
        cmds.setAttr('L_rightFootBank_Clp.maxR', 90)
        # nodes for twist heel - multiplyDivide and Clamp node
        cmds.shadingNode('multiplyDivide', n='L_twistHeel_Md', au=True, )
        cmds.shadingNode('clamp', n='L_twistHeel_Clp', au=True)
        cmds.setAttr('L_toeTap_Md.input2X', 9)
        cmds.setAttr('L_twistHeel_Clp.minR', -90)
        cmds.setAttr('L_twistHeel_Clp.maxR', 90)
        # nodes for twist ball - multiplyDivide and Clamp node
        cmds.shadingNode('multiplyDivide', n='L_twistBall_Md', au=True, )
        cmds.shadingNode('clamp', n='L_twistBall_Clp', au=True)
        cmds.setAttr('L_twistBall_Md.input2X', 9)
        cmds.setAttr('L_twistBall_Clp.minR', -90)
        cmds.setAttr('L_twistBall_Clp.maxR', 90)
        # nodes for twist toe - multiplyDivide and Clamp node
        cmds.shadingNode('multiplyDivide', n='L_twistToe_Md', au=True, )
        cmds.shadingNode('clamp', n='L_twistToe_Clp', au=True)
        cmds.setAttr('L_twistToe_Md.input2X', 9)
        cmds.setAttr('L_twistToe_Clp.minR', -90)
        cmds.setAttr('L_twistToe_Clp.maxR', 90)

        # Connecting the nodes to the groups, and connecting groups
        # Gimbal
        """
        cmds.connectAttr('L_Ik_foot_Ctl.gimbalX', 'L_foot_gimbal_Grp.rotateX')
        cmds.connectAttr('L_Ik_foot_Ctl.gimbalY', 'L_foot_gimbal_Grp.rotateY')
        cmds.connectAttr('L_Ik_foot_Ctl.gimbalZ', 'L_foot_gimbal_Grp.rotateZ')
        """
        # leg twist
        cmds.connectAttr('L_Ik_foot_Ctl.legTwist', 'L_femurAnkle_Ikh.twist')
        # offset visibility
        cmds.connectAttr('L_Ik_foot_Ctl.offsetVis', 'L_Ik_offsetFoot_Ctl.lodVisibility')
        # foot follow - create groups if not already created and parent them under
        # the skeletons joints
        # create groups
        self.util.create_space_groups(name="hip_Spa")
        self.util.create_space_groups(name="cog_Spa")
        self.util.create_space_groups(name="world_Spa")
        # move groups to the joints or controls, first get the position(xform)
        pelvis_space = cmds.xform('C_pelvis_jnt', query=True, translation=True, worldSpace=True)
        root_space = cmds.xform('C_root', query=True, translation=True, worldSpace=True)
        #
        cmds.xform("hip_Spa", t=pelvis_space, worldSpace=True)
        cmds.xform("cog_Spa", t=root_space, worldSpace=True)
        # parent the group to the nodes
        cmds.parent("hip_Spa", 'C_pelvis_jnt')
        cmds.parent("cog_Spa", 'C_root')
        # parentConstraint and setup nodes for switching between the space's
        cmds.parentConstraint('hip_Spa', "cog_Spa", "world_Spa", "L_Ik_foot_Null", maintainOffset=True)
        # combine ctl to nodes
        cmds.connectAttr('L_Ik_foot_Ctl.footFollow', 'L_Ik_footSpace_world_Cnd.firstTerm')
        cmds.connectAttr('L_Ik_foot_Ctl.footFollow', 'L_Ik_footSpace_hip_Cnd.firstTerm')
        cmds.connectAttr('L_Ik_foot_Ctl.footFollow', 'L_Ik_footSpace_cog_Cnd.firstTerm')

        cmds.connectAttr('L_Ik_footSpace_world_Cnd.firstTerm', "L_Ik_foot_Null_parentConstraint1.world_SpaW2")
        cmds.connectAttr('L_Ik_footSpace_world_Cnd.firstTerm', "L_Ik_foot_Null_parentConstraint1.cog_SpaW1")
        cmds.connectAttr('L_Ik_footSpace_world_Cnd.firstTerm', "L_Ik_foot_Null_parentConstraint1.hip_SpaW0")

        # cmds.shadingNode('condition', n='L_Ik_footSpace_world_Cnd', au=True)
        # cmds.shadingNode('condition', n='L_Ik_footSpace_hip_Cnd', au=True)
        # cmds.shadingNode('condition', n='L_Ik_footSpace_cog_Cnd', au=True)
        # Create Pole vec

        # getting controller to control the orient of the wrist
        cmds.orientConstraint('L_Ik_foot_Ctl', 'L_Ik_ankle_jnt', mo=True)
        # create a locator as a poleVector
        pv_loc = cmds.spaceLocator(n='L_leg_poleVec_Loc')
        # create a group as the group for a poleVector
        pv_grp = cmds.group(em=True, n='L_leg_poleVec_Grp')
        # parent locator to the group
        cmds.parent('L_leg_poleVec_Loc', pv_grp)
        # place the group between the shoulder and the wrist
        cmds.pointConstraint('L_Ik_femur_jnt', 'L_Ik_ankle_jnt', pv_grp)
        # aim the locator twoards the knee
        cmds.aimConstraint('L_Ik_knee_jnt', pv_grp, aim=(1, 0, 0), u=(0, 1, 0))
        # delete the constraints
        cmds.delete('L_leg_poleVec_Grp_pointConstraint1')
        cmds.delete('L_leg_poleVec_Grp_aimConstraint1')
        # place the locater out from the knee using the X axis trans
        cmds.move(5, pv_loc, z=True, a=True)
        # create controller for the polevector
        ik_knee_ctl = cmds.circle(n='L_Ik_knee_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        # rotate the controller
        # cmds.rotate(0, '90deg', 0, ik_knee_ctl)
        # move parent the controller to the locator locatieon
        cmds.pointConstraint(pv_loc, ik_knee_ctl)
        # delete pointConstraint from controller
        cmds.delete('L_Ik_knee_Ctl_pointConstraint1')
        # parent controller to grp
        cmds.parent('L_Ik_knee_Ctl', pv_grp)
        # freeze orientation on controller
        cmds.makeIdentity('L_Ik_knee_Ctl', a=True)
        # delete history on ctl
        cmds.delete('L_Ik_knee_Ctl', ch=True)
        # parent poleVEc to controller
        cmds.parent('L_leg_poleVec_Loc', 'L_Ik_knee_Ctl')
        # connect the polevector constraint to the ikhandle and the locator
        cmds.poleVectorConstraint(pv_loc, 'L_femurAnkle_Ikh')
        # hide locator
        cmds.hide(pv_loc)
        # hide scale from ik control
        cmds.setAttr('L_Ik_arm_Ctl.scaleX', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_arm_Ctl.scaleY', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_arm_Ctl.scaleZ', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_arm_Ctl.v', keyable=False, ch=False, lock=True)
        # hide rotate and scale from knee ik control
        cmds.setAttr('L_Ik_knee_Ctl.rotateX', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_knee_Ctl.rotateY', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_knee_Ctl.rotateZ', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_knee_Ctl.scaleX', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_knee_Ctl.scaleY', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_knee_Ctl.scaleZ', keyable=False, ch=False, lock=True)
        cmds.setAttr('L_Ik_knee_Ctl.v', keyable=False, ch=False, lock=True)
        # delete history on the ik control
        cmds.delete('L_Ik_foot_Ctl', ch=True)
        """
        self.util.create_space_groups(name="L_foot_Spa")          
        self.util.create_space_groups(name="R_foot_Spa")      
        self.util.create_space_groups(name="entity_Spa")
        self.util.create_space_groups(name="world_Spa")
        # move groups to the joints or controls, first get the position(xform)
        l_foot_space = cmds.xform('L_ankle_jnt', query=True, translation=True, worldSpace=True)
        r_foot_space = cmds.xform('R_ankle_jnt', query=True, translation=True, worldSpace=True)
        entity_space = cmds.xform('C_entity_Ctl', query=True, translation=True, worldSpace=True)
        #
        cmds.xform("L_foot_Spa", t=l_foot_space, worldSpace=True)
        cmds.xform("R_foot_Spa", t=r_foot_space, worldSpace=True)
        cmds.xform("entity_Spa", t=entity_space, worldSpace=True)
        # parent the group to the nodes
        cmds.parent("L_foot_Spa", 'L_ankle_jnt')
        cmds.parent("R_foot_Spa", 'R_ankle_jnt')
        cmds.parent("entity_Spa", 'C_entity_Ctl')
        # parentConstraint and setup nodes for switching between the space's
        cmds.parentConstraint('world_Spa', "entity_Spa", "R_foot_Spa", "L_foot_Spa", "L_Ik_foot_Null", maintainOffset=True) 
        """
