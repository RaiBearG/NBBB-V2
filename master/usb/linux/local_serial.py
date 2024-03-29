import serial, pickle, math, time



baud_rate = 115200


#m and b values of front yard found using tools/line_parameters.py
m = 2.347939316690
b = 335.732012260547
#height = 0 #height of the device in ft 


def find_point(m, b, x, y):
	"""
	m,b equation variables of reference line
	x,y real time point. 
	find distance between (x,y) and y=mx+b
	"""
	# p = slope of perpendicular line
	p = -(1/m)
	#print p
	# c = y intersept of perpendicular line
	c = y - (p*x)
	#print c

	lon = (c-b)/(m-p)
	lat = (m*lon) + b

	return lat, lon

def distance (lat1, lon1, lat2, lon2):
	"""
	Finds the distance between 2 GPS lat and long 
	coordinates in inches
	"""
	dlong = (lon2 - lon1) * math.pi / 180.0
	dlat = (lat2 - lat1) * math.pi / 180.0
	a = pow(math.sin(dlat/2.0), 2) + math.cos(lat1*math.pi/180.0) * math.cos(lat2*math.pi/180.0) * pow(math.sin(dlong/2.0),2)
	c =  2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	#convert distance it inches
	d = 6367 * c * 39370.07874016

	return d


def main():

	serial_port = input('Enter port number. example "/dev/ttyUSB0" : ')
	ser = serial.Serial(port=serial_port,
											baudrate=baud_rate)

	try:
		time.sleep(2)
		height = input('Enter the height of the GPS from ground in ft : ')
		while True:
			msg = ser.readline()
			
			if msg:
				commas=[]
				for ind, val in enumerate(msg):
					#print (ind, val)
					if (val == ','):
						commas.append(int(ind))
				if len(commas) == 4:

					lat = float(msg[1:(commas[0])])
					
					lon = float(msg[(commas[0]+2):(commas[1])])
					
					status = int(msg[(commas[1]+2)])
					
					sats = int(msg[(commas[2]+2):(commas[3])])
				
					imu = int(msg[(commas[3]+2):-2])
					
					tilt = float(abs(imu/70.0))
					

					
					linepoint = find_point(m, b, lon, lat)
					dist = distance(lat, lon, linepoint[0], linepoint[1])
					if lon<linepoint[1]:
						dist = dist*-1
					howfarout = distance(48.015409967799, -122.540046375689, lat, lon)
					howfarout = abs(pow(dist,2)-pow(howfarout,2))
					howfarout = (math.sqrt(howfarout))/12
					if lat < 48.015409967799:
						howfarout = howfarout * -1

					tilterror = height * math.tan(tilt*math.pi/180.0) * 12

					if imu<0:
						direction = 'right'
						dist = dist - tilterror
					else:
						direction = 'left'
						dist = dist + tilterror
						#printing stuff
					print "***"
					print "Dist from center: %f inches" %  dist
					print "%f ft out from ramp's start" % howfarout
					if status == 0:
						fix = "no fix"
					elif status == 1:
						fix = "single point"
					elif status == 2:
						fix = "DGPS"
					elif status == 3:
						fix = "Float RTK"
					elif status == 4:
						fix = "fixed RTK"
					print "Fix : %s  Sattelites : %d" % (fix, sats)
					print "lat: %.12f  lon: %.12f" % (lat, lon)
					print "Tilted %.2f degrees to the %s" % (tilt, direction)
					print "***"
				 	
	except KeyboardInterrupt:
		pass
	if ser.isopen():
		ser.close()

if __name__ == '__main__':
	main()
