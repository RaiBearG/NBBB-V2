"""
Extracts latitude, longitude, sattelite count, and imu
data from sbp messages received back form the rover over
the radio link.

Send that data over the callback IP and  
""" 

from sbp.client.loggers.json_logger import JSONLogIterator
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
import csv, time, math, socket, pickle, serial
import numpy as np

SERIAL_BAUD_IN = 57600
SERIAL_BAUD_OUT = 115200
DEFAULT_UDP_ADDRESS = '127.0.0.1' 
DEFAULT_UDP_PORT = 13320 

#open udp port 
sock = socket.socket(socket.AF_INET,		#Internet
					 socket.SOCK_DGRAM)		# UDP

#open input serial link
ser_in = serial.Serial(
		port= '/dev/ttyUSB0',
		baudrate= SERIAL_BAUD_IN
		)

#open output serial link
ser_out = serial.Serial(
		port= '/dev/ttyUSB1',
		baudrate = SERIAL_BAUD_OUT
		)


def write_data(lat, lon, flag, sat, imu_x, imu_y):
	"""
	Package all the data and send it over the serial and
	loopback ip 
	"""
	data = lat, lon, flag, sat, imu_x, imu_y
	package= pickle.dumps(data)
	ser_out.write(package)
	sock.sendto(package, (address,port))
	return 

