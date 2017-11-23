import argparse
import math
import signal
import sys
import _utils

from _utils import RingBuffer

from pythonosc import dispatcher
from pythonosc import osc_server, udp_client


def acc_handler(unused_addr, args, args2, args3):
    print("unused_addr: {0} Acc values <{1} {2} {3}>".format(unused_addr,args,args2,args3))
    client.send_message("/dumdiduu", args)

# Another way to access several arguments:  
 
# With dummy code on how to play around with buffers
 
def acc_handler2(unused_addr, *args):
    global Acc_X_Buf
    global Acc_Y_Buf
    global Acc_Z_Buf
    
    Acc_X_Buf.extend(args[0])
    Acc_Y_Buf.extend(args[1])
    Acc_Z_Buf.extend(args[2])
    
    if Acc_X_Buf.get_index() % 10 == 0:
        if Acc_X_Buf.get_last_n(10).mean() > 0:
            print("forward!")
        else:
            print("backward!")
            
    if Acc_Y_Buf.get_index() % 10 == 0:     
        if Acc_Y_Buf.get_last_n(10).mean() > 0:
            print("Left!")
        else:
            print("Right!")
        

def alpha_handler(unused_addr, *args):
    global rBuf
   # print("The total alpha is {0} and rbufsize is {1}".format(args[0]+args[1]+args[2]+args[3],rBuf.get_index()))
    
    rBuf.extend(args[0])
    if rBuf.get_index() % 10 == 0:
        print("average alpha for last 5 values is {0}".format(rBuf.get_last_n(5).mean()))
        print("the rbuf is {0}".format(rBuf.get()))
    
    
dispatcher = dispatcher.Dispatcher()

dispatcher.map("/muse/acc", acc_handler2)
#dispatcher.map("/muse/elements/alpha_absolute", alpha_handler)
#dispatcher.map("*", default_handler)   ## BAD IDEA

## To fix the Address already in use problem
# if you quit the server without closing the port
# the port stays open and you cannot restart again with the same
# port number.. with the fix below you can close this script with ctrl+c
# and the server should close smoothly..

def signal_handler(signal, frame):
    print("Trying to close the socket gracefully...")
    global server
    server.server_close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

Acc_X_Buf = RingBuffer(100)
Acc_Y_Buf = RingBuffer(100)
Acc_Z_Buf = RingBuffer(100)

#client = udp_client.SimpleUDPClient("127.0.0.1", 9006)
server = osc_server.ThreadingOSCUDPServer(
  ("127.0.0.1", 5015), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

    