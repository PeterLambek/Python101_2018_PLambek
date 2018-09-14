import maya.cmds as cmds
import tf_smoothSkinWeight as tf_smooth

print "My UI"

def tf_smooth(*args):
    print 'tf_smooth'

mymenu = cmds.menu('My_Scripts', l='MyScripts', to=True, p='MayaWindow')
cmds.menuItem(label='tf_smooth', p=mymenu, command=tf_smooth)