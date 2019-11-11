from common.app import socketio
import logging
import time
import threading
from tuxlog.cluster import ClusterSpot
from model.model import LogDxclusters, LogDxclusterLoginscripts

logger = logging.getLogger(__name__)

thread=None

def task():
    import telnetlib
    import re
    from common.app import socketio

    cluster=LogDxclusters.get(LogDxclusters.position==0)
    if cluster==None:
        logger.info("No defalut DXCluster (position 0) found!")
        return 

    tn = telnetlib.Telnet(cluster.cluster_url,cluster.port)

    query=LogDxclusterLoginscripts.select().where(LogDxclusterLoginscripts.dxcluster_id==cluster.id)
    for row in query:
        logger.info ('loginscript position %s' % row.position)
        
        if row.prompt != None:
            tn.read_until(str.encode(row.prompt))

        logger.info('sending to dxcluster => %s' % row.send)
        tn.write(str.encode(row.send+'\n'))

    while (1):
        spot="".join(map(chr, tn.read_until(b'\n'))).replace('\n','').replace('\r','')
        
        @ClusterSpot(spot, "KHz", "MHz")
        def parse_spot(*args, **kwargs):
            spot_type=args[0]
            spot=args[1]

            if spot_type=='dx':
                #socketio.emit('dxcluster_message', spot)
                socketio.emit('dxcluter_message', {})
                print(spot)        
            elif spot_type=='raw':
                print(spot)
            else:
                print("-------")

        parse_spot()

def register():
    global thread

    if thread==None:
        thread=threading.Thread(target=task)
        thread.start()
        logger.info("started")
