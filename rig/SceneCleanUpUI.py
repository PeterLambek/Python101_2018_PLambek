import maya.cmds as cmds

from blue.dcc.maya.core import msvSceneCleanup
#from shared.MSVLib.msvGui.msvGuiUtils import get_main_window
from PySide2 import QtWidgets, QtCore, QtGui

from functools import partial


class SceneCleanUpUI(QtWidgets.QDockWidget):

    def __init__(self, parent):
        super(SceneCleanUpUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setFloating(True)
        self.setWindowTitle("Scene Clean Up")
        self.setFixedSize(450, 400)
        self.build_UI()

    def build_UI(self):
        self.main_widget = QtWidgets.QWidget()
        self.setWidget(self.main_widget)

        # create's the window (vertical boxLayout)
        vertical_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(vertical_layout)

        # create the cleanUp layout
        clean_up_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(clean_up_layout)

        # hide/unhide items: label, anim keys checkBox
        scene_cleanup_label_01 = QtWidgets.QLabel("Clean Up Scene")
        clean_up_layout.addWidget(scene_cleanup_label_01)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        font.setBold(True)
        scene_cleanup_label_01.setFont(font)

        # Remove anim keys #

        # create the Remove anim keys layout
        anim_keys_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(anim_keys_layout)

        # anim keys items: label, anim keys checkBox
        scene_cleanup_label_02 = QtWidgets.QLabel("Remove joint anim keys (Not SDK):")
        anim_keys_layout.addWidget(scene_cleanup_label_02)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_02.setFont(font)

        # add space between the checkbox and the label
        anim_keys_spacer = QtWidgets.QSpacerItem(30, 0)
        anim_keys_layout.addSpacerItem(anim_keys_spacer)

        self.anim_keys_checkbox = QtWidgets.QCheckBox("on / off")
        anim_keys_layout.addWidget(self.anim_keys_checkbox)
        self.anim_keys_checkbox.setMinimumWidth(60)
        self.anim_keys_checkbox.setMaximumWidth(60)
        self.anim_keys_checkbox.setChecked(True)

        # Remove unused nodes #

        # create the unUsed nodes layout
        unused_nodes_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(unused_nodes_layout)

        # unused nodes items: label, anim keys checkBox
        scene_cleanup_label_03 = QtWidgets.QLabel("Remove unsed nodes:")
        unused_nodes_layout.addWidget(scene_cleanup_label_03)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_03.setFont(font)

        # add space between the checkbox and the label
        unused_nodes_spacer = QtWidgets.QSpacerItem(30, 0)
        unused_nodes_layout.addSpacerItem(unused_nodes_spacer)

        self.unused_nodes_checkbox = QtWidgets.QCheckBox("on / off")
        unused_nodes_layout.addWidget(self.unused_nodes_checkbox)
        self.unused_nodes_checkbox.setMinimumWidth(60)
        self.unused_nodes_checkbox.setMaximumWidth(60)
        self.unused_nodes_checkbox.setChecked(True)

        # Remove unknown plug-ins #

        # create the unUsed nodes layout
        unknown_plugins_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(unknown_plugins_layout)

        # unknown plug-ins items: label, anim keys checkBox
        scene_cleanup_label_05 = QtWidgets.QLabel("Remove unknown plug-ins:")
        unknown_plugins_layout.addWidget(scene_cleanup_label_05)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_05.setFont(font)

        # add space between the checkbox and the label
        unknown_plugins_spacer = QtWidgets.QSpacerItem(30, 0)
        unknown_plugins_layout.addSpacerItem(unknown_plugins_spacer)

        self.unknow_plugins_checkbox = QtWidgets.QCheckBox("on / off")
        unknown_plugins_layout.addWidget(self.unknow_plugins_checkbox)
        self.unknow_plugins_checkbox.setMinimumWidth(60)
        self.unknow_plugins_checkbox.setMaximumWidth(60)
        self.unknow_plugins_checkbox.setChecked(True)

        # Remove unknown nodes #

        # create the unUsed nodes layout
        unknown_nodes_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(unknown_nodes_layout)

        # Remove unknown nodes items: label, anim keys checkBox
        scene_cleanup_label_04 = QtWidgets.QLabel("Remove unknown nodes:")
        unknown_nodes_layout.addWidget(scene_cleanup_label_04)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_04.setFont(font)

        # add space between the checkbox and the label
        unknown_nodes_spacer = QtWidgets.QSpacerItem(30, 0)
        unknown_nodes_layout.addSpacerItem(unknown_nodes_spacer)

        self.unknown_nodes_checkbox01 = QtWidgets.QRadioButton("all")
        unknown_nodes_layout.addWidget(self.unknown_nodes_checkbox01)
        self.unknown_nodes_checkbox01.setMinimumWidth(40)
        self.unknown_nodes_checkbox01.setMaximumWidth(40)
        self.unknown_nodes_checkbox01.setChecked(True)

        self.unknown_nodes_checkbox02 = QtWidgets.QRadioButton("noCon")
        unknown_nodes_layout.addWidget(self.unknown_nodes_checkbox02)
        self.unknown_nodes_checkbox02.setMinimumWidth(40)
        self.unknown_nodes_checkbox02.setMaximumWidth(55)
        self.unknown_nodes_checkbox02.setChecked(True)

        self.unknown_nodes_checkbox03 = QtWidgets.QRadioButton("noEffect")
        unknown_nodes_layout.addWidget(self.unknown_nodes_checkbox03)
        self.unknown_nodes_checkbox03.setMinimumWidth(40)
        self.unknown_nodes_checkbox03.setMaximumWidth(60)
        self.unknown_nodes_checkbox03.setChecked(True)


        # create the "create" button
        execute_button = QtWidgets.QPushButton("Execute clean up")
        execute_button.clicked.connect(self.execute_scene_clean_up)

        vertical_layout.addWidget(execute_button)

        # text for visibility options #

        # create the hide/Unhide layout
        hide_unhide_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(hide_unhide_layout)

        # hide/unhide items: label, anim keys checkBox
        scene_cleanup_label_06 = QtWidgets.QLabel("Hide/Unhide Options")
        hide_unhide_layout.addWidget(scene_cleanup_label_06)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        font.setBold(True)
        scene_cleanup_label_06.setFont(font)

        # Hide output/input from channelbox #

        # create the unUsed nodes layout
        channelbox_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(channelbox_layout)

        # unknown plug-ins items: label, anim keys checkBox
        scene_cleanup_label_07 = QtWidgets.QLabel("controls output/input from channelbox")
        channelbox_layout.addWidget(scene_cleanup_label_07)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_07.setFont(font)

        # add space between the checkbox and the label
        channel_box_spacer = QtWidgets.QSpacerItem(30, 0)
        channelbox_layout.addSpacerItem(channel_box_spacer)

        self.hide_output_input_btn = QtWidgets.QPushButton("hide")
        channelbox_layout.addWidget(self.hide_output_input_btn)
        self.hide_output_input_btn.setMaximumWidth(60)
        self.hide_output_input_btn.setMinimumWidth(60)
        self.hide_output_input_btn.clicked.connect(partial(msvSceneCleanup.toggle_input_output_hide, 0))

        self.unhide_output_input_tn = QtWidgets.QPushButton("unhide")
        channelbox_layout.addWidget(self.unhide_output_input_tn)
        self.unhide_output_input_tn.setMaximumWidth(60)
        self.unhide_output_input_tn.setMinimumWidth(60)
        self.unhide_output_input_tn.clicked.connect(partial(msvSceneCleanup.toggle_input_output_hide, 1))

        # Hide bones "Drawstyle" #

        # create the Hide bones layout
        hide_bone_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(hide_bone_layout)

        # Hide bones items: label, anim keys checkBox
        option_label_07 = QtWidgets.QLabel("Joint/bones in scene")
        hide_bone_layout.addWidget(option_label_07)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        option_label_07.setFont(font)

        ##create the check box for the hide/unhide selection option UI
        self.bone_visibility = QtWidgets.QCheckBox("selection")
        hide_bone_layout.addWidget(self.bone_visibility)
        self.bone_visibility.setMinimumWidth(65)
        self.bone_visibility.setMaximumWidth(65)
        self.bone_visibility.setChecked(False)

        # create the hide bones button UI
        hide_bone_btn = QtWidgets.QPushButton("hide")
        hide_bone_layout.addWidget(hide_bone_btn)
        hide_bone_btn.setMaximumWidth(60)
        hide_bone_btn.setMinimumWidth(60)
        # connect the unhide bone button to the tool function
        hide_bone_btn.clicked.connect(partial(self.toggle_bone_visibility, 2))

        # create the unhide bones button UI
        unhide_bone_btn = QtWidgets.QPushButton("unhide")
        hide_bone_layout.addWidget(unhide_bone_btn)
        unhide_bone_btn.setMaximumWidth(60)
        unhide_bone_btn.setMinimumWidth(60)
        ##connect the unhide bone button to the tool function
        unhide_bone_btn.clicked.connect(partial(self.toggle_bone_visibility, 0))

        # toggle channelbox translate, rotate, scale, visibility#

        # create breakup/seperator text
        text_channelbox_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(text_channelbox_layout)

        # hide/unhide items: label, anim keys checkBox
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        text_channelbox_layout.addWidget(line)

        # translate

        # create the unUsed nodes layout
        translate_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(translate_layout)

        # Remove unknown nodes items: label, anim keys checkBox
        scene_cleanup_label_09 = QtWidgets.QLabel("translate:")
        translate_layout.addWidget(scene_cleanup_label_09)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_09.setFont(font)

        # add space between the checkbox and the label
        translate_spacer = QtWidgets.QSpacerItem(30, 0)
        translate_layout.addSpacerItem(translate_spacer)

        self.translate_x_checkbox = QtWidgets.QCheckBox("X")
        translate_layout.addWidget(self.translate_x_checkbox)
        self.translate_x_checkbox.setMinimumWidth(42)
        self.translate_x_checkbox.setMaximumWidth(42)
        self.translate_x_checkbox.setChecked(True)

        self.translate_y_checkbox = QtWidgets.QCheckBox("Y")
        translate_layout.addWidget(self.translate_y_checkbox)
        self.translate_y_checkbox.setMinimumWidth(40)
        self.translate_y_checkbox.setMaximumWidth(40)
        self.translate_y_checkbox.setChecked(True)

        self.translate_z_checkbox = QtWidgets.QCheckBox("Z")
        translate_layout.addWidget(self.translate_z_checkbox)
        self.translate_z_checkbox.setMinimumWidth(40)
        self.translate_z_checkbox.setMaximumWidth(40)
        self.translate_z_checkbox.setChecked(True)

        self.translate_all_checkbox = QtWidgets.QCheckBox("all")
        translate_layout.addWidget(self.translate_all_checkbox)
        self.translate_all_checkbox.setMinimumWidth(60)
        self.translate_all_checkbox.setMaximumWidth(60)
        self.translate_all_checkbox.setChecked(True)

        self.translate_all_checkbox.toggled.connect(self.translate_x_checkbox.setChecked)
        self.translate_all_checkbox.toggled.connect(self.translate_y_checkbox.setChecked)
        self.translate_all_checkbox.toggled.connect(self.translate_z_checkbox.setChecked)

        # rotate

        # create the unUsed nodes layout
        rotate_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(rotate_layout)

        # Remove unknown nodes items: label, anim keys checkBox
        scene_cleanup_label_10 = QtWidgets.QLabel("rotate:")
        rotate_layout.addWidget(scene_cleanup_label_10)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_10.setFont(font)

        # add space between the checkbox and the label
        rotate_spacer = QtWidgets.QSpacerItem(30, 0)
        rotate_layout.addSpacerItem(rotate_spacer)

        self.rotate_x_checkbox = QtWidgets.QCheckBox("X")
        rotate_layout.addWidget(self.rotate_x_checkbox)
        self.rotate_x_checkbox.setMinimumWidth(42)
        self.rotate_x_checkbox.setMaximumWidth(42)
        self.rotate_x_checkbox.setChecked(True)

        self.rotate_y_checkbox = QtWidgets.QCheckBox("Y")
        rotate_layout.addWidget(self.rotate_y_checkbox)
        self.rotate_y_checkbox.setMinimumWidth(40)
        self.rotate_y_checkbox.setMaximumWidth(40)
        self.rotate_y_checkbox.setChecked(True)

        self.rotate_z_checkbox = QtWidgets.QCheckBox("Z")
        rotate_layout.addWidget(self.rotate_z_checkbox)
        self.rotate_z_checkbox.setMinimumWidth(40)
        self.rotate_z_checkbox.setMaximumWidth(40)
        self.rotate_z_checkbox.setChecked(True)

        self.rotate_all_checkbox = QtWidgets.QCheckBox("all")
        rotate_layout.addWidget(self.rotate_all_checkbox)
        self.rotate_all_checkbox.setMinimumWidth(60)
        self.rotate_all_checkbox.setMaximumWidth(60)
        self.rotate_all_checkbox.setChecked(True)

        self.rotate_all_checkbox.toggled.connect(self.rotate_x_checkbox.setChecked)
        self.rotate_all_checkbox.toggled.connect(self.rotate_y_checkbox.setChecked)
        self.rotate_all_checkbox.toggled.connect(self.rotate_z_checkbox.setChecked)

        # scale

        # create the unUsed nodes layout
        scale_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(scale_layout)

        # Remove unknown nodes items: label, anim keys checkBox
        scene_cleanup_label_11 = QtWidgets.QLabel("scale:")
        scale_layout.addWidget(scene_cleanup_label_11)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_11.setFont(font)

        # add space between the checkbox and the label
        scale_spacer = QtWidgets.QSpacerItem(30, 0)
        scale_layout.addSpacerItem(scale_spacer)

        self.scale_x_checkbox = QtWidgets.QCheckBox("X")
        scale_layout.addWidget(self.scale_x_checkbox)
        self.scale_x_checkbox.setMinimumWidth(42)
        self.scale_x_checkbox.setMaximumWidth(42)
        self.scale_x_checkbox.setChecked(True)

        self.scale_y_checkbox = QtWidgets.QCheckBox("Y")
        scale_layout.addWidget(self.scale_y_checkbox)
        self.scale_y_checkbox.setMinimumWidth(40)
        self.scale_y_checkbox.setMaximumWidth(40)
        self.scale_y_checkbox.setChecked(True)

        self.scale_z_checkbox = QtWidgets.QCheckBox("Z")
        scale_layout.addWidget(self.scale_z_checkbox)
        self.scale_z_checkbox.setMinimumWidth(40)
        self.scale_z_checkbox.setMaximumWidth(40)
        self.scale_z_checkbox.setChecked(True)

        self.scale_all_checkbox = QtWidgets.QCheckBox("all")
        scale_layout.addWidget(self.scale_all_checkbox)
        self.scale_all_checkbox.setMinimumWidth(60)
        self.scale_all_checkbox.setMaximumWidth(60)
        self.scale_all_checkbox.setChecked(True)

        self.scale_all_checkbox.toggled.connect(self.scale_x_checkbox.setChecked)
        self.scale_all_checkbox.toggled.connect(self.scale_y_checkbox.setChecked)
        self.scale_all_checkbox.toggled.connect(self.scale_z_checkbox.setChecked)

        # visibility

        # create the unUsed nodes layout
        visibility_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(visibility_layout)

        # Remove unknown nodes items: label, anim keys checkBox
        scene_cleanup_label_12 = QtWidgets.QLabel("visibility:")
        visibility_layout.addWidget(scene_cleanup_label_12)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_12.setFont(font)

        # add space between the checkbox and the label
        visibility_spacer = QtWidgets.QSpacerItem(30, 0)
        visibility_layout.addSpacerItem(visibility_spacer)

        self.visibility_checkbox = QtWidgets.QCheckBox("visibility")
        visibility_layout.addWidget(self.visibility_checkbox)
        self.visibility_checkbox.setMinimumWidth(60)
        self.visibility_checkbox.setMaximumWidth(60)
        self.visibility_checkbox.setChecked(True)

        # radius

        # create the unUsed nodes layout
        radius_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(radius_layout)

        # Remove unknown nodes items: label, anim keys checkBox
        scene_cleanup_label_13 = QtWidgets.QLabel("radius:")
        radius_layout.addWidget(scene_cleanup_label_13)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        scene_cleanup_label_13.setFont(font)

        # add space between the checkbox and the label
        radius_spacer = QtWidgets.QSpacerItem(30, 0)
        radius_layout.addSpacerItem(radius_spacer)

        self.radius_checkbox = QtWidgets.QCheckBox("radius")
        radius_layout.addWidget(self.radius_checkbox)
        self.radius_checkbox.setMinimumWidth(60)
        self.radius_checkbox.setMaximumWidth(60)
        self.radius_checkbox.setChecked(True)

        # create the "create" button

        execute_attr_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(execute_attr_layout)

        self.execute_hide_button = QtWidgets.QPushButton("hide")
        execute_attr_layout.addWidget(self.execute_hide_button)
        self.execute_hide_button.clicked.connect(self.execute_attr_hide)

        self.execute_unhide_button = QtWidgets.QPushButton("unhide")
        execute_attr_layout.addWidget(self.execute_unhide_button)
        self.execute_unhide_button.clicked.connect(self.execute_attr_unhide)

        self.execute_lock_button = QtWidgets.QPushButton("lock")
        execute_attr_layout.addWidget(self.execute_lock_button)
        self.execute_lock_button.clicked.connect(self.execute_attr_lock)

        self.execute_unlock_button = QtWidgets.QPushButton("unlock")
        execute_attr_layout.addWidget(self.execute_unlock_button)
        self.execute_unlock_button.clicked.connect(self.execute_attr_unlock)

        # hide/lock and unhide/unlock button

        execute_attr_lock_hide_layout = QtWidgets.QHBoxLayout()
        vertical_layout.addLayout(execute_attr_lock_hide_layout)

        self.execute_hide_lock_button = QtWidgets.QPushButton("lock and hide")
        execute_attr_lock_hide_layout.addWidget(self.execute_hide_lock_button)
        self.execute_hide_lock_button.clicked.connect(self.execute_attr_lock)
        self.execute_hide_lock_button.clicked.connect(self.execute_attr_hide)

        self.execute_unhide_unlock_button = QtWidgets.QPushButton("unlock and unhide")
        execute_attr_lock_hide_layout.addWidget(self.execute_unhide_unlock_button)
        self.execute_unhide_unlock_button.clicked.connect(self.execute_attr_unlock)
        self.execute_unhide_unlock_button.clicked.connect(self.execute_attr_unhide)

    def execute_scene_clean_up(self):
        """ setup connection from sceneCleanUp tool to UI """
        state_check_box_01 = self.anim_keys_checkbox.isChecked()
        state_check_box_02 = self.unused_nodes_checkbox.isChecked()
        state_check_box_03 = self.unknow_plugins_checkbox.isChecked()
        #state_check_box_04 = self.unknown_nodes_checkbox01.isChecked()
        #state_check_box_05 = self.unknown_nodes_checkbox02.isChecked()
        #state_check_box_06 = self.unknown_nodes_checkbox03.isChecked()

        if state_check_box_01:
            msvSceneCleanup.delete_anim_keys()

        if state_check_box_02:
            msvSceneCleanup.delete_unused_nodes()

        if state_check_box_03:
            msvSceneCleanup.remove_unknown_plugins()

        # if state_check_box_04:
        # msvSceneCleanup.delete_all_unknown_nodes()

        # if state_check_box_05:
        # msvSceneCleanup.delete_unknown_nodes()

        # if state_check_box_06 :
        # msvSceneCleanup.delete_all_unknown_nodes()

    def toggle_bone_visibility(self, state):
        """ toggle visibility for bones with or without selection using an on/off checkbox """
        if self.bone_visibility.isChecked():
            joint_list = cmds.ls(selection=True, type="joint")
        else:
            joint_list = cmds.ls(type="joint")

        msvSceneCleanup.toggle_bone_visibility(joint_list, state)

    def execute_attr_lock(self):
        """  lock checked attributes """
        # translate attributes
        trans_x = self.translate_x_checkbox.isChecked()
        trans_y = self.translate_y_checkbox.isChecked()
        trans_z = self.translate_z_checkbox.isChecked()

        if trans_x:
            msvSceneCleanup.toggle_attr_lock(["tx"])
        if trans_y:
            msvSceneCleanup.toggle_attr_lock(["ty"])
        if trans_z:
            msvSceneCleanup.toggle_attr_lock(["tz"])

        # rotate attributes

        rot_x = self.rotate_x_checkbox.isChecked()
        rot_y = self.rotate_y_checkbox.isChecked()
        rot_z = self.rotate_z_checkbox.isChecked()

        if rot_x:
            msvSceneCleanup.toggle_attr_lock(["rx"])
        if rot_y:
            msvSceneCleanup.toggle_attr_lock(["ry"])
        if rot_z:
            msvSceneCleanup.toggle_attr_lock(["rz"])

        # scale attributes

        scl_x = self.scale_x_checkbox.isChecked()
        scl_y = self.scale_y_checkbox.isChecked()
        scl_z = self.scale_z_checkbox.isChecked()

        if scl_x:
            msvSceneCleanup.toggle_attr_lock(["sx"])
        if scl_y:
            msvSceneCleanup.toggle_attr_lock(["sy"])
        if scl_z:
            msvSceneCleanup.toggle_attr_lock(["sz"])

        # visibility attribute

        vis = self.visibility_checkbox.isChecked()

        # joint radius attribute

        if vis:
            msvSceneCleanup.toggle_attr_lock(["visibility"])

        rad = self.visibility_checkbox.isChecked()

        if rad:
            msvSceneCleanup.toggle_attr_lock(["radius"])

    def execute_attr_hide(self):
        """  hide checked attributes """
        trans_x = self.translate_x_checkbox.isChecked()
        trans_y = self.translate_y_checkbox.isChecked()
        trans_z = self.translate_z_checkbox.isChecked()

        if trans_x:
            msvSceneCleanup.toggle_attr_hide(["tx"])
        if trans_y:
            msvSceneCleanup.toggle_attr_hide(["ty"])
        if trans_z:
            msvSceneCleanup.toggle_attr_hide(["tz"])

        rot_x = self.rotate_x_checkbox.isChecked()
        rot_y = self.rotate_y_checkbox.isChecked()
        rot_z = self.rotate_z_checkbox.isChecked()

        if rot_x:
            msvSceneCleanup.toggle_attr_hide(["rx"])
        if rot_y:
            msvSceneCleanup.toggle_attr_hide(["ry"])
        if rot_z:
            msvSceneCleanup.toggle_attr_hide(["rz"])

        scl_x = self.scale_x_checkbox.isChecked()
        scl_y = self.scale_y_checkbox.isChecked()
        scl_z = self.scale_z_checkbox.isChecked()

        if scl_x:
            msvSceneCleanup.toggle_attr_hide(["sx"])
        if scl_y:
            msvSceneCleanup.toggle_attr_hide(["sy"])
        if scl_z:
            msvSceneCleanup.toggle_attr_hide(["sz"])

        vis = self.visibility_checkbox.isChecked()

        if vis:
            msvSceneCleanup.toggle_attr_hide(["visibility"])

        rad = self.visibility_checkbox.isChecked()

        if rad:
            msvSceneCleanup.toggle_attr_hide(["radius"])

    def execute_attr_unlock(self):
        """  unlock checked attributes """
        # translate attributes
        trans_x = self.translate_x_checkbox.isChecked()
        trans_y = self.translate_y_checkbox.isChecked()
        trans_z = self.translate_z_checkbox.isChecked()

        if trans_x:
            msvSceneCleanup.toggle_attr_unlock(["tx"])
        if trans_y:
            msvSceneCleanup.toggle_attr_unlock(["ty"])
        if trans_z:
            msvSceneCleanup.toggle_attr_unlock(["tz"])

        # rotate attributes
        rot_x = self.rotate_x_checkbox.isChecked()
        rot_y = self.rotate_y_checkbox.isChecked()
        rot_z = self.rotate_z_checkbox.isChecked()

        if rot_x:
            msvSceneCleanup.toggle_attr_unlock(["rx"])
        if rot_y:
            msvSceneCleanup.toggle_attr_unlock(["ry"])
        if rot_z:
            msvSceneCleanup.toggle_attr_unlock(["rz"])

        # scale attributes
        scl_x = self.scale_x_checkbox.isChecked()
        scl_y = self.scale_y_checkbox.isChecked()
        scl_z = self.scale_z_checkbox.isChecked()

        if scl_x:
            msvSceneCleanup.toggle_attr_unlock(["sx"])
        if scl_y:
            msvSceneCleanup.toggle_attr_unlock(["sy"])
        if scl_z:
            msvSceneCleanup.toggle_attr_unlock(["sz"])

        # visibility attribute
        vis = self.visibility_checkbox.isChecked()

        # joint radius attribute
        if vis:
            msvSceneCleanup.toggle_attr_unlock(["visibility"])

        rad = self.visibility_checkbox.isChecked()

        if rad:
            msvSceneCleanup.toggle_attr_unlock(["radius"])

    def execute_attr_unhide(self):
        """  unhide checked attributes """
        trans_x = self.translate_x_checkbox.isChecked()
        trans_y = self.translate_y_checkbox.isChecked()
        trans_z = self.translate_z_checkbox.isChecked()

        if trans_x:
            msvSceneCleanup.toggle_attr_unhide(["tx"])
        if trans_y:
            msvSceneCleanup.toggle_attr_unhide(["ty"])
        if trans_z:
            msvSceneCleanup.toggle_attr_unhide(["tz"])

        rot_x = self.rotate_x_checkbox.isChecked()
        rot_y = self.rotate_y_checkbox.isChecked()
        rot_z = self.rotate_z_checkbox.isChecked()

        if rot_x:
            msvSceneCleanup.toggle_attr_unhide(["rx"])
        if rot_y:
            msvSceneCleanup.toggle_attr_unhide(["ry"])
        if rot_z:
            msvSceneCleanup.toggle_attr_unhide(["rz"])

        scl_x = self.scale_x_checkbox.isChecked()
        scl_y = self.scale_y_checkbox.isChecked()
        scl_z = self.scale_z_checkbox.isChecked()

        if scl_x:
            msvSceneCleanup.toggle_attr_unhide(["sx"])
        if scl_y:
            msvSceneCleanup.toggle_attr_unhide(["sy"])
        if scl_z:
            msvSceneCleanup.toggle_attr_unhide(["sz"])

        vis = self.visibility_checkbox.isChecked()

        if vis:
            msvSceneCleanup.toggle_attr_unhide(["visibility"])

        rad = self.visibility_checkbox.isChecked()

        if rad:
            msvSceneCleanup.toggle_attr_unhide(["radius"])


def main():
    maya_window = get_main_window()

    for child in maya_window.children():
        if child.__class__.__name__ == "SceneCleanUpUI":
            child.close()
            break

    cleanup_tool = SceneCleanUpUI(maya_window)
    cleanup_tool.show()
