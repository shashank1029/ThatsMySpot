from elasticsearch import Elasticsearch, helpers
import csv
import json
import re
from json import JSONDecoder
es=Elasticsearch(["http://52.6.160.100:9200"])

#filename="/home/osboxes/insight/data/Elasticsearch_park_reg.csv"
jsonFile= "/home/osboxes/insight/data/Elasticsearch_park_reg.json"
#rf = open(filename,'r')
#jsonr = open(jsonFile)
#rd = csv.reader(rf)
#print(rd.next())

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

class ConcatJSONDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            objs.append(obj)
        return objs

print "decoding"
jsonList = json.load(open(jsonFile), cls=ConcatJSONDecoder)

def getJSON():
	for s in jsonList:
		yield s

print "uploading"
helpers.bulk(es,getJSON())
print "done"