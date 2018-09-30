import maya.cmds as cmds
import os
import json
from PySide2 import QtWidgets, QtCore, QtGui

#create first the joints - shoulder, elbow, wrist, wristEnd (no need for naming)
#selection to a variable


import maya.cmds as cmds


rig_jnt_list = [['Rig_shoulder', [1.0, 0, 0]], ['Rig_elbow', [3.0, 0, -1.0]], ['Rig_wrist', [5.0, 0, 0]],
                ['Rig_wristEnd', [6.0, 0, 0.0]]]
ik_jnt_list = [['Ik_shoulder', [1.0, 0, 0]], ['Ik_elbow', [3.0, 0, -1.0]], ['Ik_wrist', [5.0, 0, 0]],
               ['Ik_wristEnd', [6.0, 0, 0]]]
fk_jnt_list = [['Fk_shoulder', [1.0, 0, 0]], ['Fk_elbow', [3.0, 0, -1.0]], ['Fk_wrist', [5.0, 0, 0]],
               ['Fk_wristEnd', [6.0, 0, 0]]]



class Rig_Arm:

    def rig_arm(self):
        # create left rig, ik, fk joints
        self.create_joint(rig_jnt_list)
        cmds.select(d=True)
        self.create_joint(ik_jnt_list)
        cmds.select(d=True)
        self.create_joint(fk_jnt_list)
        cmds.select(d=True)

        # create Ik Rig
        # ik handle
        ikh = cmds.ikHandle(n='L_arm_Ikh', sj='L_Ik_shoulder', ee='L_Ik_wrist', sol='ikRPsolver', p=2, w=1)

        ik_ctl_info = [[ik_jnt_list[2][1], 'L_Ik_arm_Ctl', 'L_Ik_arm_Ctl_Grp']]
        self.create_control(ik_ctl_info)

        pvpos = self.calculatePVPosition([ik_jnt_list[0][0], [ik_jnt_list[1][0], [ik_jnt_list[2][0])
        pvctlinfo = [[pvpos, 'pv_arm_Ctl', 'ik_arm_Ctl']]
        self.create_control(pvctlinfo)

        #parent ik handle to ctl
        cmds.parent('L_arm_ikh', 'L_Ik_arm_Ctl')
        #PV Constraint
        cmds.poleVectorConstraint(pvctlinfo[0][1], ikh[0])
        # orient constraint to arm ik_wrist to arm_Ctl
        cmds.orientConstraint(pvctlinfo[0][1], ikh[0])

        # create FK rig
        fk_ctl_info = [[fk_jnt_list[0][1], 'L_Fk_shoulder_Ctl', 'L_Fk_shoulder_Ctl_Grp'],
                       [fk_jnt_list[1][1], 'Fk_elbow_Ctl', 'Fk_elbow_Ctl_Grp'],
                       [fk_jnt_list[2][1], 'Fk_wrist_Ctl', 'Fk_wrist_Ctl_Grp']]

        self.create_control(fk_ctl_info)

        #parent fk controls
        cmds.parent(fk_ctl_info[1][2], fk_ctl_info[0][1])
        cmds.parent(fk_ctl_info[2][2], fk_ctl_info[1][1])


    def create_joint(self, jntinfo):
        for item in jntinfo:
            cmds.joint(n='L_' + item[0], p=item[1], radius=1)


    def create_control(self, ctlinfo):
        for info in ctlinfo:
            # create ik control
            # get the ws=worldspace position of wrist joint
            pos = info[0]
            # create an empty group
            ctlgrp = cmds.group(em=True, name=info[2])
            # create circle control
            ctl = cmds.circle(n='L_' + info[1], nr=(0, 0, 1), c=(0, 0, 0), r=0.35)
            # parent the ctl to the group
            cmds.parent(ctl, ctlgrp)
            # move the group to the object
            cmds.xform(ctlgrp, t=pos, ws=True)


    def calculatePVPosition(self, jnts):
        from maya import cmds, OpenMaya
        start = cmds.xform(jnts[0], q=True, ws=True, t=True)
        mid = cmds.xform(jnts[1], q=True, ws=True, t=True)
        end = cmds.xform(jnts[2], q=True, ws=True, t=True)
        startV = OpenMaya.MVector(start[0], start[1], start[2])
        midV = OpenMaya.MVector(mid[0], mid[1], mid[2])
        endV = OpenMaya.MVector(end[0], end[1], end[2])
        startEnd = endV - startV
        startMid = midV - startV
        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        arrowV *= 0.5
        finalV = arrowV + midV
        return ([finalV.x, finalV.y, finalV.z])

"""
def L_bind_arm(self):

    l_arm_sel = cmds.ls(selection=True)
    left_arm = [l_arm_sel[0], l_arm_sel[1], l_arm_sel[2], l_arm_sel[3]]

    shldr = cmds.rename(l_arm_sel[0], 'L_shoulder_jnt')
    elbw = cmds.rename(l_arm_sel[1], 'L_elbow_jnt')
    wrst = cmds.rename(l_arm_sel[2], 'L_wrist_jnt')
    wrst_end = cmds.rename(l_arm_sel[3], 'L_wristEnd_jnt')

    cmds.select(d=True)
    cmds.joint(shldr, e=True, oj='xyz', sao='yup', ch=True, zso=True)


def L_fk_arm(self):

    # create the Fk arm by duplicating
    fk_arm = cmds.duplicate('L_shoulder_jnt', rc=True)

    cmds.listRelatives(fk_arm, ad=True)

    fk_shldr = cmds.rename(fk_arm[0], 'L_Fk_shoulder_jnt')
    fk_elbw = cmds.rename(fk_arm[1], 'L_Fk_elbow_jnt')
    fk_wrst = cmds.rename(fk_arm[2], 'L_Fk_wrist_jnt')
    fk_wrst_end = cmds.rename(fk_arm[3], 'L_Fk_wristEnd_jnt')

    # create Fk Rig

    # find the worldposition ws translate position of shoulder, elbow and wrist
    pos_trans_shoulder = cmds.xform(fk_shldr, q=True, t=True, ws=True)
    pos_trans_elbow = cmds.xform(fk_elbw, q=True, t=True, ws=True)
    pos_trans_wrist = cmds.xform(fk_wrst, q=True, t=True, ws=True)

    # find the worldposition ws orient position of shoulder, elbow and wrist
    pos_orient_shoulder = cmds.xform(fk_shldr, q=True, t=True, ws=True)
    pos_orient_elbow = cmds.xform(fk_elbw, q=True, t=True, ws=True)
    pos_orient_wrist = cmds.xform(fk_wrst, q=True, t=True, ws=True)

    # create a group for each limb (3)
    l_fk_shldr_grp = cmds.group(em=True, n='L_Fk_shoulder_Grp')
    l_fk_elbw_grp = cmds.group(em=True, n='L_Fk_elbow_Grp')
    l_fk_wrst_grp = cmds.group(em=True, n='L_Fk_wrist_Grp')
    # create a controller for each limb (3)

    l_shldr_ctl = cmds.circle(n='L_Fk_shoulder_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5  )
    l_elbw_ctl = cmds.circle(n='L_Fk_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5 )
    l_wrst_ctl = cmds.circle(n='L_Fk_wrist_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5 )

    # orient the group after the respected name
    cmds.xform(l_fk_shldr_grp, ro=pos_orient_shoulder, ws=True)
    cmds.xform(l_fk_elbw_grp, ro=pos_orient_elbow, ws=True)
    cmds.xform(l_fk_wrst_grp, ro=pos_orient_wrist, ws=True)
    # parent the controller to the groups
    cmds.parent(l_shldr_ctl, l_fk_shldr_grp)
    cmds.parent(l_elbw_ctl, l_fk_elbw_grp)
    cmds.parent(l_wrst_ctl, l_fk_wrst_grp)
    # move the groups to the respected names location
    cmds.xform(fk_shldr, t=pos_trans_shoulder, ws=True)
    cmds.xform(fk_elbw, t=pos_trans_elbow, ws=True)
    cmds.xform(fk_wrst, t=pos_trans_wrist, ws=True)
    # freeze the orientation of the controllers
    cmds.makeIdentity(l_shldr_ctl, apply=True, r=True, t=True)
    cmds.makeIdentity(l_elbw_ctl, apply=True, r=True, t=True)
    cmds.makeIdentity(l_wrst_ctl, apply=True, r=True, t=True)
    # delete history of the controllers
    cmds.delete('L_Fk_shoulder_Ctl', ch=True)
    cmds.delete('L_Fk_elbow_Ctl', ch=True)
    cmds.delete('L_Fk_wrist_Ctl', ch=True)
    # position the groups to the limbs
    cmds.xform(l_fk_shldr_grp, t=pos_trans_shoulder, ws=True)
    cmds.xform(l_fk_elbw_grp, t=pos_trans_elbow, ws=True)
    cmds.xform(l_fk_wrst_grp, t=pos_trans_wrist, ws=True)
    # set the controllers to control the joint limbs
    cmds.parentConstraint('L_Fk_shoulder_Ctl', 'L_Fk_shoulder_jnt', mo=True)
    cmds.parentConstraint('L_Fk_elbow_Ctl', 'L_Fk_elbow_jnt', mo=True)
    cmds.parentConstraint('L_Fk_wrist_Ctl', 'L_Fk_wrist_jnt', mo=True)
    # parent the controllers and groups together
    cmds.parent('L_Fk_wrist_Grp', 'L_Fk_elbow_Ctl')
    cmds.parent('L_Fk_elbow_Grp','L_Fk_shoulder_Ctl' )


def L_ik_arm(self):
    # create the Ik arm by duplicating
    ik_arm = cmds.duplicate('L_shoulder_jnt', rc=True)

    cmds.listRelatives(ik_arm, ad=True)

    ik_shldr = cmds.rename(ik_arm[0], 'L_Ik_shoulder_jnt')
    ik_elbw = cmds.rename(ik_arm[1], 'L_Ik_elbow_jnt')
    ik_wrst = cmds.rename(ik_arm[2], 'L_Ik_wrist_jnt')
    ik_wrst_end = cmds.rename(ik_arm[3], 'L_Ik_wristEnd_jnt')

    # create Ik Rig

    ik_hdl = cmds.ikHandle(n='L_arm_Ikh', sj=ik_shldr, ee=ik_wrst, sol='ikRPsolver', p=2, w=1)
    # find the worldspace ws translate position of the wrist
    pos_trans_ik = cmds.xform(ik_wrst, q=True, t=True, ws=True)
    # find the worldspace ws orientation position of the wrist
    pos_orient_ik = cmds.xform(ik_wrst, q=True, ro=True, ws=True)
    # create the empty group
    ik_grp = cmds.group(em=True, n='L_Ik_arm_Grp')
    # create the control
    ik_hnd_ctl = cmds.circle(n='L_Ik_arm_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=1.0 )
    # orient the group to the wrist
    cmds.xform(ik_grp, ro=pos_orient_ik, ws=True)
    # parent the control to the group
    cmds.parent(ik_hnd_ctl, ik_grp)
    # freeze ik ctl
    cmds.makeIdentity(ik_hnd_ctl, r=True, a=True)
    # move the group to the wrist
    cmds.xform(ik_grp, t=pos_trans_ik, ws=True)
    # parent the Ikhandle to the controller
    cmds.parent('L_arm_Ikh', ik_hnd_ctl)
    # getting controller to control the orient of the wrist
    cmds.orientConstraint(ik_hnd_ctl, ik_wrst, mo=True)
    # create a locator as a poleVector
    pv_loc = cmds.spaceLocator(n='L_poleVec_Loc')
    # create a group as the group for a poleVector
    pv_grp = cmds.group(em=True, n='L_poleVec_Grp')
    # parent locator to the group
    cmds.parent(pv_loc, pv_grp)
    # place the group between the shoulder and the wrist
    cmds.pointConstraint(ik_shldr, ik_wrst, pv_grp)
    # aim the locator twoards the elbow
    cmds.aimConstraint(ik_elbw, pv_grp, aim=(1,0,0), u=(0,1,0))
    # delete the constraints
    cmds.delete('L_poleVec_Grp_pointConstraint1')
    cmds.delete('L_poleVec_Grp_aimConstraint1')
    # place the locater out from the elbow using the X axis trans
    cmds.move(-5, pv_loc, x=True, a=True)
    #create controller for the polevector
    ik_elbw_ctl = cmds.circle(n='L_Ik_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5 )
    # rotate the controller
    cmds.rotate(0, '90deg', 0, ik_elbw_ctl)
    # move parent the controller to the locator locatieon
    cmds.pointConstraint(pv_loc, ik_elbw_ctl)
    # delete pointConstraint from controller
    cmds.delete('L_Ik_elbow_Ctl_pointConstraint1')
    # parent controller to grp
    cmds.parent(ik_elbw_ctl, pv_grp)
    # freeze orientation on controller
    cmds.makeIdentity(ik_elbw_ctl, a=True)
    # delete history on ctl
    cmds.delete(ik_elbw_ctl, ch=True)
    # parent poleVEc to controller
    cmds.parent(pv_loc, 'L_Ik_elbow_Ctl')
    # connect the polevector constraint to the ikhandle and the locator
    cmds.poleVectorConstraint(pv_loc, 'L_arm_Ikh')
    # hide locator
    cmds.hide(pv_loc)
    # hide scale from ik control
    cmds.setAttr('L_Ik_arm_Ctl.scaleX', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_Ik_arm_Ctl.scaleY', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_Ik_arm_Ctl.scaleZ', keyable=False, ch=False, lock=True)

    cmds.setAttr('L_Ik_arm_Ctl.v', keyable=False, ch=False, lock=True)

    #hide rotate and scale from elbow ik control
    cmds.setAttr('L_Ik_elbow_Ctl.rotateX', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_Ik_elbow_Ctl.rotateY', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_Ik_elbow_Ctl.rotateZ', keyable=False, ch=False, lock=True)

    cmds.setAttr('L_Ik_elbow_Ctl.scaleX', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_Ik_elbow_Ctl.scaleY', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_Ik_elbow_Ctl.scaleZ', keyable=False, ch=False, lock=True)

    cmds.setAttr('L_Ik_elbow_Ctl.v', keyable=False, ch=False, lock=True)

    #delete history on the ik control
    cmds.delete(ik_hnd_ctl, ch=True)

def connect_ikfk():

    ik_shldr = 'L_Ik_shoulder_jnt'
    ik_elbw = 'L_Ik_elbow_jnt'
    ik_wrst = 'L_Ik_wrist_jnt'
    ik_wrst_end = 'L_Ik_wristEnd_jnt'

    fk_shldr = 'L_Fk_shoulder_jnt'
    fk_elbw = 'L_Fk_elbow_jnt'
    fk_wrst = 'L_Fk_wrist_jnt'
    fk_wrst_end = 'L_Ff_wristEnd_jnt'

    # find the worldposition ws translate position of shoulder, elbow and wrist
    pos_trans_shoulder = cmds.xform(fk_shldr, q=True, t=True, ws=True)
    pos_trans_elbow = cmds.xform(fk_elbw, q=True, t=True, ws=True)
    pos_trans_wrist = cmds.xform(fk_wrst, q=True, t=True, ws=True)

    # find the worldposition ws orient position of shoulder, elbow and wrist
    pos_orient_shoulder = cmds.xform(fk_shldr, q=True, t=True, ws=True)
    pos_orient_elbow = cmds.xform(fk_elbw, q=True, t=True, ws=True)
    pos_orient_wrist = cmds.xform(fk_wrst, q=True, t=True, ws=True)

    # create a group for each limb (3)
    l_fk_shldr_grp = cmds.group(em=True, n='L_Fk_shoulder_Grp')
    l_fk_elbw_grp = cmds.group(em=True, n='L_Fk_elbow_Grp')
    l_fk_wrst_grp = cmds.group(em=True, n='L_Fk_wrist_Grp')
    # create a controller for each limb (3)

    l_shldr_ctl = cmds.circle(n='L_Fk_shoulder_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5  )
    l_elbw_ctl = cmds.circle(n='L_Fk_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5 )
    l_wrst_ctl = cmds.circle(n='L_Fk_wrist_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5 )

    # orient the group after the respected name
    cmds.xform(l_fk_shldr_grp, ro=pos_orient_shoulder, ws=True)
    cmds.xform(l_fk_elbw_grp, ro=pos_orient_elbow, ws=True)
    cmds.xform(l_fk_wrst_grp, ro=pos_orient_wrist, ws=True)
    # parent the controller to the groups
    cmds.parent(l_shldr_ctl, l_fk_shldr_grp)
    cmds.parent(l_elbw_ctl, l_fk_elbw_grp)
    cmds.parent(l_wrst_ctl, l_fk_wrst_grp)
    # move the groups to the respected names location
    cmds.xform(fk_shldr, t=pos_trans_shoulder, ws=True)
    cmds.xform(fk_elbw, t=pos_trans_elbow, ws=True)
    cmds.xform(fk_wrst, t=pos_trans_wrist, ws=True)
    # freeze the orientation of the controllers
    cmds.makeIdentity(l_shldr_ctl, apply=True, r=True, t=True)
    cmds.makeIdentity(l_elbw_ctl, apply=True, r=True, t=True)
    cmds.makeIdentity(l_wrst_ctl, apply=True, r=True, t=True)
    # delete history of the controllers
    cmds.delete('L_Fk_shoulder_Ctl', ch=True)
    cmds.delete('L_Fk_elbow_Ctl', ch=True)
    cmds.delete('L_Fk_wrist_Ctl', ch=True)
    # position the groups to the limbs
    cmds.xform(l_fk_shldr_grp, t=pos_trans_shoulder, ws=True)
    cmds.xform(l_fk_elbw_grp, t=pos_trans_elbow, ws=True)
    cmds.xform(l_fk_wrst_grp, t=pos_trans_wrist, ws=True)
    # set the controllers to control the joint limbs
    cmds.parentConstraint('L_Fk_shoulder_Ctl', 'L_Fk_shoulder_jnt', mo=True)
    cmds.parentConstraint('L_Fk_elbow_Ctl', 'L_Fk_elbow_jnt', mo=True)
    cmds.parentConstraint('L_Fk_wrist_Ctl', 'L_Fk_wrist_jnt', mo=True)
    # parent the controllers and groups together
    cmds.parent('L_Fk_wrist_Grp', 'L_Fk_elbow_Ctl')
    cmds.parent('L_Fk_elbow_Grp','L_Fk_shoulder_Ctl' )

    # connect the Ik and the Fk to the bind

    # create 3 pairblend node to switch between ik and fk
    pb_shldr = cmds.shadingNode('pairBlend', au=True, n='L_shoulder_Pb')
    pb_elbw = cmds.shadingNode('pairBlend', au=True, n='L_elbow_Pb')
    pb_wrst = cmds.shadingNode('pairBlend', au=True, n='L_wrist_Pb')
    # connect the Ik to the pairblend node
    cmds.connectAttr('L_Ik_shoulder_jnt.rotate','L_shoulder_Pb.inRotate1', f=True)
    cmds.connectAttr('L_Ik_elbow_jnt.rotate','L_elbow_Pb.inRotate1', f=True)
    cmds.connectAttr('L_Ik_wrist_jnt.rotate','L_wrist_Pb.inRotate1', f=True)
    # connect the fk to the pairblend node
    cmds.connectAttr('L_Fk_shoulder_jnt.rotate','L_shoulder_Pb.inRotate2', f=True)
    cmds.connectAttr('L_Fk_elbow_jnt.rotate','L_elbow_Pb.inRotate2', f=True)
    cmds.connectAttr('L_Fk_wrist_jnt.rotate','L_wrist_Pb.inRotate2', f=True)
    # connect the pairblend node to the rig
    cmds.connectAttr('L_shoulder_Pb.outRotate','L_shoulder_jnt.rotate', f=True)
    cmds.connectAttr('L_elbow_Pb.outRotate','L_elbow_jnt.rotate', f=True)
    cmds.connectAttr('L_wrist_Pb.outRotate','L_wrist_jnt.rotate', f=True)
    # create control to switch between the ik and fk
    ik_fk_ctl = cmds.circle(n='L_IkFkSwitch_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.75  )
    # create a group for the switch control
    ik_fk_grp = cmds.group(em=True, n='L_IkFkSwitch_Grp')
    # parent the switch controller to the group
    cmds.parent(ik_fk_ctl, ik_fk_grp)
    # place the group above the hand
    cmds.xform(ik_fk_grp, t=pos_trans_wrist, ws=True)
    cmds.xform(ik_fk_grp, t=pos_orient_wrist, ws=True)
    # turn the control to be horizontal and move it up
    cmds.xform(ik_fk_ctl, r=True, ro=(-90, 0, 0))
    cmds.xform(ik_fk_ctl, r=True, t=(0, 2, 0))
    # freeze the controlle
    cmds.makeIdentity(ik_fk_ctl, a=True)
    # remove history
    cmds.delete(ik_fk_ctl, ch=True)
    # hide and lock channel controls
    cmds.setAttr('L_IkFkSwitch_Ctl.translateX', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_IkFkSwitch_Ctl.translateY', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_IkFkSwitch_Ctl.translateZ', keyable=False, ch=False, lock=True)

    cmds.setAttr('L_IkFkSwitch_Ctl.rotateX', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_IkFkSwitch_Ctl.rotateY', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_IkFkSwitch_Ctl.rotateZ', keyable=False, ch=False, lock=True)

    cmds.setAttr('L_IkFkSwitch_Ctl.scaleX', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_IkFkSwitch_Ctl.scaleY', keyable=False, ch=False, lock=True)
    cmds.setAttr('L_IkFkSwitch_Ctl.scaleZ', keyable=False, ch=False, lock=True)

    cmds.setAttr('L_IkFkSwitch_Ctl.v', keyable=False, ch=False, lock=True)
    # create attributes on the controller for ik fk switch, and the visibility
    cmds.addAttr('L_IkFkSwitch_Ctl', ln="ikFkVisibility", at='enum', en='auto:both:', k=True)
    cmds.addAttr('L_IkFkSwitch_Ctl', ln="ikFkSwitch", at='enum', en='Ik:Fk:', k=True)
    # connect the pairBlend to the ikFkSwitch
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_shoulder_Pb.weight')
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_elbow_Pb.weight')
    cmds.connectAttr('L_IkFkSwitch_Ctl.ikFkSwitch', 'L_wrist_Pb.weight')
    # hide controls based on the selection ikFkVisibility attribute
    # create condition node and two reverse nodes for the setup
    rev1 = cmds.shadingNode('reverse', n="L_ikFkVisibility01_Rev", au=True)
    rev2 = cmds.shadingNode('reverse', n="L_ikFkVisibility02_Rev", au=True)
    cnd = cmds.shadingNode('condition', n="L_ikFkVisibility_Cnd", au=True)
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

    #get the ik fk switch group to follow the bind wrist
    cmds.parentConstraint('L_wrist_jnt', ik_fk_grp)
"""
