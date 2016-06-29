

'''jobstack and monitor

manages the database of shots currently on the farm

split into two catagories render que and currently rendering 

stackAndMonitor listens for jobs and stores them in the render que
when a machine becomes available it will send a command to the client machine to render the job
while the job is rendering the machine will be added to the currently rendering list
jobrmation can be queryed from the computer about its status

main features:



    #render que(renders that are ready to render- but no machine is free to render):
    -listen for new commands and continuously send render commands to free and available machines
    -log what render jobs are in the stack for server machines
    -maintain a priority for each job in the stack
    

    #currently rendering list:
    -log and update the following jobrmation about the status of each render server:

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
            
'''

import subprocess
import operator
import ast
import socket

#import sqlite3   <-may use this as my data base if i can get the hang of it!




def kill(jobId):
        print "killed job: " + str(jobId)

def sentToFarm(job):
        '''do the messaging'''
        print job

def interpretCommand(MESSAGE):
        '''interpret the string message as a dictionary
        returns a dictionary
        '''

        
        value = ast.literal_eval(MESSAGE)
        return value


def getStatus(ipAddress):
        #send a message asking for information
        #recieve a return message with status
        #this command get the ip address host name by the ip address
		hostName = socket.gethostbyaddr("10.0.0.15")[0]        
        status = "Ready"
        
        return status

        
def evaluateFarm():
        
	'''This is the workhorse function of the jobmonitor script, it turns all of the wheels  
	'''

	#get the status of all machines on farm - including busy and available machines:

	for each in availableMachines:
			getStatus()


	#in the case of a job getting finished or chrashing etc, update the jobsBeingRendered que

	#order the render que by the jobs priority

	#Sort the list of dictionaries by the key='priority':

	list_of_dicts.sort(key=operator.itemgetter('priority')) 
			

	#while there are jobs in the render que and the number of busy computers is less than the total amount of computers 
	#keep sending jobs to render farm
	while len(renderQue)>0 and len(busyMachines)<len(availableMachines):

		print "i am in the render loop"
		job = renderQue[0]
		PID = sendCommandToFarm(availableMachines[0],port,MESSAGE) #get a call back message defining the PID
		job["PID"] = PID
		#update the lists

		
		jobsBeingRendered.append(job)
		renderQue.remove(renderQue[0])
		
		availableMachines.remove(availableMachines[0])
		busyMachines.append(availableMachines)

	
	
	print "Evaluate Farm Command Completed!"

def sendCommandToFarm(id,port,MESSAGE):
    #print type(MESSAGE)    
    #print MESSAGE

    Address=(id,port)
    s = socket.socket()
    s.connect(Address)
    s.send(MESSAGE)
    print "sent successfully"
    returnMessage = s.recv(1024)
    
    s.close()
	PID = returnMessage
	return PID
     
    
    print "server returned:", returnMessage

def listen(port):
    #listen on designated port
    Address=('',port)
    MaxClient = 1
    BUFFER_SIZE = 20 
    print ("Waiting for Connection on port  ..." + str(Address[1]))
    s = socket.socket()
    s.bind(Address)
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
    
                                                        
port = 5017  
batchRenderLocation = "C:\\Program Files\\Autodesk\\Maya2014\\bin\\Render.exe"


#data will shift between these two lists to determine

#define these
renderQue = [] #jobs
jobsBeingRendered = [] #jobs

#define these
allNetworkMachines = ["10.0.0.15","10.0.0.17"]
                                          
availableMachines = allNetworkMachines  
busyMachines = [] #ipadresses

currentJobId = 1




while True:
        
        MESSAGE = listen(port)
        #MESSAGE = "{'priority': 50, 'outputFramesLocation': u'\\\\TITAN-PC\\Frames\\TestImages', 'endFrame': 10, 'commandType': 'Render', 'sceneLocation': u'\\\\TITAN-PC\\_Projects\\TestProject_Batch\\scenes\\testScene_001.ma', 'startFrame': 6, 'renderEngine': 'vray'}"


        commandType = interpretCommand(MESSAGE)['commandType']
        print commandType

        if commandType == 'addToQue':
                job = interpretCommand(MESSAGE)
                
                job['id'] = currentJobId +1
                #update the variable
                currentJobId += 1
                
                renderQue.append(job)
                
                break
                
                
                
        if commandType == 'evaluateFarm':
                
                '''an evaluate farm command command will be generated following a render submission - this is neccesary to start the render procees once all of the info has been received and added to the render que'''
                evaluateFarm()

                
                break


        if commandType == 'updateNodeAvailability':
                
                '''set a nodes availability '''


                
                break


                
        if commandType == 'Kill':
                jobId = interpretCommand(MESSAGE)['id']
                kill(jobId)
                break

        if commandType == 'Report':
                print "report"

                
