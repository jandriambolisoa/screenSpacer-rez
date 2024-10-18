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

def ssShelf( *args ):
	#--------------------
	# Screen Space Shelf
	#--------------------

	#define the load script
	def loadSS(*args):
		import screenspacer
		reload(screenspacer)

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
	cmds.shelfButton(style="iconOnly", parent=ShelfName, label='ScreenSpacer', image1=ssImage, command="loadSS()") 
	
	
	
#--------------------
# Screen Space Script
#--------------------

def screenSpacer( *args ):
    #Prep Scene for Screen Space
        
    startTime=cmds.playbackOptions(query=True, minTime=True) #sets time to be a string for current time
    endTime=cmds.playbackOptions(query=True, maxTime=True) #sets maxTime to be string for full scene length
    cmds.currentTime(startTime) #sets time to frame 1
    
    slaveObj = cmds.ls(slave)[0].rpartition(':')[2]
    con="_parentConstraint1"
    slaveCon=slaveObj+con
    cmds.select(master, replace=True)    #selects only the master
    cmds.select(slave, add=True)         #add slave to selection
    
    cmds.parentConstraint(master, slave, maintainOffset=True, weight=1)    #constrains Master and Slave
    
    cmds.select(slave)
    cmds.setKeyframe(".translate",".rotate")
    cmds.setAttr(".blendParent1", 0)    #set blendParent value to 0
    cmds.setKeyframe(".blendParent1")    #set key
        
    #Update & Key Offsets
    
    def updateKey():
        cmds.select(slaveCon)
        
        cmds.parentConstraint(master, slave, edit=True, maintainOffset=True)
        cmds.setKeyframe(".target[0].targetOffsetTranslateX")
        cmds.setKeyframe(".target[0].targetOffsetTranslateY")
        cmds.setKeyframe(".target[0].targetOffsetTranslateZ")
        cmds.setKeyframe(".target[0].targetOffsetRotateX")
        cmds.setKeyframe(".target[0].targetOffsetRotateY")
        cmds.setKeyframe(".target[0].targetOffsetRotateZ")
    
    updateKey()
    
    #Advance Time One Frame
    
    time=cmds.currentTime(query=True)
    cmds.currentTime(time+1)
        
    #Start Screen Space Loop
    
    while (time < endTime) == True:  #evaluates if the current time is less than the max time
            cmds.select(charAnim)
            frame=cmds.currentTime(query=True)
            #If there is a key
            if cmds.selectKey( charAnim, time=(frame,frame)) > 0: #Evaluates if the current frame is keyed or not
                cmds.select(slave)
                cmds.setAttr(".blendParent1", 0)    #set blendParent value to 0
                cmds.setKeyframe(".blendParent1")    #set key
                updateKey()
                time=cmds.currentTime(query=True)
                cmds.currentTime(time+1)
           #If there is no key
            else:
                cmds.select(slave)
                cmds.setAttr(".blendParent1", 1)    #set blendParent value to 0
                cmds.setKeyframe(".blendParent1")    #set key
                updateKey()
                time=cmds.currentTime(query=True)
                cmds.currentTime(time+1)
    else:
            cmds.select(charAnim)
            frame=cmds.currentTime(query=True)
            #If there is a key
            if cmds.selectKey( charAnim, time=(frame,frame)) > 0: #Evaluates if the current frame is keyed or not
                cmds.select(slave)
                cmds.setAttr(".blendParent1", 0)    #set blendParent value to 0
                cmds.setKeyframe(".blendParent1")    #set key
                updateKey()
            #If there is no key
            else:
                cmds.select(slave)
                cmds.setAttr(".blendParent1", 1)    #set blendParent value to 0
                cmds.setKeyframe(".blendParent1")    #set key
                updateKey()
                
#End of Screen Space
    
    cmds.select(slave)

    cmds.bakeResults(simulation=True, smart=1, time=(startTime,endTime)) #bake constraint
    
    if cmds.objExists(slaveCon):
        cmds.delete(slaveCon) #delete constraint
    else:
        print("Constraint was baked out")  
                  
    for blendAttr in slave: 
        print(blendAttr)
        
    if cmds.attributeQuery("blendParent1", node=blendAttr, exists=True):
        cmds.deleteAttr(".blendParent1")
    else:
        print("Attribute was baked out")    
                 
    cmds.currentTime(startTime)
    cmds.select( clear=True )
    
#--------------------
# Screen Space UI
#--------------------

def screenSpacerUI( *args ):
    
    windowID = "screenSpacer"
       
    if cmds.window( windowID, exists=True):
        cmds.deleteUI( windowID )

    def fetchRoot(*args):
        global slave
        slave=cmds.ls(selection=True, objectsOnly=True)
        root = []
        
        for obj in slave: 
            print(obj)
        
        txtRoot = cmds.textField('tRoot', edit=True, text=obj)
        
    def fetchCtrl(*args):
        global charAnim
        charAnim=cmds.ls(selection=True, objectsOnly=True)
        ctrl = []
        
        for obj in charAnim: 
            print(obj)
        
        txtCtrl = cmds.textField('tCtrl', edit=True, text=obj)
    
    def fetchCam(*args):
        global master    
        master=cmds.ls(selection=True, objectsOnly=True)  
        cam = []
        
        for obj in master: 
            print(obj)
        
        txtCam = cmds.textField('tCam', edit=True, text=obj)
        
    window = cmds.window( windowID, title="Screen Spacer", w=300, h=100)
    cmds.columnLayout()
    
    cmds.button( label='Set Character Root', command=fetchRoot )
    cmds.textField('tRoot', w=300)
    cmds.separator( height=10, style='double')
    
    cmds.button( label='Set Keyed Character Ctrl', command=fetchCtrl )
    cmds.textField('tCtrl', w=300)
    cmds.separator( height=10, style='double')
    
    cmds.button( label='Set Shot Camera', command=fetchCam )
    cmds.textField('tCam', w=300)
    cmds.separator( height=10, style='double')
       
    cmds.button( label='Run Screen Spacer', command=screenSpacer )
    
    cmds.text( label='____________________________________________________________')
    cmds.separator( h=10, style="none")   
    cmds.text( label='Created by <a href="https://linktr.ee/prattbros?q=HTML+link">ThePrattBros</a>', hyperlink=True)
    cmds.separator( h=10, style="none")    

    cmds.showWindow( window )

screenSpacerUI()
print ('Screen Spacer imported')