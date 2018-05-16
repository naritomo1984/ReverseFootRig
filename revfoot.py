# -----------------------------------------------------------------------------------------------------------------------------------------------------
#
# Revfoot.py
# v1.0
#
# create the reverse foot rig. Joints position is going to be based on each locator's (position)
#
# Tomonari Michigami
# >>tmnr.net
# >>naritomo@me.com
#
# Copyright Tomonari Michigami, 2015
# All rights reserved.
#
# -----------------------------------------------------------------------------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------------------------------------------------------------------------
#
# This program is free software. You can redistribute it and/or modify it under the terms the GNU(General Public License)
# as published by the Free Software Foundation. PLEASE USE THIS PROGRAM AT YOUR OWN RISK!!
#
#
# I hope this program will be useful for your projects.
# And if you use this for commercial projects by any chance, Please let me know. I would appriciate it.
# Thank you!
#
# -----------------------------------------------------------------------------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------------------------------------------------------------------------





import pymel.core as pm

jntnamelist = []
revjntnamelist = []
sfx = "_L"
sfx_r = "_R"

## Function for getting joint's name and making locators
def makeLocators():
    jointnamelist = []
    jointnamelist.append(pm.textField(thigh, q=True, tx=True))
    jointnamelist.append(pm.textField(leg, q=True, tx=True))
    jointnamelist.append(pm.textField(ancle, q=True, tx=True))
    jointnamelist.append(pm.textField(foot, q=True, tx=True))
    jointnamelist.append(pm.textField(toe, q=True, tx=True))
    jointnamelist.append(pm.textField(heel, q=True, tx=True))
    for jnt in jointnamelist:
        pm.spaceLocator(n=jnt)
    return jointnamelist

## Function for Applying IK solver to joints
def applyIK(sfx):
    sfx = sfx
    ikhandlelist = []
    ikhandlelist.append(pm.ikHandle(n="ikHandle_"+ jntnamelist[2] + sfx, sj=jntnamelist[0]+ sfx, ee = jntnamelist[2]+ sfx, sol = "ikRPsolver")[0])
    ikhandlelist.append(pm.ikHandle(n="ikHandle_"+ jntnamelist[3] + sfx, sj=jntnamelist[2]+ sfx, ee = jntnamelist[3]+ sfx, sol = "ikSCsolver")[0])
    ikhandlelist.append(pm.ikHandle(n="ikHandle_"+ jntnamelist[4] + sfx, sj=jntnamelist[3]+ sfx, ee = jntnamelist[4]+ sfx, sol = "ikSCsolver")[0])
    
    pm.parent("ikHandle_"+ jntnamelist[2] + sfx, "Rev_"+jntnamelist[2]+sfx)
    pm.parent("ikHandle_"+ jntnamelist[3] + sfx, "Rev_"+jntnamelist[3]+sfx)
    pm.parent("ikHandle_"+ jntnamelist[4] + sfx, "Rev_"+jntnamelist[5]+sfx)
    
## Function for mirroring joints
def mirrorJnt(revjntnamelist, sfx, sfx_r):
    sfx = "_L"
    jntnamelistL = []
    revjntnamelistL = []
    for jnt in jntnamelist[0:-1]:
        newname = pm.rename(jnt, str(jnt)+sfx)
        jntnamelistL.append(newname)
    for jnt in revjntnamelist:
        newname = pm.rename(jnt, str(jnt)+sfx)
        revjntnamelistL.append(newname)
        
    pm.mirrorJoint(pm.ls(revjntnamelistL[0]), mirrorBehavior = True, searchReplace = (sfx, sfx_r))
    pm.mirrorJoint(pm.ls(jntnamelistL[0]), mirrorBehavior = True, searchReplace = (sfx, sfx_r))

    

## Function for making reverse foot function
def makeReversefoot(jntnamelist, sfx, sfx_r, mirror):
    locatorslist = {}
    i = 0
    jntnamelist = jntnamelist
    revjntnamelist = []

    for jnt in jntnamelist:
        locator = pm.ls(jnt)[0]
        pos = locator.getTranslation()
        if jnt not in locatorslist:
            locatorslist[str(0+i)+jnt] = pos
        pm.delete(jnt)
        i +=1
        
    ##Make joints at each locators position 
    for k in sorted(locatorslist.items())[0:-1]:
        pm.joint(n = str(k[0]), p = locatorslist[k[0]])
        
    ##Make Heel joint
    heel = pm.joint(n = jntnamelist[5]+"1", p = locatorslist["5"+jntnamelist[5]])
    pm.parent(heel, w = True)
    
    ##Make Reverse joints chain
    obj = pm.ls(jntnamelist[2], type="joint")
    newandle = pm.duplicate(obj, rc=True)
    pm.parent(newandle, w=True)
    toe = pm.reroot(jntnamelist[4]+"1")
    pm.parent(jntnamelist[4]+"1", jntnamelist[5]+"1")
    rev = pm.ls(jntnamelist[5]+"1", dag = True)
    
    ##Rename reverse joints
    for jnt in rev:
        revjnt = pm.rename(jnt, "Rev_"+str(jnt[0:-1]))
        revjntnamelist.append(revjnt)
    
    
    ##Look wheather the checkbox is on or off
    mirrorEnable = pm.checkBox(mirror, query=True, v=True)
           
    ##Make Iksolver(if mirror is on, mirror joint chain)
    if mirrorEnable == True:
        mirrorJnt(revjntnamelist, sfx, sfx_r)
        applyIK(sfx)
        applyIK(sfx_r)
    else:
        sfx = ""
        applyIK(sfx)
        
##Create UI
Window = pm.window(title="RevFoot_Tool_Ver1.0", iconName = "Short Name", widthHeight = (300, 400))
pm.rowColumnLayout(numberOfColumns = 1, columnAttach = (1, 'both', 0), columnWidth = (300,300))
pm.text(label = "Joint name for Thigh")
thigh = pm.textField(tx = "Thigh")
pm.text(label = "Joint name for Leg")
leg = pm.textField(tx = "Leg")
pm.text(label = "Joint name for Ancle")
ancle = pm.textField(tx = "Ancle")
pm.text(label = "Joint name for Heel")
heel = pm.textField(tx = "Heel")
pm.text(label = "Joint name for Foot")
foot = pm.textField(tx = "Foot")
pm.text(label = "Joint name for Toe")
toe = pm.textField(tx = "Toe")


pm.button(label = "Make locators", command = "jntnamelist = makeLocators()", w = 300, h = 50)
pm.button(label = "Make reverse foot", command = "makeReversefoot(jntnamelist,sfx,sfx_r, mirror)",w = 300, h = 50)
pm.button(label = "Close window", command = "pm.deleteUI(Window, window=True)",w = 300, h = 50)
mirror = pm.checkBox(label = "Enable Mirroring(_R)")
pm.setParent('..')
pm.showWindow(Window)