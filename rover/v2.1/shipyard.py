"""
Extract MSG_POS_LLH data from a JSON log file and write to a
csv.
"""

from sbp.client.loggers.json_logger import JSONLogIterator
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
import csv, time, math, socket, pickle, serial
import numpy as np

SERIAL_BAUD = 1000000 
DEFAULT_UDP_ADDRESS = '10.3.33.86' 
DEFAULT_UDP_PORT = 13320 

def collect_data(logfile):
	"""
	open csv file and collect all pos llh dat in an array
	"""
	print ("collecting reference data")
	with open(logfile, 'r') as infile:
		with JSONLogIterator(infile) as log:
			log = log.next()

			msg_lat = []
			msg_long = []
			msg_flag = []
			length = 0

			while True:
				try:
					msg, metadata = log.next()

					#collect data
					if msg.__class__.__name__ == "MsgPosLLH":
						msg_lat.append(msg.lat)
						msg_long.append(msg.lon)
						msg_flag.append(msg.flags)
						length += 1		

				except StopIteration:
					print length
					return msg_lat, msg_long, msg_flag, length

def write_data(msg_lat, msg_long, msg_flag, length, writefile):
	"""
	Write arrays of data to a csv
	"""
	print ("writing reference data")
	fout = open(writefile, 'wt')
	writer = csv.writer(fout)
	writer.writerow(("Latitude", "Longitude", "Flag"))

	itt = 0
	while itt < length:
		writer.writerow((msg_lat[itt], msg_long[itt], msg_flag[itt]))
		itt += 1
	return

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
	coordinates in incles
	"""
	dlong = (lon2 - lon1) * math.pi / 180.0
	dlat = (lat2 - lat1) * math.pi / 180.0
	a = pow(math.sin(dlat/2.0), 2) + math.cos(lat1*math.pi/180.0) * math.cos(lat2*math.pi/180.0) * pow(math.sin(dlong/2.0),2)
	c =  2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	#convert distance it inches
	d = 6367 * c * 39370.07874016

	return d



def get_args():
  """
  Get and parse arguments.
  """
  import argparse
  parser = argparse.ArgumentParser(description='MetaData xml creator')
  parser.add_argument('-f', '--filename',
                      default=[None], nargs=1,
                      help="The SBP log file to extract data from.")
  parser.add_argument('-o', '--outfile',
                      default=["output.csv"], nargs=1,
                      help='specify the name of the CSV file output.')
  parser.add_argument("-p", "--port",
                      default=None, nargs=1,
                      help="specify the serial port to use.")
  parser.add_argument("-b", "--baud",
                      default=[SERIAL_BAUD] ,
                      help="specify the baud rate to use.")
  parser.add_argument("-a", "--address",
                      default=[DEFAULT_UDP_ADDRESS]  , nargs=1,
                      help="specify the UDP IP Address to use.")
  parser.add_argument("-u", "--udp-port",
                      default=[DEFAULT_UDP_PORT] , nargs=1,
                      help="specify the UDP Port to use.")
  args = parser.parse_args()
  return args


def main():
	args = get_args()
	lat, lon, flag, length = collect_data(args.filename[0])
	write_data(lat, lon, flag, length, args.outfile[0])
	
	#find m and b values for reference ine
	fit = np.polyfit(lon, lat, 1)
	print ("got reference line")
	
	#open udp socket 
	port = int(args.udp_port[0])
  	address = args.address[0]
  	sock = socket.socket(socket.AF_INET,    # Internet
                      	 socket.SOCK_DGRAM) # UDP

  	#start output serial
  	ser = serial.Serial(
  		port = '/dev/ttyAMA0',
  		baudrate = 115200
  		)
	
	# reference time to send data at 0.5 hz. regular speed not needed
	start = time.time()
	# Open a connection to Piksi using the default baud rate (1Mbaud)
	with PySerialDriver(args.port[0], args.baud[0]) as driver:
		with Handler(Framer(driver.read, None, verbose=True)) as source:
	    		try:
		        	for msg, metadata in source.filter(SBP_MSG_POS_LLH):
			          	diff = time.time()-start

			          	if diff>2:
			          		# Find distance from reference
			          		linepoint = find_point(fit[0], fit[1], msg.lon, msg.lat)
			          		dist = distance(msg.lat, msg.lon, linepoint[0], linepoint[1])
			          		# add a -ve sign if the point is on left of line
			          		if msg.lon<linepoint[1]:
								dist = dist*-1
			          		#find distance of shop from beginnign of ramp
			          		dist2 = distance(48.015530027273954, -122.53999350346919, msg.lat, msg.lon)
			          		#add a -ve if the ship is on the other side of the yard
			          		if msg.lat<48.015519022615955:
			          			dist2 = dist2*-1
			          		
			          		#compile all the data in a array and send a string of data. 
			          		data = dist, dist2, msg.flags, msg.lat, msg.lon, msg.n_sats
			          		package = pickle.dumps(data)
							
			          		print data
			          		ser.write(package)
			          		sock.sendto(package, (address,port))
			          		start = time.time()
			          	else : 
			          		#dump all data which is not sent on the 0.5 hz clock
			          		dump = msg
			          		dump2 = metadata	
			          	#time.sleep(1)
		      	except KeyboardInterrupt:
		        	pass
	        	

if __name__== '__main__':
	main()
