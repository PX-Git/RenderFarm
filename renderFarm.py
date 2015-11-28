from pymel.all import *
import random
import os
import socket


farmPreferenceLocation = "\\\\TITAN-PC\\_NetworkUtilities\\farmPreferences.py"



def renderFarmUI():
    
    '''
    defines the main Ui for the render farm
    '''

    #shotInfo = getShotInfo()    
    shotInfo= {'startFrame':1, 'endFrame':10}
    
    
    widthVar = 500
    renderFarmUI.buttonWidth = 280
    if window("RenderFarm_Window", exists = True):
        deleteUI("RenderFarm_Window")
        
    window("RenderFarm_Window", w = widthVar, h = 300, s = True)
    
    tabs = tabLayout(innerMarginWidth=100, innerMarginHeight=10 )
    child1= columnLayout()
    mainColumn = columnLayout(columnAlign = 'center', w = 500)
    separator (style = 'none' ,h= 10)
    
    rowColumnLayout(numberOfColumns = 5)    
    text(l = 'Scene Location:'  )
    renderFarmUI.sceneLocation_ui = textField(w = 325, tx =  "\\\\TITAN-PC\\_Projects")
    
    button(l = 'Browse', c = 'browseForSceneLocation()' )
    text(l ='       ' )
    renderFarmUI.shaveScene  = checkBox(label = 'Shave Scene')
    setParent(mainColumn)
    
    #os.mkdir("\\\\TITAN-PC\\_Projects\\test")
    
    
    rowColumnLayout(numberOfColumns = 3) 
    text (l = "Output Frame Location:")
    renderFarmUI.outputFramesLocation_ui = textField(w = 325,tx = "\\\\TITAN-PC\\Frames")
    

    
    
    button(l = 'Set', c = 'browseForOutputLocation()' )    
    
    setParent(mainColumn)        
    #symbolButton(c = 'getScene Location()', i = 'C:/Users/Rob/Documents/maya/2014-x64/prefs/icons/' )
    #symbolButton(c = 'renderFarm.getScene Location()', i = '' )
    
    #separator(w = 30, style = 'none')
    separator(h = 10)
    text(l = "Frames to Distribute to Farm:")
    separator(h = 5)
    rowColumnLayout(numberOfColumns = 5)
    text(l = 'StartFrame:')
    renderFarmUI.startFrame  = intField(v = shotInfo['startFrame'],w = 40)
    separator(w = 5, style = 'none')
    text(l = 'EndFrame:')
    renderFarmUI.endFrame = intField(v = shotInfo['endFrame'],w = 40)    
    setParent('..')
    
    rowColumnLayout(numberOfColumns = 2)
    text (l = "Priority: ")
    renderFarmUI.priority = intField(v = 50,min = 1, max = 100, w = 40)
    setParent('..')
    separator(h = 10)
    text(l = "-Check the ids you would like to render on")
    text(l = "-Press Refresh to update the status of all computers")
    separator(h = 10)
    

    renderFarmUI.rows = populateNetworkInfo(mainColumn)
    
    separator(h = 10)
    button(l = 'Refresh All',w =200, c = 'updateAllIpStatus()')
    button(l = "Send Job To Farm", w = 200, c ='sendToJobStack()')
    
    
    setParent(tabs)
    
    
    child2 = columnLayout() #Set File Paths
    
    rowColumnLayout(numberOfColumns = 2) 
    
    
    #load in preferences? project based preferences?
    text (l = "Log File Location:")
    renderFarmUI.logFileLocation_ui = textField(w = 325,tx = "\\\\TITAN-PC\\Frames\\Logs")

    
    
    tabLayout( tabs, edit=True, tabLabel=((child1, 'Generate Commands'), (child2, 'Set File Paths')), w = 275 ) ##Sets up and names tabs
    showWindow("RenderFarm_Window")
    

def browseForSceneLocation():  
    
    #shotInfo = getShotInfo() 

    shotInfo= {'dir':"\\\\TITAN-PC\\_Projects"}

    userPrefScene = fileDialog2(ds=1, fm = 1, dir = shotInfo['dir'] )  [0]
    slashReverse = userPrefScene.replace("/","\\")   
    textField(renderFarmUI.sceneLocation_ui, e = True, text = slashReverse    ) 

    




    
def browseForOutputLocation():  

    
    #shotInfo = getShotInfo() 

    shotInfo= {'dir':"\\\\TITAN-PC\\Frames"}

    userPrefScene = fileDialog2(ds = 1, fm = 3, dir = shotInfo['dir'] )  [0]

    textField(renderFarmUI.outputFramesLocation_ui, e = True, text = userPrefScene   )   
   
def populateNetworkInfo(uiParent):
    
    '''
    creates rows of info and interactive options based on each computer in a list of ip Adresses
    Requires the uiParent that it should be placed under - #renderFarmUI.mainColumn 
    '''
    ipList = ["10.0.0.15",
                    "10.0.0.17",
                    "172.16.254.4",
                    "172.16.254.5",]
    rows = []                
    for each in ipList:
        
        groupRowInfo = rowColumnLayout(numberOfColumns = 5, columnWidth =[400,500])
        checkBox(l = each)
        #get the status of the ips connectivity status
        status = getIpStatus(each)
        textField(text = status, ed = False)
        rows.append(groupRowInfo )
        setParent(uiParent)
            
    return rows       
        
        
        
def getIpStatus(ip):
    
    'determines whether the status of given ip - temp setup'
    
    statusOptions = ['Ready', 'Rendering', 'Not Connected']
    #status = random.choice(statusOptions)
    status = 'Ready'
    return status
                          
    
    
    
#using the rowColumns that are created by - check the contents of their childArray's for info on each computer
#store the info in a list/dictionary ?????


def updateAllIpStatus():
    allInfo = getUiInfo()

    for each in allInfo:
        status = getIpStatus(each['id'])
        textField(each['textFieldId'], edit = True, text = status )

 

def getUiInfo():
    '''
    creates a list of dictionaries - the dictioaries contain the current status information of the users preferences
    '''
    allInfo = []
    for row in renderFarmUI.rows:
        info = {}
        checkBoxId,textFieldId = rowColumnLayout (row, q = True, childArray = True)
        info['id'] = checkBox(checkBoxId, q = True, label  = True )
        info['checkedForRender']  = checkBox(checkBoxId, q = True, v  = True )
        info['status']  = textField(textFieldId , q = True, text = True)
        info['textFieldId'] = textFieldId 
        allInfo.append(info)

        
    return allInfo

    
def returnAvailableIds():
    '''
    based on the current status of all available computers AND the users checkbox selection - 
    returns a the final list of computer ids used to send info to the farm
    *note: also helps to eliminate the possibility computers changing their status befor user submits job 
    '''
    
    allInfo = getUiInfo()
    updateAllIpStatus()
    
    availableIds = []
    for each in allInfo:
        id =  each['id']
        
        checkedForRender = each['checkedForRender']
        status = getIpStatus(id)
        if (checkedForRender == True) and (status == 'Ready'):
            availableIds.append(id)
    return availableIds    
    print availableIds    


def generateFrameSequences(availableMachines,startFrame,endFrame):
    if availableMachines ==[]:
        print "no computers both Ready and checked"
        return 
    if availableMachines !=[]:
        
        

        numberOfFrames = len(range(startFrame,endFrame))
        divisibleFrames = numberOfFrames/len(availableMachines)
        remainderFrames = numberOfFrames % len(availableMachines)  
        
        #generate render frame splits()
        current =startFrame
        lastFrame = endFrame
        sequences = []
        while current<=lastFrame:
            
            
            if current + divisibleFrames + remainderFrames == lastFrame:
                #add the modulo value
                sequenceStart = current +1
        
                sequenceEnd = current + divisibleFrames + remainderFrames
                
                sequences.append((sequenceStart,sequenceEnd))
                #print (sequenceStart,sequenceEnd)
                break
                
                
            if startFrame == current:
                    
                sequenceStart = current
                
            if startFrame != current:   
                
                sequenceStart = current +1
                
            sequenceEnd = current + divisibleFrames
            
            current  =  sequenceEnd
        
            sequences.append((sequenceStart,sequenceEnd))
            #print (sequenceStart,sequenceEnd)
            
    return sequences

def addToQueCommand( outputFramesLocation, renderEngine, startFrame, endFrame, priority, logFileLocation ,sceneLocation ):
    
    jobInfoDictionary = {'commandType':"addToQue", "outputFramesLocation":outputFramesLocation, 'startFrame':startFrame , "endFrame":endFrame,"renderEngine":renderEngine,"priority": priority,"logFileLocation":logFileLocation, "sceneLocation":sceneLocation}
    
    MESSAGE= str(jobInfoDictionary)


    return MESSAGE

def evaluateFarmCommand( ):
    
    jobInfoDictionary = {'commandType':"evaluateFarm"}
    
    MESSAGE= str(jobInfoDictionary)


    return MESSAGE



def sendMessage(id,port,MESSAGE):
    print type(MESSAGE)    
    print MESSAGE
    '''
    Adress=(id,port)
    s = socket.socket()
    s.connect(Adress)
    s.send(MESSAGE)
    print "sent successfully"
    returnMessage = s.recv(1024)
    
    s.close()
     
    
    print "server returned:", returnMessage
    '''
    #return returnMessage
    #my computer is 10.0.0.15 port 51950





def sendToJobStack():
    port = 5015
    renderEngine = "vray"
    #Make sure file we can read in file paths
    
    sceneLocation  = textField( renderFarmUI.sceneLocation_ui, q = True, tx = True)
    
    if not os.path.isfile(sceneLocation):
        error( 'Select a File!')
    
    outputFramesLocation = textField(renderFarmUI.outputFramesLocation_ui, q = True, tx = True)
    
    
    if not os.path.exists(outputFramesLocation):
        os.mkdir(outputFramesLocation)    

    
    startFrame = intField( renderFarmUI.startFrame, q = True, v = True)
    endFrame = intField( renderFarmUI.endFrame, q = True, v = True)
    
    priority = intField( renderFarmUI.priority, q = True, v = True)
    logLocation = textField(renderFarmUI.logFileLocation_ui, q = True, tx = True)
    
    availableMachines = []
    
    
    for each in getUiInfo():
        #print each['status'],each['checkedForRender']
        if each['status']=='Ready' and each['checkedForRender'] == True:
            availableMachines.append(each['id'])    
    
    sequences = generateFrameSequences(availableMachines,startFrame,endFrame)
    
    batchRenderLocation = "C:\\Program Files\\Autodesk\\Maya2014\\bin\\Render.exe"
    
    i = 0    

    for each in sequences:
        startFrame =  sequences[i][0]
        endFrame =  sequences[i][1]
        id =  availableMachines[i]

        i+=1

        MESSAGE = addToQueCommand( outputFramesLocation, renderEngine, startFrame, endFrame, priority, logLocation, sceneLocation )
        sendMessage(id,port,MESSAGE)
    #send the evaluate farm command the render job sequences have been sent
    MESSAGE = evaluateFarmCommand()
    sendMessage(id,port,MESSAGE)
    
    
renderFarmUI()
