#--------------------
# Screen Spacer
# by Beau C. Pratt
# 
# A tool for fixing the visual flicker that happens 
# when a character is animated in stepped mode with a moving camera.
#
#--------------------

import maya.cmds as cmds
import maya.mel as mel

#--------------------
# Screen Space Shelf
#--------------------

#define the load script
#def loadSS(*args):
#   import screenspacer
#   reload(screenspacer)

# get top shelf
gShelfTopLevel = mel.eval("$tmpVar=$gShelfTopLevel")
print (gShelfTopLevel)

# get top shelf names
shelves = cmds.tabLayout(gShelfTopLevel, query=1, ca=1)
print (shelves)

# create shelf
ShelfName = 'Custom'

if ShelfName not in shelves:
    cmds.shelfLayout(ShelfName, parent=gShelfTopLevel)

# get existing members
names = cmds.shelfLayout(ShelfName, query=True, childArray=True) or []
labels = [cmds.shelfButton(n, query=True, label=True) for n in names]

print (names)
print (labels)

# prep shelf tool

shelfTool = 'ScreenSpacer'

# delete existing button

if shelfTool in labels:
    index = labels.index(shelfTool)
    cmds.deleteUI(names[index])

# bring in image
ssImage='screenspacer_Icon'

# add button
cmds.shelfButton(style="iconOnly", parent=ShelfName, label='ScreenSpacer', image1=ssImage, command='''
import screenspacer_Script
reload(screenspacer_Script) 
''')