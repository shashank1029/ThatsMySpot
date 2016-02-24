from datetime import datetime
from elasticsearch import Elasticsearch
from app import app
from dataGeneration import randomTrafficES as rtgen
from flask import Flask,render_template, request,jsonify
import json


from threading import Thread

#Elasticsearch config
#es=Elasticsearch(["http://52.6.160.100:9200"]) #masternode
es=Elasticsearch(["http://52.71.241.40:9200","http://52.6.160.100:9200", "http://52.70.246.158:9200", "http://52.71.221.173:9200" ])	

parkindex= 'park_reg5copy'
parkdoc_type = 'parksgn5copy'

#Mapbox config
userid=None
mapbox_token='pk.eyJ1Ijoic2hhc2hhbmsxMDI5IiwiYSI6ImNpanp1aGp3azJ6ZWd2Z2x6ZDlobXB1ajkifQ.u-fXXU_MpLS8TxFtt2PAgA'

rdGenStart=True
#Flask socket IO config
# app1 = Flask(__name__)
# app1.config['SECRET_KEY'] = 'secret!'
# socketSha = SocketIO(app1)


@app.route('/')
def index():
	#print "Home!!!!!"
	return render_template("map.html",
        title = 'Home',
        mapbox=mapbox_token
        )

        #return ("Got %d hits:" %res['hits']['total'])

@app.route('/output')
def findSpots():

	#print ("output!!")
	lat = request.args.get('lati')
	lon = request.args.get('longi')
	refresh = request.args.get('shouldRefresh', True, type=bool)
	userid = request.args.get('userid')
	parkingids = request.args.get('parkingids')
	parkingSpotRange = "500m"
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
	if(parkingids is None or len(parkingids["ids"])<=2):
		res= es_search_new_Spots(lat, lon, parkingSpotRange)
		##print res
		# if res[hits][total] == 0:
		# 	parkingSpotRange = "1000m"
		# 	res= es_search_new_Spots(lat, lon, parkingSpotRange)
		isNewSpotsFound=True
	else:
		idstosearch = []
		isNewSpotsFound=False
		
		#print ("len", len(parkingids["ids"]))
		for id in parkingids["ids"]:
			idstosearch.append(parkdoc_type+"#"+str(id))
			rtgen.ids.append(id)
			if len(rtgen.ids) > 20:
				rtgen.ids.pop(0)
		global rdGenStart
		if rdGenStart:
			rtgen.main()
			rdGenStart=False
		# sleepT = rtgen.sleeptime
		# rtgen.sleeptime=1
		# rtgen.ids=rtgen.ids.extend(parkingids["ids"])
		# rtgen.sleeptime= sleepT
		#print(idstosearch)
		res=es.search(index=parkindex, doc_type=parkdoc_type,
				body={
				  "query": {
				    "terms": {
				      "_uid": 
				        idstosearch
				      
				    }
				  }
				})

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
	res = es.update(index=parkindex, doc_type=parkdoc_type, id = parkingspot_id, 
		body= {"doc" : {"isAvailable" : "false" ,"userId":userid}})
	if res['error']:
		errortype = res['error']['root_cause']['type']
		errorreason = res['error']['root_cause']['reason']
		return render_template("output.html", errortype = json.dumps(errortype) ,
			lat=lat,lon=lon, errorreason=json.dumps(errorreason), message="fail")
	else:
		return render_template("output.html", messageJson =json.dumps(res), message="success",
			lat=lat,lon=lon, parklati=parklati, parklongi= parklongi)

@app.route('/refresh')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return jsonify(result=a + b)

@app.route('/test2')
def test():
	#print "test"
	return render_template("test.html")


def es_search_new_Spots(lat, lon, parkingSpotRange):
	return es.search(index=parkindex, doc_type=parkdoc_type,
			body=
			{"size" : 20,
			"query": 
				{"bool": 
					{"must":  
					  [{"match" :
					      {"canPark": True}
					    },
					    {"match":
					      {"isAvailable": True}
					    }
					  ], 
					  "filter":  
						[{
						"geo_distance":  
							{
							"distance": parkingSpotRange,
							"location": 
								{
								"lat":lat,
								"lon":lon
								}
							}
						},
						{
					    "range": {
					      "avaliableSpots": {
					        "gt": 0
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
			})
#send string message
# @socketSha.on('connect', namespace='/what')
# def handle_my_custom_namespace_event():
# 	#print "hiii"
# 	emit('connect', {'data': 'Connected', 'count': 0})



#socketSha.run(app1)