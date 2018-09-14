from Biped import armRig
import maya.cmds as cmds
import os
import json
from Qt import QtWidgets, QtCore, QtGui

"""
USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'bipedUI')


def createDirectory(directory=DIRECTORY):
    
    function creates given directory if it dosen't exist already
    :param directory(str): directory to create
    :return:
    
    if not os.path.exists(directory):
        os.mkdir(directory)
"""
#from functools import partial

class autoBipedUI(QtWidgets.QDockWidget):

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

