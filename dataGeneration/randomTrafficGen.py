'''

@author: shashank
'''
from threading import Thread
from time import sleep
import random
from datatbase.dbFunctions import dbFunctions
from datetime import datetime


dbFunc1 = dbFunctions()
dbFunc2 = dbFunctions()
minParkingID=0
minUserId=0
ids=dbFunc1.getAllParkingSpotIds()

sleeptime=0.0
maxLat = 40.912462
minLat = 40.499776
maxLon=-73.70057
minLon = -74.253838

fileread = open('/home/osboxes/randomeNames.txt','r')
users = fileread.readlines()
maxUserID = minUserId + len(users)-1
maxParkingID = minParkingID +len(ids)-1

def releaseSpotMethod(r):
    for x in range(r):
        userName = users[random.randint(minUserId, maxUserID)].split(' ',1)[0]
        dbFunc1.emptySpace(userName)
        sleep(sleeptime)

def occupySpotMethod(r):
    
#     print parkingId
    
    for x in range(r):
        for x in range(r):
            userName = users[random.randint(minUserId, maxUserID)].split(' ',1)[0]
            userName1 = users[random.randint(minUserId, maxUserID)].split(' ',1)[0]
            parkingId=ids[random.randint(minParkingID,maxParkingID)]['id']
            dbFunc2.parkUser(userName, random.uniform(minLat, maxLat), random.uniform(minLon, maxLon), parkingId)
#             sleep(sleeptime)
            dbFunc1.emptySpace(userName1)
            sleep(sleeptime)
            if x%100==0:
                print (x,datetime.now())
        
        
        print ("outer ",x,datetime.now())
        
      
def main():
    numberOfTransactions=1000
    print "start"
    thread1=Thread(target=occupySpotMethod,args=[numberOfTransactions])
#     thread2=Thread(target=releaseSpotMethod,args=[numberOfTransactions])
    thread1.start()
#     thread2.start()
     #thread1.join()
     #thread2.join()
    print "finish"


if __name__ == '__main__':
    main()  