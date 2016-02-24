import csv
import json
import re

print ("started")

parkindex='park_reg6'
parkdoc_type="parksgn6"

#index files
# requires CSV file to be sorted based on order number
filename="/home/osboxes/insight/data/Elasticsearch_park_reg2.csv"
fileToBeIndexed = "/home/osboxes/insight/data/Elasticsearch_park_reg_condensed.csv"
jsonFile= "/home/osboxes/insight/data/Elasticsearch_park_reg6_1.json"
csvFileR = open(filename,'r')
jsonWr = open(jsonFile, 'w')
csvWr = open(fileToBeIndexed, 'w')
csvRd = csv.reader(csvFileR)
#initialize a few variables
ordernum=""
distance=0
lastDistanceFromCurb=0
lastOrderNum=""
signdesc=[]
row=[]
totalSpots=0
#write json file and csv file with condensed parking reg and calculating available spots and no parking spots
header = csvFileR.__next__()
csvWr.write(header)
print (header)
for rownew in csvRd:
    ordernum2=rownew[2]
    distance2=int(rownew[5])
    sgn=rownew[10].strip()
    if (ordernum== ""):
        if sgn and sgn!="":
            signdesc.append(sgn)
        row = rownew
        ordernum=ordernum2
        distance=distance2
        #print ("1", ordernum, distance,signdesc)
        continue
    elif (ordernum==ordernum2 and distance==distance2):
        if sgn and sgn!="":
            signdesc.append(sgn)
        #print ("2", ordernum, distance,signdesc)
        continue
    else:
        if (any("ANYTIME" in s for s in signdesc)):
            canPark="false"
        else:
            canPark="true"
        if ordernum!=lastOrderNum:
            lastDistanceFromCurb=0

        #print (distance, lastDistanceFromCurb)
        totalSpots= (distance-lastDistanceFromCurb)/15
        totalSpots = int (totalSpots)
        #write in JSON file
        json.dump({
        "_op_type": "create",
        "_index": parkindex,
        "_id": row[0],
        "_type": parkdoc_type,
        "_source": {
            "id": int(row[0]),
            "borough": row[1],
            "ordernum": row[2],
            "seqnum": int(row[3]),
            "SG_MUTCD_C": row[4],
            "distfromcurb": int(row[5]),
            "signfc": row[6],
            "arrow": row[7],
            "x": float(row[8]),
            "y": float(row[9]),
            "signdesc": signdesc,
            "location": {
                "lat": row[11],
                "lon": row[12]
            },
            "main_street": row[13],
            "from_street": row[14],
            "to_street": row[15],
            "direction": row[16],
            "canPark": canPark,
            "noParkDays": [],
            "noParkTime": [],
            "canParkDays": [],
            "canParkTime": [],
            "canParkDuration": -1,
            "isAvailable": canPark,
            "userId": "",
            "totalSpots": totalSpots,
            "avaliableSpots": totalSpots
            }
            },jsonWr)
        jsonWr.write("\r\n")
        #write in CSV file
        sign =""
        #sign = signdesc[0]
        for i in range(0,len(signdesc)):
            temp=signdesc[i]
            #if temp=="" or not temp:
             #   continue
            if i==0:
                sign=temp
            else:
                sign = sign+","+temp

        sign = "\"{"+sign+"}\""
        csvWr.write(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+","+row[6]+","+row[7]+","+row[8]
                    +","+row[9]+","+sign+","+row[11]+","+ row[12]+","+row[13]+","+row[14]+","+row[15]+","+ row[16]+","
                    + canPark+","+str(totalSpots)+","+ str(totalSpots))
        csvWr.write("\n")
        #print ("3", ordernum, distance,signdesc)
        del signdesc[:]
        lastDistanceFromCurb=distance
        lastOrderNum=ordernum
        sgn=rownew[10].strip()
        if sgn and sgn!="":
            signdesc.append(sgn)
        row=rownew
        ordernum=ordernum2
        distance=distance2


if len(row)>0:
        if (any("ANYTIME" in s for s in signdesc)):
            canPark="false"
        else:
            canPark="true"

        if ordernum!=lastOrderNum:
            lastDistanceFromCurb=0

        print (distance, lastDistanceFromCurb)
        totalSpots= (distance-lastDistanceFromCurb)/15
        totalSpots = int (totalSpots)

        json.dump({
        "_op_type": "create",
        "_index": parkindex,
        "_id": row[0],
        "_type": parkdoc_type,
        "_source": {
            "id": int(row[0]),
            "borough": row[1],
            "ordernum": row[2],
            "seqnum": int(row[3]),
            "SG_MUTCD_C": row[4],
            "distfromcurb": int(row[5]),
            "signfc": row[6],
            "arrow": row[7],
            "x": float(row[8]),
            "y": float(row[9]),
            "signdesc": signdesc,
            "location": {
                "lat": row[11],
                "lon": row[12]
            },
            "main_street": row[13],
            "from_street": row[14],
            "to_street": row[15],
            "direction": row[16],
            "canPark": canPark,
            "noParkDays": [],
            "noParkTime": [],
            "canParkDays": [],
            "canParkTime": [],
            "canParkDuration": -1,
            "isAvailable": canPark,
            "userId": "",
            "totalSpots": totalSpots,
            "avaliableSpots": totalSpots
            }
            },jsonWr)
        jsonWr.write("\r\n")
        #write in CSV file
        sign = ""
        for i in range(0,len(signdesc)):
            temp=signdesc[i]
            #if temp=="" or not temp:
             #   continue
            if i==0:
                sign=temp
            else:
                sign = sign+","+temp

        sign = "\"{"+sign+"}\""
        csvWr.write(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+","+row[6]+","+row[7]+","+row[8]
                    +","+row[9]+","+sign+","+row[11]+","+ row[12]+","+row[13]+","+row[14]+","+row[15]+","+ row[16]+","
                    + canPark+","+str(totalSpots)+","+ str(totalSpots))
        csvWr.write("\n")
        print ("3", ordernum, distance,signdesc)

jsonWr.close()
csvWr.close()

print ("JSON file created")