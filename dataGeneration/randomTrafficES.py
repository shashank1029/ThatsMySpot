import random
from elasticsearch import Elasticsearch, TransportError, helpers
from threading import Thread
from time import sleep


#es=Elasticsearch(["http://52.6.160.100:9200"])
es=Elasticsearch(["http://52.71.241.40:9200"])	#datanode3
parkindex= 'park_reg5copy'
parkdoc_type = 'parksgn5copy'
ids=[50]
#ids=[245262, 324327, 245259, 245283, 14734, 64629, 35287, 324328, 68719, 14736, 35289, 14737, 245286, 61525, 29440, 324333, 35292, 29441, 29451, 32637]
minParkingID = 0
sleeptime=0.2
#maxParkingID = minParkingID +len(ids)-1 #376863

def occupySpot(parkingId):
	res=""
	res=es.search(index=parkindex, doc_type=parkdoc_type,
				body={
				  "query": {
				    "terms": {
				      "_uid": 
				      [  parkdoc_type+"#"+str(parkingId)]
				    }
				  }
				})
	#print res
	lis=res["hits"]["hits"]
	s={}
	for i in lis:
		s.update(i)

	if "_source" in s and s["_source"]["avaliableSpots"] > 0 :
		res = es.update(index=parkindex, doc_type=parkdoc_type,id=parkingId,body={
		"script":
		{
			"inline": "ctx._source.avaliableSpots -= count",
        	"params" : 
        	{
            	 "count" : 1
         	} 
   		}
 		})
 		print ("occupy", parkingId)
 		#print res
 	#print res

def releaseSpot(parkingId):
	res=""
	res=es.search(index=parkindex, doc_type=parkdoc_type,
				body={
				  "query": {
				    "terms": {
				      "_uid": 
				      [  parkdoc_type+"#"+str(parkingId)]
				    }
				  }
				})
	lis=res["hits"]["hits"]
	source={}
	for i in lis:
		source.update(i)
	if "_source" in source and source["_source"]["avaliableSpots"] < source["_source"]["totalSpots"]:
		res=es.update(index=parkindex, doc_type=parkdoc_type,id=parkingId,body={
 	 		"script":
 		{
 			"inline": "ctx._source.avaliableSpots += count",
        	"params" : {
             	"count" : 1
         	} 
   		}
 		})
 		print ("release", parkingId)
 	#print res

def printit(w):
	print w


def occupySpotMethod(r):
	#while true:
	for x in range(r):
		maxParkingID = minParkingID +len(ids)-1
		sleep(sleeptime)
		#parkingId=random.randint(minParkingID,maxParkingID)
		parkingId=ids[random.randint(minParkingID,maxParkingID)]
		#parkingId=999999999
		try:
			
			#printit(parkingId)
			
			occupySpot(parkingId)
			#releaseSpot(parkingId)
		except TransportError as e:
			print ("id not found", parkingId, e)
			continue
		
	

def releaseSpotMethod(r):
	#while true:
	for x in range(r):
		maxParkingID = minParkingID +len(ids)-1
		sleep(sleeptime)
		#parkingId=random.randint(minParkingID,maxParkingID)
		parkingId=ids[random.randint(minParkingID,maxParkingID)]
		#parkingId=999999999
		try:
			
			#printit(parkingId)
			#occupySpot(parkingId)

			releaseSpot(parkingId)
		except TransportError as e:
			print ("id not found", parkingId, e)
			continue


def main():
	numberOfTransactions=1000
 	print "start"
 	thread1=Thread(target=occupySpotMethod,args=[numberOfTransactions])
 	thread2=Thread(target=releaseSpotMethod,args=[numberOfTransactions])
 	thread1.start()
 	thread2.start()
 	#thread1.join()
 	#thread2.join()
 	print "finish"


if __name__ == '__main__':
 	main()
 	