'''


@author: shashank
'''

from datatbase.dbFunctions import dbFunctions
from datatbase import esconnection



es=None
parkindex= 'park_reg6'
parkdoc_type = 'parksgn6'
dbFunc = None
    
class esFunctions(object):
    '''
    classdocs
    '''
    
    
    def __init__(self):
        global es
        es=esconnection.getConnection()
        global dbFunc
        dbFunc = dbFunctions()
    
    def getSpotsInRange(self,numberOfSpots,lat, lon, innerRange, outerRange,spotsToNotConsider):
        '''get spots in a given range''' 
        numberOfSpots = numberOfSpots%5 + numberOfSpots/5
        query={"size" : numberOfSpots,
            "query": 
                {"bool": 
                    {               
                     "must_not": 
                     [{"ids": {
                       "type": parkdoc_type,
                       "values": spotsToNotConsider
                     }
                    }],
                     "must":  
                      [{"match" :
                          {"canPark": True}
                        },
                        {"match":
                          {"isAvailable": True}
                        }
                      ], 
                      "filter":  
                        [{
                        "geo_distance_range":  
                        {
                        "from": innerRange,
                        "to":outerRange,
                            "location": 
                                {
                                "lat":lat,
                                "lon":lon
                                }
                            }
                        }
                      ]
                    }
                },
                "sort" : [
                   {
                   "_geo_distance" : {
                   "location" : {
                       "lat" : lat,
                       "lon" : lon
                   },
                   "order" : "asc",
                   "unit" : "m",
                   "distance_type" : "plane"
               }
           }]
            }
        return es.search(index=parkindex, doc_type=parkdoc_type,body=query, search_type="scan", scroll="2m")    
        
    
    def getAvailableSpots(self, lat, lon, minimumNumOfSpots):
        ''' get top 10 spots *available* near given location'''
        innerRange=0
        outerRange=500
        incrementRangeBy=200
        incrementSpotsNumBy=1
        numberOfSpots=minimumNumOfSpots+incrementSpotsNumBy
        spotsToNotConsider=[]
        nearestSpotsRespFinal = None
        shouldExtendHits = False
        
        ''' get scan for nearest spots'''
        nearestSpotsScan = self.getSpotsInRange(numberOfSpots,lat,lon,str(innerRange)+'m',str(outerRange)+'m',spotsToNotConsider)
        scrollId = nearestSpotsScan['_scroll_id']
        totalSpotsFound = nearestSpotsScan['hits']['total']
        
        for x in range (0,3):
            '''use scan result to obtain actalk results'''
            nearestSpotsResp= es.scroll(scroll_id=scrollId, scroll= "2m")
            if nearestSpotsRespFinal==None:
                nearestSpotsRespFinal = nearestSpotsResp
            spotsArray=nearestSpotsResp['hits']['hits']                  

            '''check if their is parking available in those spots'''
            nearestSpotsRespFinal = self.setAvailableSpotsNum(nearestSpotsRespFinal,spotsArray, shouldExtendHits)
            ''' return if minimum spot requirement is met'''
            if len(nearestSpotsRespFinal['hits']['hits']) >=minimumNumOfSpots:
                return nearestSpotsRespFinal
            else:
                totalSpotsFound = totalSpotsFound - len(spotsArray)
                if totalSpotsFound < minimumNumOfSpots:
                    nearestSpotsScan = self.getSpotsInRange(numberOfSpots,lat,lon,str(outerRange)+'m',str(outerRange+incrementRangeBy)+'m',spotsToNotConsider)
                    outerRange=outerRange+incrementRangeBy
                    scrollId = nearestSpotsScan['_scroll_id']
                shouldExtendHits=True
                continue
        
#         ''' if not then scroll for more spots except the ones that had availability'''
#         spotsWithAvailability=[]
#         for spotDict in availabilityStatusDict:
#             spotsWithAvailability.append(spotDict.id)
#         ''' remove spots with availability from array of all spots in vicinity to modelController without them'''
#         spotsToNotConsider = list(set(spotsIdsArray)-set(spotsWithAvailability))
#         
#         ''' get more spots '''
#         if totalSpotsFound > numberOfSpots+minimumNumOfSpots-len(availabilityStatusDict):
#             nearestSpotsResp = self.getSpotsInRange(numberOfSpots,lat,lon,str(innerRange)+'m',str(outerRange)+'m',allspotsDict.keys())
#         else:
#             nearestSpotsResp = self.getSpotsInRange(numberOfSpots,lat,lon,str(outerRange)+'m',str(outerRange+incrementRangeBy)+'m',allspotsDict.keys())
#         
#         return self.setAvailableSpotsNum(nearestSpotsResp, availabilityStatusDict)
        
    
    def setAvailableSpotsNum(self,esResultDict,spotsArray, shouldExtendHits):
        '''set number of spots available in elasticsearch result and append results to result JSON'''
        '''update status using database'''
        allspotsDict = {} 
        for spotDict in spotsArray:
            allspotsDict[spotDict['_source']['id']]=spotDict
        availabilityStatusDict= dbFunc.getSpotsAvailabilityStatus(allspotsDict.keys())
        
        '''filter spot ids that have availability'''
        spotsWithAvailability = list(set(availabilityStatusDict.keys()) & set(allspotsDict.keys()))
#         spotsArray=esResultDict['hits']['hits']
        for spotId in spotsWithAvailability:
            allspotsDict[spotId]['_source']['avaliableSpots'] = availabilityStatusDict[spotId][dbFunc.available_spots]
#         for spot in spotsArray:
#             spot['_source']['avaliableSpots'] = dbResultDict[spot['_source']['id']].available_spots
        if shouldExtendHits:
            esResultDict['hits']['hits']=esResultDict['hits']['hits'].extend(allspotsDict)
        else: 
            esResultDict['hits']['hits']=allspotsDict
        return esResultDict
     
    
    def getDocsOfSpots(self, idstosearchArray):
        '''get docs for specified ids'''
        query= {"query": {
                      "ids" : {
                        "type" : parkdoc_type,
                        "values" : idstosearchArray
                    }
                }}
        es.search(index=parkindex, doc_type=parkdoc_type, body=query)    
        
     