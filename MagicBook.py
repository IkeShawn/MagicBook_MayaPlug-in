### Plugin name: MagicBook
### Version: 1.0
### Author: 御宅松鼠(Ike Shawn)
### Date: 2023/1/29
### My Email: 2694836731@qq.com
### 你可以在任何项目中使用这个脚本，但是不允许用于出售。
### You can use this script in any project, but not for sale.
###
import pymel.core as pm
#set default value->
USERAPPDIR = pm.internalVar(userAppDir=True)
attributeList = ['rotateByAxis1', 'rotateByAxis2', 'rotateByAxis3', 'length1', 'length2', 'length3', 'gap1', 'gap2', 'gap3']
maxid=5
pageHeight = 1
pageWidth = 2
pageSH = 15
pageSW = 1
gapDefault=1.0
rootOffset=1
#utility func
def nameFromId(id):
    if id<=0:
        name='PN'+str(-id).zfill(3)
    else:
        name='PP'+str(id).zfill(3)
    return name
def idFromName(name):
    if name[1] =='M':
        id=-int(name[2:])
    else:
        id=int(name[2:])
    return id
def listExistingStates(stateCount):
    #read existing states in MainBook
    existingStates = []
    nodeName='MainBook'
    for i in range(stateCount + 1):
        attrName='state'+str(i)
        if(pm.attributeQuery(attrName,node=nodeName,exists=1)):
            existingStates.append(i)
    return existingStates
def getWeight(stateid,statemax):
    existingStates=listExistingStates(statemax)
    statement=''
    for i in range(len(existingStates)):
        statement+='MainBook.state'+str(existingStates[i])+'+'
    statement='('+'MainBook.state'+str(stateid)+'/'+'('+statement[:-1]+'))'
    return statement
#1
def createRigHierarchy(pageHeight=1,pageWidth=1):
    try:
        pm.delete('BookRigGroup')
    except:
        pass
    # create rig hierarchy
    pm.select(cl=1)
    pm.createNode('transform', name='BookRigGroup')
    pm.circle(nr=(0, 1, 0), c=(0, 0, 0), name='MainBook', radius=max(pageWidth, pageHeight)*0.7)
    pm.parent('MainBook', 'BookRigGroup')
    pm.createNode('transform', name='DeformationSystem')
    pm.createNode('transform', name='AllCtrlGrp')
    pm.createNode('transform', name='Geo')
    pm.createNode('transform', name='DeformCurve')
    pm.createNode('transform', name='IKHandleGrp')
    pm.createNode('transform', name='JointGrp')
    pm.addAttr('MainBook', longName='open', shortName='open', attributeType='double', keyable=1, min=0, max=1,
               defaultValue=1)
    pm.addAttr('MainBook',longName='atPage',shortName='ap',attributeType='double',keyable=1,defaultValue=0)
    pm.addAttr('MainBook', longName='perPos', shortName='perPos', attributeType='double', keyable=1,min=0,max=1,defaultValue=0)
    pm.addAttr('MainBook', longName='perVal', shortName='perVal', attributeType='double', keyable=1,min=0,max=1,defaultValue=0)
    pm.addAttr('MainBook', longName='sufPos', shortName='sufPos', attributeType='double', keyable=1,min=0,max=1,defaultValue=0)
    pm.addAttr('MainBook', longName='sufVal', shortName='sufVal', attributeType='double', keyable=1,min=0,max=1,defaultValue=0)

    pm.setAttr('IKHandleGrp.visibility', 0)
    pm.setAttr('JointGrp.visibility', 0)
    pm.parent('Geo', 'BookRigGroup')
    pm.parent('AllCtrlGrp', 'MainBook')
    pm.parent('DeformationSystem', 'MainBook')
    pm.parent('DeformCurve', 'DeformationSystem')
    pm.parent('IKHandleGrp', 'DeformationSystem')
    pm.parent('JointGrp', 'DeformationSystem')
    pm.select(cl=1)
def deleteHierarchy():
    try:
        pm.delete('BookRigGroup')
    except:
        pass
#2
def pageGen(id,pageHeight, pageWidth, pageSH, pageSW, gap=1.0, rof=1):
    pagename=nameFromId(id)
    pm.select(cl=1)
    # generate a plane
    pm.polyPlane(name=pagename, subdivisionsHeight=pageSH, height=pageHeight, width=pageWidth, subdivisionsWidth=pageSW,
                 axis=(1, 0, 0), constructionHistory=0)
    pm.move(pagename, [0, pageHeight / 2, 0])
    pm.setAttr(pagename + ".rotatePivotY", -pageHeight / 2)
    pm.setAttr(pagename + ".scalePivotY", -pageHeight / 2)
    pageUV=pagename+'.f[0:]'
    pm.polyEditUV(pageUV, pivotU=0.5, pivotV=0.5, a=90)
    # generate a joint chain
    pm.select(clear=1)
    for i in range(pageSH + 1):
        # pm.select(clear=1)
        nameTemp = pagename + "pageJoint"
        number = str(i).zfill(2)
        nameJoint = nameTemp + number
        pm.joint(n=nameJoint, position=(0, (i / pageSH) * pageHeight, 0), radius=0.3)
        pm.setAttr(nameJoint + '.preferredAngleZ', 10)
    # create a Bezier curve
    pm.curve(name=pagename + 'ctrlCurve',
             point=[(0, 0, 0), (0, 0.3 * pageHeight, 0), (0, 0.7 * pageHeight, 0), (0, pageHeight, 0)], bezier=1)
    pm.setAttr(pagename + 'ctrlCurve.rotateY', 90)
    pm.makeIdentity(pagename + 'ctrlCurve', apply=True)
    # create an ik spline handle
    startJoint = pagename + 'pageJoint00'
    endJoint = pagename + 'pageJoint' + str(pageSH).zfill(2)
    pm.ikHandle(name=pagename + 'pageIK', startJoint=startJoint, endEffector=endJoint, createCurve=False,
                curve=pagename + 'ctrlCurve', solver='ikSplineSolver')
    # create 4 transform and connect them to the curve
    pm.select(cl=1)
    pm.createNode('transform', name=pagename + 'ctrlPoints')
    pm.addAttr(pagename + 'ctrlPoints', longName='id', attributeType='short', keyable=1)
    pm.addAttr(pagename + 'ctrlPoints', longName='flip', shortName='flip', attributeType='double', keyable=1, max=1,
               min=-1,
               defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='rotateByAxis1', shortName='rba1', attributeType='double', keyable=1,
               maxValue=1, minValue=-1, defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='rotateByAxis2', shortName='rba2', attributeType='double', keyable=1,
               maxValue=1, minValue=-1, defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='rotateByAxis3', shortName='rba3', attributeType='double', keyable=1,
               maxValue=1, minValue=-1, defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='length1', shortName='len1', attributeType='double', keyable=1,
               defaultValue=1)
    pm.addAttr(pagename + 'ctrlPoints', longName='length2', shortName='len2', attributeType='double', keyable=1,
               defaultValue=1)
    pm.addAttr(pagename + 'ctrlPoints', longName='length3', shortName='len3', attributeType='double', keyable=1,
               defaultValue=1)
    pm.addAttr(pagename + 'ctrlPoints', longName='gap1', shortName='gap1', attributeType='double', keyable=1, min=0,
               defaultValue=gap)
    pm.addAttr(pagename + 'ctrlPoints', longName='gap2', shortName='gap2', attributeType='double', keyable=1, min=0,
               defaultValue=gap)
    pm.addAttr(pagename + 'ctrlPoints', longName='gap3', shortName='gap3', attributeType='double', keyable=1, min=0,
               defaultValue=gap)
    pm.addAttr(pagename + 'ctrlPoints', longName='rootOffset', shortName='ros', attributeType='double', keyable=1,min=0,
               defaultValue=rof)
    pm.addAttr(pagename + 'ctrlPoints', longName='remap', shortName='rm', attributeType='double', keyable=1,
               min=0,max=1,
               defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='remapWeight', shortName='rw', attributeType='double', keyable=1,
               min=0, max=1,
               defaultValue=1)
    pm.addAttr(pagename + 'ctrlPoints', longName='postAdj', shortName='pa', attributeType='double', keyable=1,
               min=-1, max=1,
               defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='open', shortName='open', attributeType='double', keyable=1,
               min=0, max=1,
               defaultValue=1)

    pm.addAttr(pagename + 'ctrlPoints', longName='x0', shortName='x0', attributeType='double', keyable=1,
               defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='y0', shortName='y0', attributeType='double', keyable=1,
               defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='x1', shortName='x1', attributeType='double', keyable=1,
               defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='y1', shortName='y1', attributeType='double', keyable=1,
               defaultValue=0.3 * pageHeight)
    pm.addAttr(pagename + 'ctrlPoints', longName='x2', shortName='x2', attributeType='double', keyable=1,
               defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='y2', shortName='y2', attributeType='double', keyable=1,
               defaultValue=0.7 * pageHeight)
    pm.addAttr(pagename + 'ctrlPoints', longName='x3', shortName='x3', attributeType='double', keyable=1,
               defaultValue=0)
    pm.addAttr(pagename + 'ctrlPoints', longName='y3', shortName='y3', attributeType='double', keyable=1,
               defaultValue=pageHeight)
    pm.setAttr(pagename + 'ctrlPoints' + '.id', id, keyable=1, lock=1)

    pm.setAttr(pagename + 'ctrlPoints' + '.tx', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.ty', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.tz', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.rx', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.ry', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.rz', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.sx', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.sy', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.sz', keyable=0)
    pm.setAttr(pagename + 'ctrlPoints' + '.visibility', keyable=0)
    #getColor
    if id<0:
        pm.setAttr(pagename+'.useOutlinerColor', 1)
        pm.setAttr(pagename+'.outlinerColorR', 0.47)
        pm.setAttr(pagename+'.outlinerColorG', 0.73)
        pm.setAttr(pagename+'.outlinerColorB', 1.000)
        pm.setAttr(pagename + 'ctrlCurve'+ '.useOutlinerColor', 1)
        pm.setAttr(pagename + 'ctrlCurve'+ '.outlinerColorR', 0.47)
        pm.setAttr(pagename + 'ctrlCurve'+ '.outlinerColorG', 0.73)
        pm.setAttr(pagename + 'ctrlCurve'+ '.outlinerColorB', 1.000)
        pm.setAttr(pagename + 'ctrlPoints' + '.useOutlinerColor', 1)
        pm.setAttr(pagename + 'ctrlPoints' + '.outlinerColorR', 0.47)
        pm.setAttr(pagename + 'ctrlPoints' + '.outlinerColorG', 0.73)
        pm.setAttr(pagename + 'ctrlPoints' + '.outlinerColorB', 1.000)
    if id>0:
        pm.setAttr(pagename + '.useOutlinerColor', 1)
        pm.setAttr(pagename + '.outlinerColorR', 1)
        pm.setAttr(pagename + '.outlinerColorG', 0.53)
        pm.setAttr(pagename + '.outlinerColorB', 0.93)
        pm.setAttr(pagename + 'ctrlCurve' + '.useOutlinerColor', 1)
        pm.setAttr(pagename + 'ctrlCurve' + '.outlinerColorR', 1)
        pm.setAttr(pagename + 'ctrlCurve' + '.outlinerColorG', 0.53)
        pm.setAttr(pagename + 'ctrlCurve' + '.outlinerColorB', 0.93)
        pm.setAttr(pagename + 'ctrlPoints' + '.useOutlinerColor', 1)
        pm.setAttr(pagename + 'ctrlPoints' + '.outlinerColorR', 1)
        pm.setAttr(pagename + 'ctrlPoints' + '.outlinerColorG', 0.53)
        pm.setAttr(pagename + 'ctrlPoints' + '.outlinerColorB', 0.93)

    pm.connectAttr(pagename + 'ctrlPoints.x0', pagename + 'ctrlCurveShape.controlPoints[0].xValue')
    pm.connectAttr(pagename + 'ctrlPoints.y0', pagename + 'ctrlCurveShape.controlPoints[0].yValue')
    pm.connectAttr(pagename + 'ctrlPoints.x1', pagename + 'ctrlCurveShape.controlPoints[1].xValue')
    pm.connectAttr(pagename + 'ctrlPoints.y1', pagename + 'ctrlCurveShape.controlPoints[1].yValue')
    pm.connectAttr(pagename + 'ctrlPoints.x2', pagename + 'ctrlCurveShape.controlPoints[2].xValue')
    pm.connectAttr(pagename + 'ctrlPoints.y2', pagename + 'ctrlCurveShape.controlPoints[2].yValue')
    pm.connectAttr(pagename + 'ctrlPoints.x3', pagename + 'ctrlCurveShape.controlPoints[3].xValue')
    pm.connectAttr(pagename + 'ctrlPoints.y3', pagename + 'ctrlCurveShape.controlPoints[3].yValue')
    # bind skin
    pm.skinCluster(pagename, pagename + 'pageJoint00', name=pagename + 'pageSkinCluster')
    # paint weight
    for i in range((pageSH + 1) * (pageSW + 1)):
        row = int(i / (pageSW + 1))
        for j in range(pageSH + 1):
            attribute = pagename + 'pageSkinCluster.weightList[{}].weights[{}]'.format(str(i), str(j))
            if row == j:
                pm.setAttr(attribute, 1)
            else:
                pm.setAttr(attribute, 0)
    # parent to rig system
    pm.parent(pagename + 'pageJoint00', 'JointGrp')
    pm.parent(pagename, 'Geo')
    pm.parent(pagename + 'ctrlPoints', 'AllCtrlGrp')
    pm.parent(pagename + 'pageIK', 'IKHandleGrp')
    pm.parent(pagename + 'ctrlCurve', 'DeformCurve')
    pm.select(cl=1)
    # create expression
    expression = '''
    //rootOffset
{pagename}ctrlCurve.tx={pagename}ctrlPoints.ros*0.01*{pagename}ctrlPoints.id;

{pagename}ctrlPoints.x1 = 0.3*{pageHeight}*{pagename}ctrlPoints.len1 * sin({pagename}ctrlPoints.rba1 *0.5 * 3.1415926 * (1+sign({pagename}ctrlPoints.rba1) *{pagename}ctrlPoints.id * {pagename}ctrlPoints.gap1*0.01));
{pagename}ctrlPoints.y1 = 0.3*{pageHeight}*{pagename}ctrlPoints.len1 * cos({pagename}ctrlPoints.rba1 *0.5 * 3.1415926 * (1+sign({pagename}ctrlPoints.rba1) *{pagename}ctrlPoints.id * {pagename}ctrlPoints.gap1*0.01));

{pagename}ctrlPoints.x2 = 0.7*{pageHeight}*{pagename}ctrlPoints.len2 * sin({pagename}ctrlPoints.rba2 *0.5 * 3.1415926 * (1+sign({pagename}ctrlPoints.rba2) *{pagename}ctrlPoints.id * {pagename}ctrlPoints.gap2*0.01));
{pagename}ctrlPoints.y2 = 0.7*{pageHeight}*{pagename}ctrlPoints.len2 * cos({pagename}ctrlPoints.rba2 *0.5 * 3.1415926 * (1+sign({pagename}ctrlPoints.rba2) *{pagename}ctrlPoints.id * {pagename}ctrlPoints.gap2*0.01));

{pagename}ctrlPoints.x3 = 1*{pageHeight}*{pagename}ctrlPoints.len3 * sin({pagename}ctrlPoints.rba3 *0.5 * 3.1415926 * (1+sign({pagename}ctrlPoints.rba3) *{pagename}ctrlPoints.id * {pagename}ctrlPoints.gap3*0.01));
{pagename}ctrlPoints.y3 = 1*{pageHeight}*{pagename}ctrlPoints.len3 * cos({pagename}ctrlPoints.rba3 *0.5 * 3.1415926 * (1+sign({pagename}ctrlPoints.rba3) *{pagename}ctrlPoints.id * {pagename}ctrlPoints.gap3*0.01));
    '''.format(pagename=pagename, pageHeight=str(pageHeight))
    pm.expression(s=expression, name=pagename + 'Ctrl')
def pageGenRange(maxid=1, pageHeight=1, pageWidth=1, pageSH=10, pageSW=1, gap=1.0, rof=1):
    for i in range(-maxid, maxid+1):
        pageGen(id=i, pageHeight=pageHeight, pageWidth=pageWidth, pageSH=pageSH, pageSW=pageSW,gap=gap, rof=rof)
    pm.reorder('PN000ctrlPoints',relative=-maxid)
    maxname=nameFromId(maxid)
    pm.reorder(maxname+'ctrlPoints',relative=-maxid*2+2)
#3
def setDrivenKey(targetId=0):
    #if you have a blendState, this func will kill blendstate
    targetname=nameFromId(targetId)
    groupname = 'ctrlPoints'
    driver=targetname+groupname+'.flip'

    for i in range(len(attributeList)):
        attributeName=targetname+groupname+'.'+attributeList[i]
        list=pm.listConnections(attributeName, type='animCurveUU', source=1, destination=0)
        if len(list)==0:
            try:
                pass
#                pm.disconnectAttr(attributeName,)
            except:
                pass
        pm.setDrivenKeyframe(attributeName, currentDriver=driver)
def setDrivenKeySym(targetId=0):
    #if you have a blendState, this func will kill blendstate
    targetname=nameFromId(targetId)
    groupname = 'ctrlPoints'
    driver=targetname+groupname+'.flip'
    driverValue = pm.getAttr(driver)
    symDriverValue=-1*driverValue
    for i in range(len(attributeList)):
        attributeName = targetname + groupname + '.' + attributeList[i]
        drivenValue=pm.getAttr(attributeName)
        if i==0 or i==1 or i==2:
            symDrivenValue=-1*drivenValue
        else:
            symDrivenValue=drivenValue
        pm.setDrivenKeyframe(attributeName, currentDriver=driver)
        pm.setDrivenKeyframe(attributeName, currentDriver=driver,driverValue=symDriverValue,value=symDrivenValue)
def setDrivenKeyAuto0(targetId=0):
    targetname=nameFromId(targetId)
    groupname = 'ctrlPoints'
    attributeList = ['rotateByAxis1', 'rotateByAxis2', 'rotateByAxis3', 'length1', 'length2', 'length3', 'gap1', 'gap2',
                     'gap3']
    driver=targetname+groupname+'.flip'
    driven=[]
    for i in range(len(attributeList)):
        driven.append(targetname+groupname+'.'+attributeList[i])
    pm.setDrivenKeyframe(driven[0], currentDriver=driver, v=0.3, driverValue=0)
    pm.setDrivenKeyframe(driven[1], currentDriver=driver, v=-0.2, driverValue=0)
    pm.setDrivenKeyframe(driven[2], currentDriver=driver, v=0, driverValue=0)
    pm.setDrivenKeyframe(driven[3], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[4], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[5], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[6], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[7], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[8], currentDriver=driver, v=1, driverValue=0)

    pm.setDrivenKeyframe(driven[0], currentDriver=driver, v=-0.2, driverValue=-1)
    pm.setDrivenKeyframe(driven[1], currentDriver=driver, v=-0.9, driverValue=-1)
    pm.setDrivenKeyframe(driven[2], currentDriver=driver, v=-0.9, driverValue=-1)
    pm.setDrivenKeyframe(driven[3], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[4], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[5], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[6], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[7], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[8], currentDriver=driver, v=1, driverValue=-1)

    pm.setDrivenKeyframe(driven[0], currentDriver=driver, v=0.2, driverValue=1)
    pm.setDrivenKeyframe(driven[1], currentDriver=driver, v=0.9, driverValue=1)
    pm.setDrivenKeyframe(driven[2], currentDriver=driver, v=0.9, driverValue=1)
    pm.setDrivenKeyframe(driven[3], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[4], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[5], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[6], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[7], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[8], currentDriver=driver, v=1, driverValue=1)
def setDrivenKeyAuto1(targetId=0):
    targetname=nameFromId(targetId)
    groupname = 'ctrlPoints'
    attributeList = ['rotateByAxis1', 'rotateByAxis2', 'rotateByAxis3', 'length1', 'length2', 'length3', 'gap1', 'gap2',
                     'gap3']
    driver=targetname+groupname+'.flip'
    driven=[]
    for i in range(len(attributeList)):
        driven.append(targetname+groupname+'.'+attributeList[i])
    pm.setDrivenKeyframe(driven[0], currentDriver=driver, v=-0.3, driverValue=0)
    pm.setDrivenKeyframe(driven[1], currentDriver=driver, v=0.2, driverValue=0)
    pm.setDrivenKeyframe(driven[2], currentDriver=driver, v=0, driverValue=0)
    pm.setDrivenKeyframe(driven[3], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[4], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[5], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[6], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[7], currentDriver=driver, v=1, driverValue=0)
    pm.setDrivenKeyframe(driven[8], currentDriver=driver, v=1, driverValue=0)

    pm.setDrivenKeyframe(driven[0], currentDriver=driver, v=-0.2, driverValue=-1)
    pm.setDrivenKeyframe(driven[1], currentDriver=driver, v=-0.9, driverValue=-1)
    pm.setDrivenKeyframe(driven[2], currentDriver=driver, v=-0.9, driverValue=-1)
    pm.setDrivenKeyframe(driven[3], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[4], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[5], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[6], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[7], currentDriver=driver, v=1, driverValue=-1)
    pm.setDrivenKeyframe(driven[8], currentDriver=driver, v=1, driverValue=-1)

    pm.setDrivenKeyframe(driven[0], currentDriver=driver, v=0.2, driverValue=1)
    pm.setDrivenKeyframe(driven[1], currentDriver=driver, v=0.9, driverValue=1)
    pm.setDrivenKeyframe(driven[2], currentDriver=driver, v=0.9, driverValue=1)
    pm.setDrivenKeyframe(driven[3], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[4], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[5], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[6], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[7], currentDriver=driver, v=1, driverValue=1)
    pm.setDrivenKeyframe(driven[8], currentDriver=driver, v=1, driverValue=1)
#4
def saveState(sourceId=0, stateId=0):
    sourceName = nameFromId(sourceId)
    # this function will backup the drivenKeyFrame nodes as discrete nodes
    # so the 'Delete Unused Nodes' command will kill all of them
    groupname = 'ctrlPoints'
    #create an attribute on MainBook controller
    attrPlug = 'MainBook.state' + str(stateId)
    attrname = 'state'+str(stateId)
    try:
        pm.setAttr(attrPlug,1)
    except:
        pm.addAttr('MainBook',longName=attrname,shortName=attrname,attributeType='double',keyable=1,max=1,min=0,defaultValue=1)

    #this function will overwrite the existing node, so it won't cause heavy cache
    #name like: PP003ctrlPoints_gap2
    for i in range(len(attributeList)):
        sourceNodeName = sourceName + groupname + '_' + attributeList[i]
        newNodeName = attributeList[i]+'state' + str(stateId)
        try:
            pm.delete(newNodeName)
        except:
            pass
        pm.duplicate(sourceNodeName, name=newNodeName)
def delState(stateId):
    attrPlug = 'MainBook.state' + str(stateId)
    try:
        pm.deleteAttr(attrPlug)
    except:
        pass
    for i in range(len(attributeList)):
        targetNodeName = attributeList[i]+'state' + str(stateId)
        try:
            pm.delete(targetNodeName)
        except:
            pass
#5
def rebuildKey(targetId, stateId):
    #create nodes like: PP003ctrlPoints_gap2(with out state suffix)
    targetName = nameFromId(targetId)
    groupname = 'ctrlPoints'
    # this function will overwrite the existing node, so it won't produce heavy cache
    for i in range(len(attributeList)):
        sourceNodeName = attributeList[i]+'state' + str(stateId)
        newNodeName = targetName + groupname + '_' + attributeList[i]
        try:
            pm.delete(newNodeName)
        except:
            pass
        pm.duplicate(sourceNodeName, name=newNodeName)
        pm.disconnectAttr(targetName + groupname + '.' + attributeList[i],inputs=1,outputs=0)
        pm.connectAttr(newNodeName + '.output', targetName + groupname + '.' + attributeList[i])
        pm.connectAttr(targetName + groupname + '.flip', newNodeName + '.input')
def rebuildKeyRange(maxid=1,stateId=0):
    for i in range(-maxid,maxid+1):
        rebuildKey(targetId=i, stateId=stateId)
def delKeyRange(maxid):
    #this function try to delete nodes like: PP003ctrlPoints_gap2(with out state suffix), attach on all ctrlPoints
    for i in range(-maxid,maxid+1):
        pernodename=nameFromId(i)+'ctrlPoints_'
        for j in range(len(attributeList)):
            nodename=pernodename+attributeList[j]
            try:
                pm.delete(nodename)
            except:
                pass
#6
def blendStates(maxState,targetId=0):
    targetName = nameFromId(targetId)
    expressionName='StateBlend_'+targetName
    try:
        pm.delete(expressionName)
    except:
        pass
    existingStates = listExistingStates(maxState)
    groupname = 'ctrlPoints'
    statement = ''
    inputattr=''
    exp=''
    for i in range(len(attributeList)):
        try:
            pm.disconnectAttr(targetName+groupname+'.'+attributeList[i],outputs=0,inputs=1)
        except:
            pass
        #create nodes
        for stateId in range(len(existingStates)):

            sourceName = attributeList[i] + 'state' + str(stateId)
            newName=targetName+groupname+'_'+attributeList[i] + 'state' + str(stateId)
            try:
                pm.delete(newName)
            except:
                pass
            pm.duplicate(sourceName,name=newName)
            inputattr += str(newName) + '.input=' + targetName + groupname + '.flip;\n'
        statement=''
        line=''
        for stateId in range(len(existingStates)):
            newName = targetName + groupname + '_' + attributeList[i] + 'state' + str(stateId)
            statement+=getWeight(stateId,maxState)+'*'+ newName+'.output+'
        line=targetName+groupname+'.'+attributeList[i]+'='+statement[:-1]+';\n'
        exp+=line
    exp+=inputattr
    pm.expression(s=exp,name=expressionName)
def blendStatesRange(maxState,maxid):
    for id in range(-maxid,maxid+1):
        blendStates(maxState,id)
def delBlendState(targetId):
    targetName = nameFromId(targetId)
    expressionName = 'StateBlend_' + targetName
    try:
        pm.delete(expressionName)
    except:
        pass
def delBlendStateRange(maxid):
    for id in range(-maxid,maxid+1):
        delBlendState(targetId=id)
#7
def linkRemapNode(pageId=0, pageCount=1):
    pagename = nameFromId(pageId)
    nodeName = pagename + 'RemapValue'
    pm.createNode('remapValue', name=nodeName)
    pm.setAttr(nodeName + '.inputMax', pageCount)
    pm.setAttr(nodeName + '.inputMin', -pageCount)
    #attention, outputMax is -1, and outputMin is 1
    pm.setAttr(nodeName + '.outputMax', -1)
    pm.setAttr(nodeName + '.outputMin', 1)
    pm.connectAttr('MainBook.atPage', nodeName + '.inputValue')
    pm.addAttr(nodeName, longName='v2p', shortName='v2p', attributeType='double', keyable=1,
               defaultValue=(pageId + pageCount) / (2 * pageCount) - 0.01)
    pm.addAttr(nodeName, longName='v3p', shortName='v3p', attributeType='double', keyable=1,
               defaultValue=(pageId + pageCount) / (2 * pageCount) + 0.01)
    pm.addAttr(nodeName, longName='v2v', shortName='v2v', attributeType='double', keyable=1, defaultValue=0)
    pm.addAttr(nodeName, longName='v3v', shortName='v3v', attributeType='double', keyable=1, defaultValue=1)
    pm.setAttr(nodeName + '.v2p', lock=1)
    pm.setAttr(nodeName + '.v3p', lock=1)
    pm.setAttr(nodeName + '.v2v', lock=1)
    pm.setAttr(nodeName + '.v3v', lock=1)
    pm.setAttr(nodeName + '.value[2].value_Position', (pageId + pageCount) / (2 * pageCount) - 0.01)
    pm.setAttr(nodeName + '.value[3].value_Position', (pageId + pageCount) / (2 * pageCount) + 0.01)
    pm.setAttr(nodeName + '.value[2].value_FloatValue', 0)
    pm.setAttr(nodeName + '.value[3].value_FloatValue', 1)
    pm.setAttr(nodeName + '.value[2].value_Interp', 1)
    pm.setAttr(nodeName + '.value[3].value_Interp', 1)
    #this expression indicates how the remap curve should respond to the attributes on MainBook controller
    exp = '''
    {nodeName}.value[0].value_Position=0;
    {nodeName}.value[1].value_Position=1;
    {nodeName}.value[0].value_FloatValue=0;
    {nodeName}.value[1].value_FloatValue=1;
    {nodeName}.value[2].value_Position=(1-MainBook.perPos)*{v2p};
    {nodeName}.value[3].value_Position={v3p}*(1-MainBook.sufPos)+MainBook.sufPos;
    {nodeName}.value[2].value_FloatValue=MainBook.perVal;
    {nodeName}.value[3].value_FloatValue=(1-MainBook.sufVal);
    '''.format(nodeName=nodeName, v2p=pm.getAttr(nodeName + '.v2p'), v3p=pm.getAttr(nodeName + '.v3p'),
               v2v=pm.getAttr(nodeName + '.v2v'), v3v=pm.getAttr(nodeName + '.v3v'))
    expressionNodeName=pagename + 'Remap'
    targetPlug = pagename + 'ctrlPoints.flip'
    remapPlug = pagename + 'ctrlPoints.remap'
    remapWeightPlug = pagename + 'ctrlPoints.remapWeight'
    postAdjPlug = pagename + 'ctrlPoints.postAdj'
    openPlug=pagename+'ctrlPoints.open'
    exp2 = targetPlug + '=' + '('+remapPlug + '*' + remapWeightPlug + '+' + postAdjPlug+')*'+openPlug
    exp2name = pagename + 'remapWeight'
    #this function will overwrite the existing nodes
    try:
        pm.delete(expressionNodeName)

    except:
        pass
    try:
        pm.delete(exp2name)
    except:
        pass
    pm.expression(s=exp, name=expressionNodeName)
    pm.connectAttr(nodeName + '.outValue', remapPlug)
    pm.expression(s=exp2, name=exp2name)

    #refresh
    pm.setAttr('MainBook.atPage',0)



def linkRemapNodeRange(maxid=1):
    for i in range(-maxid, maxid + 1):
        linkRemapNode(pageId=i,pageCount=maxid)#
def delRemapNode(pageId):
    pagename=nameFromId(pageId)
    try:
        pm.delete(pagename+'RemapValue')
    except:
        pass
    try:
        pm.delete(pagename+'remapWeight')

    except:
        pass
def delRemapNodeRange(maxid):
    for i in range(-maxid, maxid + 1):
        delRemapNode(pageId=i)

def exportState(stateid,name):
    if name=='':
        name='state'+str(stateid)
    pm.select(cl=1)
    exportPath=USERAPPDIR+'plug-ins/MagicBook/'+name+'.ma'
    exportPathmb = USERAPPDIR + 'plug-ins/MagicBook/' + name + '.mb'
    for i in range(len(attributeList)):
        nodeName=attributeList[i]+'state'+str(stateid)
        pm.select(nodeName,add=1)
    try:
        pm.exportSelected(exportPath,force=1,type='mayaAscii')
    except:
        pm.exportSelected(exportPathmb,force=1,type='mayaBinary')


def importState(stateid,name):
    if name=='':
        name='state'+str(stateid)
    for i in range(len(attributeList)):
        nodeName=attributeList[i]+'state'+str(stateid)
        try:
            pm.delete(nodeName)
        except:
            pass
    try:
        importPath = USERAPPDIR + 'plug-ins/MagicBook/' + name + '.ma'
        pm.importFile(importPath)
    except:
        importPath = USERAPPDIR + 'plug-ins/MagicBook/' + name + '.mb'
        pm.importFile(importPath)

