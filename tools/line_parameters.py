"""
Use all position points in a log file to create a best 
line and output the m and b of its equation
y=mx+b
"""


from sbp.client.loggers.json_logger import JSONLogIterator
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
import csv, time, math, socket, pickle, serial
import numpy as np

def collect_data(logfile):
	"""
	open csv file and collect all pos llh dat in an array
	"""
	print ("collecting reference data ...")
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
						#msg_flag.append(msg.flags)
						#length += 1		

				except StopIteration:
					#print length
					return msg_lat, msg_long


def get_args():
  """
  Get and parse arguments.
  """
  import argparse
  parser = argparse.ArgumentParser(description='MetaData xml creator')
  parser.add_argument('-f', '--filename',
                      default=[None], nargs=1,
                      help="The SBP log file to extract data from.")
  args = parser.parse_args()
  return args

def main():
	args = get_args()
	lat, lon = collect_data(args.filename[0])
	fit = np.polyfit(lon, lat, 1)
	print('m = %.10f  b = %.10f') %(fit[0], fit[1])

if __name__ == '__main__':
	main()	
