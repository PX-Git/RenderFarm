#listening script
import socket, time,os, random , subprocess


"""This script will need to do the following


LISTEN :

-idlely listen for a command on port XXXX


upon recieving a command:

RENDER and RECORD:
Once a command has been recieved decode it and render 

 
decode the command to start the render process and generate information about it - including:

-a job name - based on the name of the scene(this will be the same on multiple machines)
-a path to the maya render log file the server machine will generate
-the process id number associated with render currently running on the machine
-the standard out pipe (a way to check the standard output codes(0,211,ect))
-frame output directory


upon a Proccess ID number being generated:

LISTEN and ACT and REPORT:
once a render is in progress a new reporting mode will commence
Renders may take several hours or even days to finish in this time, the following may occur:


-render may be killed by client machine via jobstack
    which will kill the job entirely
-server machine may become occupied by new user
-sudden power loss on server machine
    which will kill the job on the client machine anf

normal opperation:
while the render is in progress listen on port XXXX

Listen for the following commands from a jobStack:

Kill:
    kill the render by stopping the PID

Report :
    -Status(Rendering, Id)
    -job name
    -path to the maya render log
    -the process id number associated with render currently running on the machine
    -frame output directory
    -start time and how long the render has been running

    Some nice to have functions:
    
    -how long have the current frames been running
    -what frames have been rendered
    -what frames are remaining to be rendered
    -what frames are currently being rendered

"""

port = 5015


"""Run main loop until we get a render to pick up, that wil progress the script and return a processID"""





    
def mainLoop():

    #LISTEN:
    MESSAGE = listen() #Runs until a command is recieved, returning the raw message

    #INTERPERATE
    commandType, messageContent = identifyCommand(MESSAGE) #converts the Message into a useable command
                                                                #render 
                                                                #kill
                                                                #report

    #EXECUTE #KILL or #REPORT

    '''

    Info  dictionary records the following:
        #"jobName": a job name - based on the name of the scene(this will be the same on multiple machines)
        #"logPath": a path to the maya render log file the server machine will generate
        #"PID":the process id number associated with render currently running on the machine
        #"PIPE"the standard out pipe (a way to check the standard output codes(0,211,ect))
        #"frameOutputLocation": frame output directory

    #Kill commands will return the string "Killed" or "Not Killed"?

    '''

     #Exccutes one of the three commands based on command type

    if commandType == "Render":
        info = render(messageContent)

    if commandType == "Kill":
        info = kill(messageContent)


    if commandType == "Report":
        info = generateReport(messageContent)


    sendToJobStack(info)

    
def listen(port)
    #listen on designated port
    Adress=('',port)
    MaxClient=1
    BUFFER_SIZE = 20 
    print ("Waiting for Connection on port  ..." + str(Adress[1]))
    s = socket.socket()
    s.bind(Adress)
    s.listen(MaxClient)
    clientSocket,incAddress = s.accept()
    print incAddress
    print('Got a connection from: '+ str(incAddress) +'.')

    while 1:
        MESSAGE = clientSocket.recv(BUFFER_SIZE)
        if not MESSAGE: break

        print "received data:", data
        clientSocket.send("receved the message!")  # echo

    clientSocket.close()
    return MESSAGE
    

def identifyCommand(MESSAGE)
    '''This command will identify the string message as one of the following
    
    Render - flag flag info flag blah
    Kill - pid
    Report()

    then return the command type and the command
    '''
    commandType, command =  MESSAGE.split(" --> ")

    return commandType, messageContent

    
    
def render( command ):
    #receives batchRenderLocation, outputLocation, startFrame, endFrame, renderEngine, scene






batchRenderLocation = "C:\\Program Files\\Autodesk\\Maya2014\\bin\\Render.exe"


#search the log figure out what the currrent log number is and iterate by +1
logID = "00001"
logFileDirectory = "\\\\TITAN-PC\\Frames\\Logs\\"
log = logFileDirectory + "RenderLog_" + str(logID) + ".txt"
print logFile 


params = [batchRenderLocation]
params += ['-rd', outputFramesLocation]
params += ['-r', renderEngine]
params += ['-s', str(startFrame)]
params += ['-e', str(endFrame)]
params += ['-log',logFile]

params += [sceneLocation]
print params


#-archive [file]

PID = subprocess.Popen(params, stdin=subprocess.PIPE,  
                                   stdout=subprocess.PIPE,  
                                   stderr=subprocess.PIPE)
PID.pid


subprocess.Popen.wait(PID)
output, errors = PID.communicate()  

print output
print errors 













def kill(PID):
    killStatus = "Killed"
    return killStatus




def generateReport()    


    info = {}
    status = getStatus() # where am i in the loop?
    if status == "Ready"
        info['status'] = "Ready"
    if status == "Rendering"
        jobName = getJobName()
        -path to the maya render log
        -the process id number associated with render currently running on the machine
        -frame output directory
        -start time and how long the render has been running


    
    return info


while True:

    mainLoop()
    raw_input()

















#subprocess.call(["shutdown", "-f", "-s", "-t", "5"])
#print 'hi'
#shutdown -r

