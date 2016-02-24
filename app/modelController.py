'''


@author: shashank
'''
from datatbase.esFunctions import esFunctions
from datatbase.dbFunctions import dbFunctions

es=None
db=None
    
class modelController(object):
    '''
    classdocs
    '''
    


    def __init__(self):
        global es
        global db
        es=esFunctions()
        db=dbFunctions()

    
    def getAvailableSpots(self,lat, lon, minimumNumOfSpots):
        ''' get available spots for given location'''
        return es.getAvailableSpots(lat, lon, minimumNumOfSpots)
    
    
    def updateSpotsAvailability(self, parkingSpotIdsArray):
        '''get availability updates'''
        return db.getSpotsAvailabilityStatus(parkingSpotIdsArray)
    
    def getUpdatedDocs(self,parkingSpotIdsArray):
        '''get updated doc from search index'''
        es.getDocsOfSpots(parkingSpotIdsArray)