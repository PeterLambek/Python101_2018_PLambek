import maya.cmds as cmds
import rigui.ui as ui

print "My Startup"

# Change the current time unit to ntsc
cmds.currentUnit(time='ntsc')

# change the current linear unit to centimeters
cmds.currentUnit(linear='cm')
