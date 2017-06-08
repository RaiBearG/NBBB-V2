# Copyright (C) 2015 Swift Navigation Inc.
# Contact: Fergus Noble <fergus@swiftnav.com>
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.

"""
the :mod:`sbp.client.examples.simple` module contains a basic example of
reading SBP messages from a serial port, decoding BASELINE_NED messages and
printing them out.
"""

from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.client.loggers.json_logger import JSONLogger
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
from sbp.imu import SBP_MSG_IMU_RAW, MsgImuRaw
import argparse, time

def main():
  parser = argparse.ArgumentParser(description="Swift Navigation SBP Example.")
  parser.add_argument("-p", "--port",
                      default=['/dev/ttyUSB2'], nargs=1,
                      help="specify the serial port to use.")
  args = parser.parse_args()

  start = time.time()
  pos = 0
  imu = 0

  # Open a connection to Piksi using the default baud rate (1Mbaud)
  with PySerialDriver(args.port[0], baud=115200) as driver:
    with Handler(Framer(driver.read, None, verbose=True)) as source:
      try:
        for msg, metadata in source:
        	diff = time.time()-start

        	if msg.msg_type == 2304:
        		imu = msg.acc_x
        	if msg.msg_type == 522:
        		pos = msg.lat, msg.lon, msg.flags, msg.n_sats, imu
        	if diff>2:
        		data = pos
        		print data
        		start = time.time()



      except KeyboardInterrupt:
        pass

if __name__ == "__main__":
  main()

