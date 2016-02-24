'''


@author: shashank
'''
from datatbase import dbconnection
from datetime import datetime

available_spots = 'available_spots'
total_spots='total_spots'
idField='id'


dbconn = None

class dbFunctions(object):
    '''
    classdocs
    '''

    

    def __init__(self):
        global dbconn 
        dbconn = dbconnection.getConnection()
    
    def getDbConn(self):
        global dbconn
        return dbconn
   
    def  getSpotsAvailabilityStatus(self,parkingSpotIDsArray):  
        '''get spot availability status for array of parking spot ids, return results as dictionary with id as key and named row as value'''
        idsStr = str(parkingSpotIDsArray).replace('[', '(').replace(']',')')
        spotsStatus=dbconn.query("select id,available_spots,total_spots from tms.parkingsignstatus where available_spots>0 and id in "+idsStr)
        statusArray=spotsStatus.dictresult()
        resultDict={}
        for s in statusArray:
            resultDict[s.id]=s
        return resultDict
        
        
    def getSpotAvailability(self,parkingSpotID):
        '''get availability status for one parking spot id, return dictionary with status '''
        spotStatusDict = dbconn.get('tms.parkingsignstatus',parkingSpotID)
        return spotStatusDict
    
    def parkUser(self, userName, userLat, userLon, parkingSpotId):
        '''save parking spot for user'''
        LastparkingSpotId = self.getLastParked(userName)
        if LastparkingSpotId!=None:
#             print "No spot taken"
            self.emptySpace(userName)
        d=datetime.now()
        pd = str(d.year)+'-'+str(d.month)+'-'+str(d.day)+' '+str(d.hour)+':'+str(d.minute)+':'+str(d.second)+'.'+str(d.microsecond)
        userParkingResult = dbconn.insert('TMS.USERSTATUS', username=userName, parkingid=parkingSpotId,userlat=userLat, userlon=userLon, parktime=pd)
        availabilityUpdate = dbconn.query('UPDATE TMS.PARKINGSIGNSTATUS SET AVAILABLE_SPOTS=AVAILABLE_SPOTS-1, LASTUPDATED=$1 WHERE ID=$2 AND AVAILABLE_SPOTS>0',pd,parkingSpotId)
        spots = dbconn.query('select AVAILABLE_SPOTS from TMS.PARKINGSIGNSTATUS where ID=$1',parkingSpotId)
        historyUpdate = dbconn.query('INSERT INTO TMS.PARKINGSIGNSSTATUSHISTORY (USERNAME,PARKINGID,AVAILABLE_SPOTS,WAS_SPOT_TAKEN,UPDATETIME)values($1,$2,$4, TRUE, $3)',userName, parkingSpotId,pd, spots.dictresult()[0][available_spots])
        
    def emptySpace(self, userName):
        parkingSpotId = self.getLastParked(userName)
        if parkingSpotId==None:
#             print "No spot taken"
            return
        d=datetime.now()
        pd = str(d.year)+'-'+str(d.month)+'-'+str(d.day)+' '+str(d.hour)+':'+str(d.minute)+':'+str(d.second)+'.'+str(d.microsecond)
        userParkingResult = dbconn.query('UPDATE TMS.USERSTATUS SET RELEASETIME=$1 WHERE USERNAME=$2 AND PARKINGID=$3;',pd, userName, parkingSpotId)
#         print userParkingResult
        availabilityUpdate = dbconn.query('UPDATE TMS.PARKINGSIGNSTATUS SET AVAILABLE_SPOTS=AVAILABLE_SPOTS+1, LASTUPDATED=$1 WHERE ID=$2 AND AVAILABLE_SPOTS<TOTAL_SPOTS',pd, parkingSpotId)
#         print availabilityUpdate
        spots = dbconn.query('select AVAILABLE_SPOTS from TMS.PARKINGSIGNSTATUS where ID=$1',parkingSpotId)
        historyUpdate = dbconn.query('INSERT INTO TMS.PARKINGSIGNSSTATUSHISTORY (USERNAME,PARKINGID,AVAILABLE_SPOTS,WAS_SPOT_TAKEN,UPDATETIME)values($1,$2,$4, TRUE, $3)',userName, parkingSpotId,pd, spots.dictresult()[0][available_spots])
#         print historyUpdate

    def getLastParked(self, userName):
        lastParkResult = dbconn.query('select parkingid from TMS.USERSTATUS where username=$1 and releasetime is NULL', userName)
        lastParkResult = lastParkResult.dictresult()
        if len(lastParkResult)==0:
#             print "No spot taken"
            return None
        else:
            return lastParkResult[0]['parkingid']

    def getAllParkingSpotIds(self):
        result = dbconn.query('select id from TMS.CONDENSEPARKSIGNS ')
        return result.dictresult()