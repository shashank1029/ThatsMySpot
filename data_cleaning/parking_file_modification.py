import csv

read = open('/home/ubuntu/data/Parking_regulations.csv','rb')
reader = csv.reader(read)
writef=open('/home/ubuntu/data/Parking_regulations_es.csv','wb')
writer= csv.writer(writef)
count=0
for row in reader:
	if count==0:
		writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],'location'])
		count=1
		continue
	writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]+', '+row[12]])

read.close()
writef.close()
