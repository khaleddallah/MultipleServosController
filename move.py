import time
import serial
import sys

import excel
import dataset.nparser as dbparse

#make fram of angle values as string to send it
def MakeFrame ():
	global frameValues
	global lastframe
	if(lastframe==True):
		frameValues = str(str(currentAngles)[:-1])
	else:
		frameValues = str(currentAngles)

#send to serial and receive acknolege
def SendValues ():
	global frameValues
	MakeFrame()
	ser.write(frameValues.encode("utf-8"))
	print (frameValues)
	print (ser.readline())

	

#make the move to target step step
def StepMove (targetAngles):
	for i in range (len(targetAngles)):
		step=1
		
		#make step negative if target less than current
		if targetAngles[i]<currentAngles[i]:
			step = -step
		
		#increase or decrease value
		if currentAngles[i] != targetAngles[i] : 
			currentAngles[i] += step  
	
	SendValues()

#
def MoveToTarget (targetAngles,waitTime=0.001):
	global lastframe
	lastframe=False
	#cal max sub between current and target
	maxSub=0
	curSub=0
	for j in range (len(targetAngles)):
		curSub = abs(currentAngles[j] - int(targetAngles[j]))
		if curSub > maxSub :
			maxSub = curSub
	
	if (maxSub==0) : 
		lastframe=True

	#increase value of angles until reach to target
	for i in range (maxSub):
		if ( i == (maxSub-1) ): 
			lastframe=True
		time.sleep(waitTime)
		StepMove(targetAngles)
	

def highCtrl (sheet=0):
	data,waitTime,targetTime = excel.exlHandler(sheet=int(sheet))
	for i in range (len(data)):
		MoveToTarget(data[i][:-2],float(waitTime[i]))
		time.sleep(targetTime[i])

def highCtrlDB (data):
	print(data)
	global lastframe
	global currentAngles
	lastframe = False
	for i in range (len(data)):
		if ( i == (len(data)-1) ): 
			lastframe=True
		for j in range(11):
			if (j<6):currentAngles[j] = -data[i][j]+90
			else: currentAngles[j] = data[i][j]+90

		#currentAngles = data[i]
		SendValues()
		time.sleep(0.05)
	

#init serial	
ser = serial.Serial('COM5', 115200)
print (ser.readline())

#global var
lastframe=False
frameValues=''
currentAngles=[90]*11

#mov to default angle
MoveToTarget(currentAngles)


if __name__ == "__main__":
	if (len(sys.argv)>=2):
		option = sys.argv[1]
		#-e for excel
		if (option=='-e'):
			if (len(sys.argv)>=3):
				numOfSheet=sys.argv[2]
				highCtrl(numOfSheet)
		#-d direct determine valueAngles
		elif (option=='-d'):
			while True :
				inputVal=input("enter values:")
				inputValSplit=inputVal.split(",")
				valuesInt=[0]*11
				for i in range(len(inputValSplit)):
					valuesInt[i]=int(inputValSplit[i])
					print (valuesInt[i])
				MoveToTarget(valuesInt)
		
		elif (option=='-db'):
			x=dbparse.parse_motions('dataset\walking_01_mmm.xml')
			highCtrlDB(dbparse.proccess(x[0][1]))
			
		
		
		
		else :
			print ('Use : python move.py [option] \n-e  [numOfSheet] :for read from excel files \n-d  to put value directly \nshould put like [10, 33, 22, 45, 24, 12, 33, 44, 13, 12, 10]')
	else :
			print ('Use : python move.py [option] \n-e  [numOfSheet] :for read from excel files \n-d  to put value directly \nshould put like [10, 33, 22, 45, 24, 12, 33, 44, 13, 12, 10]')
	
	ser.close()