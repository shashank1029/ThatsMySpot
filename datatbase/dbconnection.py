'''

@author: shashank
'''
from pg import DB

postGresConnection = None

def getConnection():
    global postGresConnection
    if postGresConnection==None:
        postGresConnection = DB(dbname="mydb", host='52.70.246.158', port=5432, user="sha", passwd="sha")
    return postGresConnection

def closeConnection():
    postGresConnection.close()
    postGresConnection=None
