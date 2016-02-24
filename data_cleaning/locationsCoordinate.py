import csv
import geocoder
import time

read= open('/home/osboxes/insight/locations.CSV','rb')
reader=csv.reader(read)
writefile=open('/home/osboxes/insight/locations_c.CSV','wb')
writer=csv.writer(writefile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
boroughs={'B':'Bronx', 'K':'Brooklyn', 'M':'Manhattan', 'Q':'Queens', 'S':'Staten Island'}
print "starting"
count=0
for row in reader:
	#columns=row.split(',')
	if len(row) < 2 or int(row[0]) < 2460:
		print "omitted " + row[0]
		continue


	if count>=2100:
		print "Count over"
		break
	
	#print row
	borough=row[1]
	main_st=row[3]
	one_st=row[4]
	two_st=row[5]

	print(row[0], main_st, one_st, two_st)
	st_1=main_st + ' and ' + one_st +','+ boroughs[borough]+', New York City'
	g=geocoder.google(st_1)
	count=count+1
	print (st_1, g)
	lon_1=g.geojson['geometry']['coordinates'][0]
	lat_1=g.geojson['geometry']['coordinates'][1]
	print("1st st")
	print(row, lon_1, lat_1)
	time.sleep(.2)

	st_2=main_st + ' and ' + two_st +','+ boroughs[borough]+', New York City'
	g2=geocoder.google(st_2)
	count=count+1
	print (st_2, g2)
	lon_2=g2.geojson['geometry']['coordinates'][0]
	lat_2=g2.geojson['geometry']['coordinates'][1]
	print ("2nd st")
	print(row, lon_2,lat_2)
	writer.writerow([','.join(row) , lon_1, lat_1,g,lon_2, lat_2, g2])
	time.sleep(.2)


read.close()
writefile.close()