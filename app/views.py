from datetime import datetime
from elasticsearch import Elasticsearch
from app import app
from dataGeneration import randomTrafficES as rtgen
from flask import Flask,render_template, request,jsonify
import json
from threading import Thread
from app.modelController import modelController

	
#create model objects
modelCont = modelController()

#Mapbox config
userid=None
mapbox_token='pk.eyJ1Ijoic2hhc2hhbmsxMDI5IiwiYSI6ImNpanp1aGp3azJ6ZWd2Z2x6ZDlobXB1ajkifQ.u-fXXU_MpLS8TxFtt2PAgA'

rdGenStart=True


@app.route('/')
def index():
	#print "Home!!!!!"
	return render_template("map.html",
        title = 'Home',
        mapbox=mapbox_token
        )


@app.route('/output')
def findSpots():
	''' find spots '''
	#print ("output!!")
	lat = request.args.get('lati')
	lon = request.args.get('longi')
	refresh = request.args.get('shouldRefresh', True, type=bool)
	userid = request.args.get('userid')
	parkingids = request.args.get('parkingids')
	spotsData = request.args.get('spotsData')
	parkingSpotRange = "500m"
	minimumNumOfSpots=2
	isNewSpotsFound = True
	
	#print lat
	#print lon
	#print refresh
	#print userid
	#print parkingids
	#print type(parkingids)
	parkingids=json.loads(parkingids)
	#print type(parkingids)
	#print parkingids
	##print len(parkingids)
	# if not userid:
	# 	return render_template("map.html",
 #        title = 'Home',
 #        mapbox=mapbox_token,
 #        error="Please enter a username"
 #        )
 	''' get spots for given location from search index'''
	if(parkingids is None or len(parkingids["ids"])<=minimumNumOfSpots):
		res= modelCont.getAvailableSpots(lat, lon, minimumNumOfSpots)
		#es_search_new_Spots(lat, lon, parkingSpotRange)
		##print res
		# if res[hits][total] == 0:
		# 	parkingSpotRange = "1000m"
		# 	res= es_search_new_Spots(lat, lon, parkingSpotRange)
		isNewSpotsFound=True
		global rdGenStart
		rdGenStart=True
	else:
		isNewSpotsFound=False
		#res = json.dumps(modelCont.updateSpots(parkingids["ids"]))
		'''for random traffic generator'''
		for id in parkingids["ids"]:
			rtgen.ids.append(id)
			if len(rtgen.ids) > 20:
				rtgen.ids.pop(0)
		global rdGenStart
		if rdGenStart:
			rtgen.main()
			rdGenStart=False
		res=modelCont.getUpdatedDocs(parkingids["ids"])

		##print type(res)
	#hits = res[hits][hits]
	#print "got es results"
	# if not refresh:

	# 	return render_template("output.html",lat=lat,lon=lon, res=json.dumps(res), uid=userid, mapbox= mapbox_token)
	# else:
	jsonResult = jsonify(lat=lat, lon=lon, res=res, uid=userid, mapbox=mapbox_token, newSpotsFound = isNewSpotsFound)
	return jsonResult


@app.route('/parkhere')
def parkhere():
	lat = request.args.get('lati')
	lon = request.args.get('longi')
	parklati = request.args.get('parklati')
	parklongi = request.args.get('parklongi')
	parkingspot_id = request.args.get('parkingspotid')
	
# 	res = es.update(index=parkindex, doc_type=parkdoc_type, id = parkingspot_id, 
# 		body= {"doc" : {"isAvailable" : "false" ,"userId":userid}})
# 	if res['error']:
# 		errortype = res['error']['root_cause']['type']
# 		errorreason = res['error']['root_cause']['reason']
# 		return render_template("output.html", errortype = json.dumps(errortype) ,
# 			lat=lat,lon=lon, errorreason=json.dumps(errorreason), message="fail")
# 	else:
# 		return render_template("output.html", messageJson =json.dumps(res), message="success",
# 			lat=lat,lon=lon, parklati=parklati, parklongi= parklongi)

@app.route('/refresh')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return jsonify(result=a + b)

@app.route('/test2')
def test():
	#print "test"
	return render_template("test.html")


# def es_search_new_Spots(lat, lon, parkingSpotRange):
# 	return es.search(index=parkindex, doc_type=parkdoc_type,
# 			body=
# 			{"size" : 20,
# 			"query": 
# 				{"bool": 
# 					{"must":  
# 					  [{"match" :
# 					      {"canPark": True}
# 					    },
# 					    {"match":
# 					      {"isAvailable": True}
# 					    }
# 					  ], 
# 					  "filter":  
# 						[{
# 						"geo_distance":  
# 							{
# 							"distance": parkingSpotRange,
# 							"location": 
# 								{
# 								"lat":lat,
# 								"lon":lon
# 								}
# 							}
# 						},
# 						{
# 					    "range": {
# 					      "avaliableSpots": {
# 					        "gt": 0
# 					      }
# 					    }
# 					  }
# 					  ]
# 					}
# 				},
# 				"sort" : [
# 	       		{
# 	           	"_geo_distance" : {
# 	               "location" : {
# 	                   "lat" : lat,
# 	                   "lon" : lon
# 	               },
# 	               "order" : "asc",
# 	               "unit" : "m",
# 	               "distance_type" : "plane"
# 	           }
# 	       }]
# 			})
#send string message
# @socketSha.on('connect', namespace='/what')
# def handle_my_custom_namespace_event():
# 	#print "hiii"
# 	emit('connect', {'data': 'Connected', 'count': 0})



#socketSha.run(app1)