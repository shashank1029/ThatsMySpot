'''


@author: shashank
'''
from elasticsearch import Elasticsearch

elasticSearchConnection= None

def getConnection():
    global elasticSearchConnection
    if elasticSearchConnection==None:
        elasticSearchConnection=Elasticsearch(["http://52.71.241.40:9200","http://52.6.160.100:9200", "http://52.70.246.158:9200", "http://52.71.221.173:9200" ])
    return elasticSearchConnection    
    