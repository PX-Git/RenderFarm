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

    '''

    Info  dictionary records the following:
        #"jobName": a job name - based on the name of the scene(this will be the same on multiple machines)
        #"logPath": a path to the maya render log file the server machine will generate
        #"PID":the process id number associated with render currently running on the machine
        #"PIPE"the standard out pipe (a way to check the standard output codes(0,211,ect))
        #"frameOutputLocation": frame output directory

    #Kill commands will return the string "Killed" or "Not Killed"?

    '''
    #LISTEN:
	MESSAGE = listen(port)
	#MESSAGE = "{'priority': 50, 'outputFramesLocation': u'\\\\TITAN-PC\\Frames\\TestImages', 'endFrame': 10, 'commandType': 'Render', 'sceneLocation': u'\\\\TITAN-PC\\_Projects\\TestProject_Batch\\scenes\\testScene_001.ma', 'startFrame': 6, 'renderEngine': 'vray'}"


	commandType = interperateCommand(MESSAGE)['commandType']
	
	print commandType

	if commandType == 'Render':
		job = interperateCommand(MESSAGE)
		
		
		
		break


	if commandType == 'updateNodeAvailability':
			
		'''set a nodes availability '''


		
		break


			
	if commandType == 'Kill':
		jobId = interperateCommand(MESSAGE)['id']
		kill(jobId)
		break

	if commandType == 'Report':
		print "report"

    sendToJobStack(info)

    
def listenForCommands(port):

	'''the render machine will need to:
		
		listen for a connection,
		interperate the command,
		execute some command
		return a message 
		
		all while the socket is still open
		
		
		'''
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
		
		interperateCommand(MESSAGE)
		
		
	commandType = interperateCommand(MESSAGE)['commandType']
	
	print commandType

	if commandType == 'Render':
		job = interperateCommand(MESSAGE)
		
		


	if commandType == 'updateNodeAvailability':
			
		'''set a nodes availability '''



			
	if commandType == 'Kill':
		jobId = interperateCommand(MESSAGE)['id']
		kill(jobId)
		break

	if commandType == 'Report':
		print "report"		
		
		
		
		
		
		
		
		
		
        clientSocket.send("receved the message!")  # echo

    clientSocket.close()
    return MESSAGE

def interperateCommand(MESSAGE):
        '''interperate the string message as a dictionary
        returns a dictionary
        '''

        
        value = ast.literal_eval(MESSAGE)
        return value

    
    
def render( batchRenderLocation, outputFramesLocation renderEngine startFrame endFrame,logFileDirectory,sceneLocation ):
    #receives batchRenderLocation, outputLocation, startFrame, endFrame, renderEngine, sceneLocation




	logFile = generateLog(logFileDirectory )


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


	return PID
	#subprocess.Popen.wait(PID)
	#output, errors = PID.communicate()  

	#print output
	#print errors 

def generateLog(logFileDirectory ):

	#this command get the ip adress host name

	
	
	hostName = socket.gethostname()
	
	dir = os.path.join (logFileDirectory, hostName)
	
	if os.listdir(dir) != []:
		#search the log figure out what the currrent log number is and iterate by +1

		highestVersionOfLog = checkMaxVersion(dir)
		logFile = increment(highestVersionOfLog)
		
	if os.listdir(dir) == []:
		#create the first file
		logFile = dir + "\\" + "renderlog.00001.txt"
		
	
	return logFile






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

currentVersion = checkCacheVersion(individualCharDir)

cacheDir = individualCharDir + '/' + currentVersion	
	
	
def increment(s):
    """ look for the last sequence of number(s) in a string and increment 
        This function is used to iterate versions of folders in the script
    """
    numbers = re.compile('\d+')
    if numbers.findall(s):
        lastoccr_sre = list(numbers.finditer(s))[-1]
        lastoccr = lastoccr_sre.group()
        lastoccr_incr = str(int(lastoccr) + 1)
        if len(lastoccr) > len(lastoccr_incr):
            lastoccr_incr = zfill(lastoccr_incr, len(lastoccr))
        return s[:lastoccr_sre.start()]+lastoccr_incr+s[lastoccr_sre.end():]

    return s

def checkMaxVersion(dir):
    
    
    versions =  os.listdir( dir )
    if versions == []:
        versions = ['Empty']      
    currentHighestVersion = max(versions)
    
    return currentHighestVersion
	
	
	
	
	
	

while True:

    mainLoop()
    raw_input()

















#subprocess.call(["shutdown", "-f", "-s", "-t", "5"])
#print 'hi'
#shutdown -r

