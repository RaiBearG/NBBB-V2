"""
Extracts latitude, longitude, sattelite count, and imu
data from sbp messages received back form the rover over
the radio link.

Send that data over the callback IP 
""" 

from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
from sbp.imu import SBP_MSG_IMU_RAW, MsgImuRaw
import time, socket, pickle

SERIAL_PORT_IN = '/dev/ttyAMA0'
SERIAL_BAUD_IN = 115200
DEFAULT_UDP_ADDRESS = '127.0.0.1' 
DEFAULT_UDP_PORT = 13320 

#open udp port 
sock = socket.socket(socket.AF_INET,		#Internet
					 socket.SOCK_DGRAM)		# UDP


def write_data(data):
	"""
	Package all the data and send it over the serial and
	loopback ip 
	"""
	print data
	package= pickle.dumps(data)
	#driver.write(data)
	sock.sendto(package, (DEFAULT_UDP_ADDRESS,DEFAULT_UDP_PORT))
	return 

def main():
	#start timer to control output flow
	start = time.time()

	# start data storage variables
	pos=0
	imu=0
	# open the serial port with handler and extract the messages wanted
	with PySerialDriver(SERIAL_PORT_IN, baud=SERIAL_BAUD_IN) as driver:
		with Handler(Framer(driver.read, None, verbose=True)) as source:
			try:
				for msg, metadata in source:
					diff = time.time()-start

					#store the imu data
					if msg.msg_type == 2304:
						imu = msg.acc_x
					#store the position data with latest imu at the end
					if msg.msg_type == 522 :
						pos = msg.lat, msg.lon, msg.flags, msg.n_sats, imu
					# write data to loopback ip at 0.5 hz
					if diff>2:
						write_data(pos)
						driver.write(pos)
						start = time.time()
			except KeyboardInterrupt:
				pass

if __name__ == '__main__':
	main()

