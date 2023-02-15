from MagicBook import *
import pymel.core as pm
USERAPPDIR = pm.internalVar(userAppDir=True)
message=''
def main():
    try:
        pm.deleteUI('MagicBook')
    except:
        pass
    USERAPPDIR = pm.internalVar(userAppDir=True)
    pluginPath=USERAPPDIR+'plug-ins/MagicBook'
    windowWidth=240
    windowHeight=405
    MBGUIwindow=pm.window('MagicBook',width=windowWidth,height=windowHeight,sizeable=0)
    iconLayout=pm.columnLayout('icon',p=MBGUIwindow,columnWidth=windowWidth)
    pm.rowLayout(numberOfColumns=2,columnWidth=[(1,100),(2,120)],columnAlign=[(1,'right'),(2,'center')],
                 columnAttach=[(1,'left',20),(2,'both',10)])
    pm.image( image=pluginPath+'/yuumi.png')

    pm.setParent('..')
    tabLayout=pm.tabLayout('tabs',p=MBGUIwindow,width=windowWidth,innerMarginHeight=0)
    pm.setParent('..')
    pm.rowLayout(height=30,width=windowWidth,numberOfColumns=1,
                 rowAttach =(1,'both',5))
    pm.text('messageBox',l='Message Box',backgroundColor=(0.7,0.7,0.9),
            width=windowWidth,height=24)
def genTab():
    Gen = pm.columnLayout('Gen', p='tabs', rowSpacing=10,columnAttach =('left',55))
    # GenPart1
    pm.text('Rig Hierarchy:',height=30,annotation='')
    pm.rowLayout( numberOfColumns=1, columnWidth=(1, 120), columnAlign=(1, 'center'),
                            columnAttach=(1, 'both', 30))
    pm.button(label='Create Rig',c='createRigHierarchy()')
    pm.setParent('..')
    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 120), columnAlign=(1, 'center'),
                 columnAttach=(1, 'both', 30))
    pm.button(label='Delete Rig',c='deleteHierarchy()')
    pm.setParent('..')

    # GenPart2
    pm.text(label='Parameters:',height=30)
    pm.rowColumnLayout(numberOfColumns=2,
                                  columnWidth=[(1, 80), (2, 40)],
                                  columnAttach=[(1, 'right', 5), (2, 'both', 0)],
                                  columnAlign=[(1, 'right'), (2, 'center')]
                                  )
    pm.text(label='max id = ', annotation='Max:999')
    pm.textField('maxid',tx='4')
    pm.text(label='height = ')
    pm.textField('height',tx='1')
    pm.text(label='width = ')
    pm.textField('width',tx='1')
    pm.text(label='height div = ')
    pm.textField('heightdiv',tx='10')
    pm.text(label='width div = ')
    pm.textField('widthdiv',tx='1')
    pm.setParent('..')
    # GenPart3
    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 120), columnAlign=(1, 'center'),
                            columnAttach=(1, 'both', 30))
    pm.button(label='Generate',c='gennerateFromtext()')
    pm.setParent('..')

def keyTab():
    Key=pm.columnLayout('Key',p='tabs',rowSpacing=10,columnAttach =('left',55))
    pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 60)], columnAlign=[(1, 'center'), (2, 'center')],
                 columnAttach=[(1, 'both', 5), (2, 'both', 5)])
    pm.button(label='Auto0',c='auto0()')
    pm.button(label='Auto1',c='auto1()')
    pm.setParent('..')
    #KeyPart1
    pm.text(label='Set driven key:',height=30)
    pm.rowLayout(numberOfColumns=2,columnWidth=[(1,60),(2,40)],
                 columnAlign=[(1, 'left'), (2, 'left')],
                 columnAttach=[(1, 'right', 0), (2, 'both', 0)])
    pm.text(label='page id:')
    pm.textField('pageid', tx='0')
    pm.setParent('..')

    #KeyPart2
    pm.rowLayout(numberOfColumns=2,columnWidth=[(1,120),(2,30)],columnAttach=[(1,'both',10),(2,'both',0)])
    pm.button(label='setDrivenKey',c='drivenKey()')
    pm.button(label='SYM', c='drivenKeySym()')
    pm.setParent('..')
    #KeyPart3

    pm.rowLayout(numberOfColumns=2,columnWidth=[(1,60),(2,40)],
                 columnAlign=[(1, 'left'), (2, 'left')],
                 columnAttach=[(1, 'right', 0), (2, 'both', 0)])
    pm.text(label='state id:')
    pm.textField('stateid', tx='0')
    pm.setParent('..')
    pm.text(label='Save state from page:')
    #saveState
    pm.rowLayout(numberOfColumns=1,columnWidth=(1,120),columnAttach=(1,'both',10))
    pm.button(label='saveState',c='saveStateUI()')
    pm.setParent('..')
    #deleteState
    pm.rowLayout(numberOfColumns=1,columnWidth=(1,120),columnAttach=(1,'both',10))
    pm.button(label='deleteState',c='deleteStateUI()')
    pm.setParent('..')
    #copyToAll

    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 120), columnAttach=(1, 'both', 10))
    pm.button(label='copyToAll',c='copyToAll()')
    pm.setParent('..')
    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 120), columnAttach=(1, 'both', 10))
    pm.button(label='deleteKeys', c='deleteKeysUI()')
    pm.setParent('..')


def blendTab():
    Blend = pm.columnLayout('Blend', p='tabs', rowSpacing=10,columnAttach =('left',55))
    pm.text(label='Blend states:',height=30)
    pm.rowLayout(numberOfColumns=2,columnWidth=[(1,60),(2,40)],
                 columnAlign=[(1, 'right'), (2, 'center')],
                 columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    pm.text(label='max state:')
    pm.textField('maxstate')
    pm.setParent('..')
    pm.rowLayout(numberOfColumns=1,columnWidth=(1,120),columnAttach=(1,'both',20))
    pm.button(label='blendState',c='blendState()')
    pm.setParent('..')
    pm.text(align='left',
            label='Warning: \nyou CANNOT edit in \nKey tab if you have \nblended states. \nif you want, please \ndelete blend state',
            width=120)
    pm.text(label='Delete blend states:', height=30)

    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 120), columnAttach=(1, 'both', 0))
    pm.button(label='deleteBlendState', c='delBlendStateUI()')
    pm.setParent('..')

def linkTab():

    link=pm.columnLayout('Link',p='tabs',rowSpacing=10,columnAttach =('left',55))
    pm.text('MagicLink!',height=30)
    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 120), columnAttach=(1, 'both', 0))
    pm.button(label='Enable',c='enableMagicLink()')
    pm.setParent('..')
    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 120), columnAttach=(1, 'both', 0))
    pm.button(label='Disable',c='disableMagicLink()')
    pm.setParent('..')

def IOTab():
    exp = pm.columnLayout('I/O', p='tabs', rowSpacing=10, columnAttach=('left', 0))
    pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 40)],
                 columnAlign=[(1, 'right'), (2, 'center')],
                 columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    pm.text(label='state id:')
    pm.textField('stateidIO')
    pm.setParent('..')
    pm.rowLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 120)],
                 columnAlign=[(1, 'right'), (2, 'center')],
                 columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    pm.text(label='name:')
    pm.textField('nameIO')
    pm.setParent('..')
    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 220), columnAttach=(1, 'both', 55))
    pm.button(label='Export',c='exportUI()')
    pm.setParent('..')
    pm.rowLayout(numberOfColumns=1, columnWidth=(1, 220), columnAttach=(1, 'both', 55))
    pm.button(label='Import',c='importUI()')
    pm.setParent('..')

def MBGUI():

    main()
    genTab()
    keyTab()
    blendTab()
    linkTab()
    IOTab()
    pm.showWindow()

#Func
def gennerateFromtext():
    pm.text('messageBox', edit=1, l='Please wait for a moment')
    maxid=int(pm.textField('maxid',text=1,q=1))
    height = float(pm.textField('height', text=1, q=1))
    width = float(pm.textField('width', text=1, q=1))
    heightdiv = int(pm.textField('heightdiv', text=1, q=1))
    widthdiv = int(pm.textField('widthdiv', text=1, q=1))
    pageGenRange(maxid,height,width,heightdiv,widthdiv)
    pm.text('messageBox', edit=1, l='Generate succeed'+';'+str(maxid)+';'+str(height)+';'+str(width)+';'+str(heightdiv)+';'+str(widthdiv))
def drivenKey():
    pageid=int(pm.textField('pageid',text=1,q=1))
    setDrivenKey(pageid)
    attrName=nameFromId(pageid)+'ctrlPoints.flip'
    attr=pm.getAttr(attrName)
    attrFormat='{:.3f}'.format(attr)
    pm.text('messageBox', edit=1, l=attrName+':'+attrFormat)
def drivenKeySym():
    pageid=int(pm.textField('pageid',text=1,q=1))
    setDrivenKeySym(pageid)
    attrName=nameFromId(pageid)+'ctrlPoints.flip'
    attr=pm.getAttr(attrName)
    attrFormat='{:.3f}'.format(attr)
    pm.text('messageBox', edit=1, l=attrName+':'+attrFormat)
def saveStateUI():
    pageid = int(pm.textField('pageid', text=1, q=1))
    stateid = int(pm.textField('stateid', text=1, q=1))
    saveState(sourceId=pageid, stateId=stateid)
    pm.text('messageBox', edit=1, l='Saved state'+str(stateid))
def deleteStateUI():
    stateid = int(pm.textField('stateid', text=1, q=1))
    delState(stateid)
    pm.text('messageBox', edit=1, l='Deleted state' + str(stateid))
def copyToAll():
    maxid = int(pm.textField('maxid', text=1, q=1))
    stateid = int(pm.textField('stateid', text=1, q=1))
    rebuildKeyRange(maxid=maxid,stateId=stateid)
    pm.text('messageBox', edit=1, l='Copied state' + str(stateid)+' to all')
def deleteKeysUI():
    maxid = int(pm.textField('maxid', text=1, q=1))
    delKeyRange(maxid)
    pm.text('messageBox', edit=1, l='Deleted all key attach on ctrlPoints')
def auto0():
    maxid = int(pm.textField('maxid', text=1, q=1))
    setDrivenKeyAuto0(targetId=0)
    saveState(sourceId=0, stateId=0)
    rebuildKeyRange(maxid=maxid, stateId=0)
    pm.text('messageBox', edit=1, l='Auto0')
def auto1():
    maxid = int(pm.textField('maxid', text=1, q=1))
    setDrivenKeyAuto1(targetId=0)
    saveState(sourceId=0, stateId=1)
    rebuildKeyRange(maxid=maxid, stateId=1)
    pm.text('messageBox', edit=1, l='Auto1')
def blendState():
    maxid = int(pm.textField('maxid', text=1, q=1))
    maxstate = int(pm.textField('maxstate', text=1, q=1))
    blendStatesRange(maxstate,maxid)
    pm.text('messageBox', edit=1, l='Blendstates succeed')
def delBlendStateUI():
    maxid = int(pm.textField('maxid', text=1, q=1))
    delBlendStateRange(maxid=maxid)
    pm.text('messageBox', edit=1, l='Delete blendstates succeed')
def enableMagicLink():
    maxid = int(pm.textField('maxid', text=1, q=1))
    linkRemapNodeRange(maxid=maxid)
    pm.text('messageBox', edit=1, l='Magic link enabled')
def disableMagicLink():
    maxid = int(pm.textField('maxid', text=1, q=1))
    delRemapNodeRange(maxid=maxid)
    pm.text('messageBox', edit=1, l='Magic link disabled')
def exportUI():
    stateidIO=int(pm.textField('stateidIO',text=1,q=1))
    nameIO=pm.textField('nameIO',text=1,q=1)
    if nameIO=='':
        nameIO='state'+str(stateidIO)
    exportState(stateidIO, nameIO)
    pm.text('messageBox', edit=1, l='exported:state' + str(stateidIO) + ' , name:' + nameIO)

def importUI():
    stateidIO=int(pm.textField('stateidIO',text=1,q=1))
    nameIO=pm.textField('nameIO',text=1,q=1)
    if nameIO=='':
        nameIO='state'+str(stateidIO)
    importState(stateidIO, nameIO)
    pm.text('messageBox',edit=1,l='imported:state'+str(stateidIO)+' , name:'+nameIO)