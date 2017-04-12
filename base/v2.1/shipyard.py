import socket
import time
import pickle


DEFAULT_UDP_ADDRESS = "127.0.0.1"
DEFAULT_UDP_PORT = 13320

def get_args():
  """
  Get and parse arguments.
  """
  import argparse
  parser = argparse.ArgumentParser(description="Swift Navigation UDP Receive tool.")
  parser.add_argument("-a", "--address",
                      default=[DEFAULT_UDP_ADDRESS], nargs=1,
                      help="specify the UDP IP Address to use.")
  parser.add_argument("-p", "--udp-port",
                      default=[DEFAULT_UDP_PORT], nargs=1,
                      help="specify the UDP Port to use.")
  return parser.parse_args()



def main():
  """Simple Command line interface for receiving observations over UDP and repeating
     them over serial
  """
  args = get_args()
  port = int(args.udp_port[0])
  address = args.address[0]
  sock = socket.socket(socket.AF_INET,    # Internet
                       socket.SOCK_DGRAM) # UDP
  sock.bind((address, port))
  
  try:
    while True:
      data, addr = sock.recvfrom(1024)
      if data:
        data = pickle.loads(data)
        print "***"
        print "Dist from center : %f inches" % data[0]
        print "Dist from start : %f feet" % (data[1]/12)
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
        print "***"  

  except KeyboardInterrupt:
    pass 
  if ser.isopen():
    ser.close()
if __name__ == "__main__":
  main()
