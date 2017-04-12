import serial
import time
import pickle


DEFAULT_COM_PORT = '/dev/ttyUSB0'
DEFAULT_BAUD_RATE = 115200

def get_args():
  """
  Get and parse arguments.
  """
  import argparse
  parser = argparse.ArgumentParser(description="NBBB Serial receive tool.")
  parser.add_argument("-p", "--port",
                      default=[DEFAULT_COM_PORT], nargs=1,
                      help="specify the serial port to use.")
  parser.add_argument("-b", "--baud-rate",
                      default=[DEFAULT_BAUD_RATE], nargs=1,
                      help="specify the baud rate for to use.")
  return parser.parse_args()



def main():
  """Simple Command line interface for receiving observations over UDP and repeating
     them over serial
  """
  args = get_args()
  baud = int(args.baud_rate[0])
  port = args.port[0]
  ser = serial.Serial(
    port=port,
    baudrate=baud
    )
  
  try:
    while True:
      data = ser.readline()
      if data:
        """data = pickle.load(data)
        print "***"
        print "Dist from center : %f" % data[0]
        print "Dist from start : %f" % data[1]
        if data[2] == 0:
          fix = "no fix"
        elif data[2] == 1:
          fix = "single point"
        elif data[2] == 2:
          fix = "DGPS"
        elif data[2] == 3:
          fix = "Float RTK"
        elif data[2] == 4:
          fix = "Fixed RTK" 

        print "Fix : %s  Sattelites : %d" % (fix, data[5])
        print "lat: %f  lon: %f" % (data[3], data[4])
        print "***"  """
        print data 
  except KeyboardInterrupt:
    pass 
  if ser.isopen():
    ser.close()
if __name__ == "__main__":
  main()
