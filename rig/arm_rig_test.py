import maya.cmds as cmds

jnt_list = {'LJNTS': [['shoulder', [1.0, 0, 0]], ['elbow', [3.0, 0, -1.0]], ['wrist', [5.0, 0, 0]], ['wristEnd', [6.0, 0, 0.0]]],
            'RJNTS': [['shoulder', [-1.0, 0, 0]], ['elbow', [-3.0, 0, -1.0]], ['wrist', [-5.0, 0, 0]],['wristEnd', [-6.0, 0, 0]]]}
# set the definition for the joints
arm_list = ['Rig_', 'Ik_', 'Fk_']


class Rig_Arm:

    def l_arm_rig(self):

        #create joints
        self.lcreateJoint()
        cmds.joint('L_Rig_shoulder', e=True, oj='xyz', sao='yup', ch=True, zso=True)
        cmds.joint('L_Ik_shoulder', e=True, oj='xyz', sao='yup', ch=True, zso=True)
        cmds.joint('L_Fk_shoulder', e=True, oj='xyz', sao='yup', ch=True, zso=True)
        cmds.select(d=True)
        #create left and right ikhandle
        self.lIkSetup()
        #create fk setup
        self.lFkSetup()

    def r_arm_rig(self):

        #create joints
        self.rcreateJoint()
        cmds.joint('R_Rig_shoulder', e=True, oj='xyz', sao='yup', ch=True, zso=True)
        cmds.joint('R_Ik_shoulder', e=True, oj='xyz', sao='yup', ch=True, zso=True)
        cmds.joint('R_Fk_shoulder', e=True, oj='xyz', sao='yup', ch=True, zso=True)
        cmds.select(d=True)
        #create left and right ikhandle
        self.rIkSetup()
        #create fk setup
        self.rFkSetup()

    def lconnect(self):

        #connect ik, fk and rig
        self.lconnectIkFk()

    def rconnect(self):

        #connect ik, fk and rig
        self.rconnectIkFk()



    def lcreateJoint(self):

        for item in arm_list:
            for jnt in jnt_list['LJNTS']:
                jnt_name = 'L_' + item + jnt[0]
                cmds.joint(n=jnt_name, p=jnt[1], radius=1)

            cmds.select(d=True)

    # right side joint setup

    def rcreateJoint(self):
        for item in arm_list:
            for jnt in jnt_list['RJNTS']:
                jnt_name = 'R_' + item + jnt[0]
                cmds.joint(n=jnt_name, p=jnt[1], radius=1)

            cmds.select(d=True)



    def lIkSetup(self):
        cmds.ikHandle(n='L_arm_Ikh', sj='L_Ik_shoulder', ee='L_Ik_wrist', sol='ikRPsolver', p=2, w=1)
        # find the worldspace ws translate position of the wrist
        posTransIk = cmds.xform('L_Ik_wrist', q=True, t=True, ws=True)
        # find the worldspace ws orientation position of the wrist
        posOrientIk = cmds.xform('L_Ik_wrist', q=True, ro=True, ws=True)
        # create the empty group
        cmds.group(em=True, n='L_Ik_arm_Grp')
        # create the control
        cmds.circle(n='L_Ik_arm_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.35)
        # orient the group to the wrist
        cmds.xform('L_Ik_arm_Grp', ro=posOrientIk, ws=True)
        # parent the control to the group
        cmds.parent('L_Ik_arm_Ctl', 'L_Ik_arm_Grp')
        # move the group to the wrist
        cmds.xform('L_Ik_arm_Grp', t=posTransIk, ws=True)
        # parent the Ikhandle to the controller
        cmds.parent('L_arm_Ikh', 'L_Ik_arm_Ctl')
        # getting controller to control the orient of the wrist
        cmds.orientConstraint('L_Ik_arm_Ctl', 'L_Ik_wrist', mo=True)
        # create a locator as a poleVector
        cmds.spaceLocator(n='L_poleVec_Loc')
        # create a group as the group for a poleVector
        cmds.group(em=True, n='L_poleVec_Grp')
        # parent locator to the group
        cmds.parent('L_poleVec_Loc', 'L_poleVec_Grp')
        # place the group between the shoulder and the wrist
        cmds.pointConstraint('L_Ik_shoulder', 'L_Ik_wrist', 'L_poleVec_Grp')
        # aim the locator twoards the elbow
        cmds.aimConstraint('L_Ik_elbow', 'L_poleVec_Grp', aim=(1, 0, 0), u=(0, 1, 0))
        # delete the constraints
        cmds.delete('L_poleVec_Grp_pointConstraint1')
        cmds.delete('L_poleVec_Grp_aimConstraint1')
        # place the locater out from the elbow using the X axis trans
        cmds.move(-5, 'L_poleVec_Loc', z=True, a=True)
        # create controller for the polevector
        cmds.circle(n='L_Ik_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        # rotate the controller
        cmds.rotate(0, '90deg', 0, 'L_Ik_elbow_Ctl')
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


    def rIkSetup(self):
        cmds.ikHandle(n='R_arm_Ikh', sj='R_Ik_shoulder', ee='R_Ik_wrist', sol='ikRPsolver', p=2, w=1)
        # find the worldspace ws translate position of the wrist
        posTransIk = cmds.xform('R_Ik_wrist', q=True, t=True, ws=True)
        # find the worldspace ws orientation position of the wrist
        posOrientIk = cmds.xform('R_Ik_wrist', q=True, ro=True, ws=True)
        # create the empty group
        cmds.group(em=True, n='R_Ik_arm_Grp')
        # create the control
        cmds.circle(n='R_Ik_arm_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.35)
        # orient the group to the wrist
        cmds.xform('R_Ik_arm_Grp', ro=posOrientIk, ws=True)
        # parent the control to the group
        cmds.parent('R_Ik_arm_Ctl', 'R_Ik_arm_Grp')
        # move the group to the wrist
        cmds.xform('R_Ik_arm_Grp', t=posTransIk, ws=True)
        # parent the Ikhandle to the controller
        cmds.parent('R_arm_Ikh', 'R_Ik_arm_Ctl')
        # getting controller to control the orient of the wrist
        cmds.orientConstraint('R_Ik_arm_Ctl', 'R_Ik_wrist', mo=True)
        # create a locator as a poleVector
        cmds.spaceLocator(n='R_poleVec_Loc')
        # create a group as the group for a poleVector
        cmds.group(em=True, n='R_poleVec_Grp')
        # parent locator to the group
        cmds.parent('R_poleVec_Loc', 'R_poleVec_Grp')
        # place the group between the shoulder and the wrist
        cmds.pointConstraint('R_Ik_shoulder', 'R_Ik_wrist', 'R_poleVec_Grp')
        # aim the locator twoards the elbow
        cmds.aimConstraint('R_Ik_elbow', 'R_poleVec_Grp', aim=(1, 0, 0), u=(0, 1, 0))
        # delete the constraints
        cmds.delete('R_poleVec_Grp_pointConstraint1')
        cmds.delete('R_poleVec_Grp_aimConstraint1')
        # place the locater out from the elbow using the X axis trans
        cmds.move(-5, 'R_poleVec_Loc', z=True, a=True)
        # create controller for the polevector
        cmds.circle(n='R_Ik_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        # rotate the controller
        cmds.rotate(0, '90deg', 0, 'R_Ik_elbow_Ctl')
        # move parent the controller to the locator locatieon
        cmds.pointConstraint('R_poleVec_Loc', 'R_Ik_elbow_Ctl')
        # delete pointConstraint from controller
        cmds.delete('R_Ik_elbow_Ctl_pointConstraint1')
        # parent controller to grp
        cmds.parent('R_Ik_elbow_Ctl', 'R_poleVec_Grp')
        # freeze orientation on controller
        cmds.makeIdentity('R_Ik_elbow_Ctl', a=True)
        # parent poleVEc to controller
        cmds.parent('R_poleVec_Loc', 'R_Ik_elbow_Ctl')
        # connect the polevector constraint to the ikhandle and the locator
        cmds.poleVectorConstraint('R_poleVec_Loc', 'R_arm_Ikh')
        # hide locator
        cmds.hide('R_poleVec_Loc')

        # create Fk Rig


    def lFkSetup(self):
        # find the worldposition ws translate position of shoulder, elbow and wrist
        posTransShoulder = cmds.xform('L_Fk_shoulder', q=True, t=True, ws=True)
        posTransElbow = cmds.xform('L_Fk_elbow', q=True, t=True, ws=True)
        posTransWrist = cmds.xform('L_Fk_wrist', q=True, t=True, ws=True)
        # find the worldposition ws orient position of shoulder, elbow and wrist
        posOrientShoulder = cmds.xform('L_Fk_shoulder', q=True, t=True, ws=True)
        posOrientElbow = cmds.xform('L_Fk_elbow', q=True, t=True, ws=True)
        posOrientWrist = cmds.xform('L_Fk_wrist', q=True, t=True, ws=True)
        # create a group for each limb (3)
        cmds.group(em=True, n='L_Fk_shoulder_Grp')
        cmds.group(em=True, n='L_Fk_elbow_Grp')
        cmds.group(em=True, n='L_Fk_wrist_Grp')
        # create a controller for each limb (3)
        cmds.circle(n='L_Fk_shoulder_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        cmds.circle(n='L_Fk_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        cmds.circle(n='L_Fk_wrist_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        # orient the group after the respected name
        cmds.xform('L_Fk_shoulder_Grp', ro=posOrientShoulder, ws=True)
        cmds.xform('L_Fk_elbow_Grp', ro=posOrientElbow, ws=True)
        cmds.xform('L_Fk_wrist_Grp', ro=posOrientWrist, ws=True)
        # parent the controller to the groups
        cmds.parent('L_Fk_shoulder_Ctl', 'L_Fk_shoulder_Grp')
        cmds.parent('L_Fk_elbow_Ctl', 'L_Fk_elbow_Grp')
        cmds.parent('L_Fk_wrist_Ctl', 'L_Fk_wrist_Grp')
        # move the groups to the respected names location
        cmds.xform('L_Fk_shoulder', t=posTransShoulder, ws=True)
        cmds.xform('L_Fk_elbow', t=posTransElbow, ws=True)
        cmds.xform('L_Fk_wrist', t=posTransWrist, ws=True)
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
        cmds.parentConstraint('L_Fk_shoulder_Ctl', 'L_Fk_shoulder', mo=True)
        cmds.parentConstraint('L_Fk_elbow_Ctl', 'L_Fk_elbow', mo=True)
        cmds.parentConstraint('L_Fk_wrist_Ctl', 'L_Fk_wrist', mo=True)
        # parent the controllers and groups together
        cmds.parent('L_Fk_wrist_Grp', 'L_Fk_elbow_Ctl')
        cmds.parent('L_Fk_elbow_Grp', 'L_Fk_shoulder_Ctl')


    def rFkSetup(self):
        # find the worldposition ws translate position of shoulder, elbow and wrist
        posTransShoulder = cmds.xform('R_Fk_shoulder', q=True, t=True, ws=True)
        posTransElbow = cmds.xform('R_Fk_elbow', q=True, t=True, ws=True)
        posTransWrist = cmds.xform('R_Fk_wrist', q=True, t=True, ws=True)
        # find the worldposition ws orient position of shoulder, elbow and wrist
        posOrientShoulder = cmds.xform('R_Fk_shoulder', q=True, t=True, ws=True)
        posOrientElbow = cmds.xform('R_Fk_elbow', q=True, t=True, ws=True)
        posOrientWrist = cmds.xform('R_Fk_wrist', q=True, t=True, ws=True)
        # create a group for each limb (3)
        cmds.group(em=True, n='R_Fk_shoulder_Grp')
        cmds.group(em=True, n='R_Fk_elbow_Grp')
        cmds.group(em=True, n='R_Fk_wrist_Grp')
        # create a controller for each limb (3)
        cmds.circle(n='R_Fk_shoulder_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        cmds.circle(n='R_Fk_elbow_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        cmds.circle(n='R_Fk_wrist_Ctl', nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
        # orient the group after the respected name
        cmds.xform('R_Fk_shoulder_Grp', ro=posOrientShoulder, ws=True)
        cmds.xform('R_Fk_elbow_Grp', ro=posOrientElbow, ws=True)
        cmds.xform('R_Fk_wrist_Grp', ro=posOrientWrist, ws=True)
        # parent the controller to the groups
        cmds.parent('R_Fk_shoulder_Ctl', 'R_Fk_shoulder_Grp')
        cmds.parent('R_Fk_elbow_Ctl', 'R_Fk_elbow_Grp')
        cmds.parent('R_Fk_wrist_Ctl', 'R_Fk_wrist_Grp')
        # move the groups to the respected names location
        cmds.xform('R_Fk_shoulder', t=posTransShoulder, ws=True)
        cmds.xform('R_Fk_elbow', t=posTransElbow, ws=True)
        cmds.xform('R_Fk_wrist', t=posTransWrist, ws=True)
        # freeze the orientation of the controllers
        cmds.makeIdentity('R_Fk_shoulder_Ctl', apply=True, r=True, t=True)
        cmds.makeIdentity('R_Fk_elbow_Ctl', apply=True, r=True, t=True)
        cmds.makeIdentity('R_Fk_wrist_Ctl', apply=True, r=True, t=True)
        # delete history of the controllers
        cmds.delete('R_Fk_shoulder_Ctl', ch=True)
        cmds.delete('R_Fk_elbow_Ctl', ch=True)
        cmds.delete('R_Fk_wrist_Ctl', ch=True)
        # position the groups to the limbs
        cmds.xform('R_Fk_shoulder_Grp', t=posTransShoulder, ws=True)
        cmds.xform('R_Fk_elbow_Grp', t=posTransElbow, ws=True)
        cmds.xform('R_Fk_wrist_Grp', t=posTransWrist, ws=True)
        # set the controllers to control the joint limbs
        cmds.parentConstraint('R_Fk_shoulder_Ctl', 'R_Fk_shoulder', mo=True)
        cmds.parentConstraint('R_Fk_elbow_Ctl', 'R_Fk_elbow', mo=True)
        cmds.parentConstraint('R_Fk_wrist_Ctl', 'R_Fk_wrist', mo=True)
        # parent the controllers and groups together
        cmds.parent('R_Fk_wrist_Grp', 'R_Fk_elbow_Ctl')
        cmds.parent('R_Fk_elbow_Grp', 'R_Fk_shoulder_Ctl')


    # connect the Ik and the Fk to the bind
    def lconnectIkFk(self):
        # this is done to many times, and should be boiled down when introducing class
        # find the worldposition ws translate position of shoulder, elbow and wrist
        posTransWrist = cmds.xform('L_Fk_wrist', q=True, t=True, ws=True)
        # find the worldposition ws orient position of shoulder, elbow and wrist
        posOrientWrist = cmds.xform('L_Fk_wrist', q=True, t=True, ws=True)
        # create 3 pairblend node to switch between ik and fk
        cmds.shadingNode('pairBlend', au=True, n='L_shoulder_Pb')
        cmds.shadingNode('pairBlend', au=True, n='L_elbow_Pb')
        cmds.shadingNode('pairBlend', au=True, n='L_wrist_Pb')
        # connect the Ik to the pairblend node
        cmds.connectAttr('L_Ik_shoulder.rotate', 'L_shoulder_Pb.inRotate1', f=True)
        cmds.connectAttr('L_Ik_elbow.rotate', 'L_elbow_Pb.inRotate1', f=True)
        cmds.connectAttr('L_Ik_wrist.rotate', 'L_wrist_Pb.inRotate1', f=True)
        # connect the fk to the pairblend node
        cmds.connectAttr('L_Fk_shoulder.rotate', 'L_shoulder_Pb.inRotate2', f=True)
        cmds.connectAttr('L_Fk_elbow.rotate', 'L_elbow_Pb.inRotate2', f=True)
        cmds.connectAttr('L_Fk_wrist.rotate', 'L_wrist_Pb.inRotate2', f=True)
        # connect the pairblend node to the rig
        cmds.connectAttr('L_shoulder_Pb.outRotate', 'L_Rig_shoulder.rotate', f=True)
        cmds.connectAttr('L_elbow_Pb.outRotate', 'L_Rig_elbow.rotate', f=True)
        cmds.connectAttr('L_wrist_Pb.outRotate', 'L_Rig_wrist.rotate', f=True)
        # create control to switch between the ik and fk
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
        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_poleVec_Grp.visibility')
        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorG', 'L_Ik_shoulder.visibility')
        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder_Grp.visibility')
        cmds.connectAttr('L_ikFkVisibility_Cnd.outColorR', 'L_Fk_shoulder.visibility')


    def rconnectIkFk(self):
        # this is done to many times, and should be boiled down when introducing class
        # find the worldposition ws translate position of shoulder, elbow and wrist
        posTransWrist = cmds.xform('R_Fk_wrist', q=True, t=True, ws=True)
        # find the worldposition ws orient position of shoulder, elbow and wrist
        posOrientWrist = cmds.xform('R_Fk_wrist', q=True, t=True, ws=True)
        # create 3 pairblend node to switch between ik and fk
        cmds.shadingNode('pairBlend', au=True, n='R_shoulder_Pb')
        cmds.shadingNode('pairBlend', au=True, n='R_elbow_Pb')
        cmds.shadingNode('pairBlend', au=True, n='R_wrist_Pb')
        # connect the Ik to the pairblend node
        cmds.connectAttr('R_Ik_shoulder.rotate', 'R_shoulder_Pb.inRotate1', f=True)
        cmds.connectAttr('R_Ik_elbow.rotate', 'R_elbow_Pb.inRotate1', f=True)
        cmds.connectAttr('R_Ik_wrist.rotate', 'R_wrist_Pb.inRotate1', f=True)
        # connect the fk to the pairblend node
        cmds.connectAttr('R_Fk_shoulder.rotate', 'R_shoulder_Pb.inRotate2', f=True)
        cmds.connectAttr('R_Fk_elbow.rotate', 'R_elbow_Pb.inRotate2', f=True)
        cmds.connectAttr('R_Fk_wrist.rotate', 'R_wrist_Pb.inRotate2', f=True)
        # connect the pairblend node to the rig
        cmds.connectAttr('R_shoulder_Pb.outRotate', 'R_Rig_shoulder.rotate', f=True)
        cmds.connectAttr('R_elbow_Pb.outRotate', 'R_Rig_elbow.rotate', f=True)
        cmds.connectAttr('R_wrist_Pb.outRotate', 'R_Rig_wrist.rotate', f=True)
        # create control to switch between the ik and fk
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
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorG', 'R_Ik_shoulder.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorR', 'R_Fk_shoulder_Grp.visibility')
        cmds.connectAttr('R_ikFkVisibility_Cnd.outColorR', 'R_Fk_shoulder.visibility')


