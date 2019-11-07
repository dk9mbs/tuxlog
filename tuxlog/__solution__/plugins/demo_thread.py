from common.app import socketio
import logging
import time
import threading

logger = logging.getLogger(__name__)

thread=None

def task():
    #import socket

    #HOST = 'la3waa.ddns.net'  # The server's hostname or IP address
    #PORT = 8000        # The port used by the server

    #s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((HOST, PORT))

    #while True:
     #   dataarray = s.recv(1024)
     #   data="".join(map(chr,dataarray)).split('\n')
     #   for line in data:
     #       line=line.replace('\n','').replace('\r','')
     #       if line != '':
     #           print (line)
     #           if line=='login: ':
     #               s.send(b'DK9MBS \n')

    import telnetlib
    import re
    from common.app import socketio

    tn = telnetlib.Telnet("la3waa.ddns.net",8000)
    tn.read_until(b'login: ') 
    tn.write(b'DK9MBS \n')

    while (1):
        telnet_output="".join(map(chr, tn.read_until(b'\n'))).replace('\n','').replace('\r','')
        socketio.emit('dxcluster_message', telnet_output)
        print(telnet_output)
        #match = pattern.match(telnet_output)

        # If there is a match, sort matches into variables
        #if match:
        #    spotter = match.group(1)
        #    frequency = float(match.group(2))
        #    spotted = match.group(3)
        #    comment = match.group(4).strip()
        #    spot_time = match.group(5)
            #band = frequency_to_band(frequency)
        

def register():
    global thread

    #thread=socketio.start_background_task(task)
    thread=threading.Thread(target=task)
    thread.start()
    logger.info("started")
