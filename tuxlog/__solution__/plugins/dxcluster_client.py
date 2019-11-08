from common.app import socketio
import logging
import time
import threading
from tuxlog.cluster import ClusterSpot
logger = logging.getLogger(__name__)

thread=None

def task():
    import telnetlib
    import re
    from common.app import socketio

    tn = telnetlib.Telnet("la3waa.ddns.net",8000)
    #tn =telnetlib.Telnet("157.158.185.199", 9000)
    tn.read_until(b'login: ') 
    tn.write(b'DK9MBS \n')

    while (1):
        spot="".join(map(chr, tn.read_until(b'\n'))).replace('\n','').replace('\r','')
        
        @ClusterSpot(spot, "KHz", "MHz")
        def parse_spot(*args, **kwargs):
            spot_type=args[0]
            spot=args[1]

            if spot_type=='dx':
                socketio.emit('dxcluster_message', spot)
                print(spot)        
            elif spot_type=='raw':
                print(spot)
            else:
                print("-------")

        parse_spot()

def register():
    global thread

    #thread=socketio.start_background_task(task)
    thread=threading.Thread(target=task)
    thread.start()
    logger.info("started")
