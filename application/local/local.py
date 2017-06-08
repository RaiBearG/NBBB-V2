import socket, pickle, math

udp_address = "127.0.0.1"
udp_port = 13320

#m and b values of front yard found using tools/line_parameters.py
m = -0.0855672342
b = 38.6242134961
height = 50 #height of the device in ft 


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
	sock = socket.socket(socket.AF_INET,
											 socket.SOCK_DGRAM)
	sock.bind((udp_address,udp_port))

	try:
		while True:
			msg, addr = sock.recvfrom(1024)
			if msg:
				data = pickle.loads(msg)
				linepoint = find_point(m, b, data[1], data[0])
				dist = distance(data[0], data[1], linepoint[0], linepoint[1])
				if data[1]<linepoint[1]:
					dist = dist*-1

				#printing stuff
				print "***"
				print "Dist from center: %f inches" %  dist
				if data[2] == 0:
					fix = "no fix"
				elif data[2] == 1:
					fix = "single point"
				elif data[2] == 2:
					fix = "DGPS"
				elif data[2] == 3:
					fix = "Float RTK"
				elif data[2] == 4:
					fix = "fixed RTK"
				print "Fix : %s  Sattelites : %d" % (fix, data[3])
				print "lat: %f  lon: %f" % (data[0], data[1])
				print "***"	 	
	except KeyboardInterrupt:
			pass

if __name__ == '__main__':
	main()
