from common.app import socketio
import logging
import time
import threading
from tuxlog.cluster import ClusterSpot
from model.model import LogDxclusters
from tuxlog.system.settungs import Setting

logger = logging.getLogger(__name__)

thread=None

def task():
    import telnetlib
    import re
    from common.app import socketio

    
    default_cluster_id=Setting.get_setting_value('*','default_dxcluster','1')

    cluster=LogDxclusters.get(LogDxclusters.id==default_cluster_id)
    if cluster==None:
        logger.info("No defalut DXCluster found!")
        return 

    tn = telnetlib.Telnet(cluster.host,cluster.port)

    '''
    query=LogDxclusterLoginscripts.select().where(LogDxclusterLoginscripts.dxcluster_id==cluster.id)
    for row in query:
        logger.info ('loginscript position %s' % row.position)
        
        if row.prompt != None:
            tn.read_until(str.encode(row.prompt))

        logger.info('sending to dxcluster => %s' % row.send)
        tn.write(str.encode(row.send+'\n'))
    '''

    tn.read_until(str.encode(cluster.prompt_username))
    tn.write(str.encode(cluster.username+'\n'))

    if cluster.prompt_password!=None:
        tn.read_until(str.encode(cluster.prompt_password))
        tn.write(str.encode(cluster.password+'\n'))

    tn.write(str.encode('SET/NAME %s\n' % Setting.get_setting_value('*','dxcluster_set_name','')  ))
    tn.write(str.encode('SET/QRA %s\n' % Setting.get_setting_value('*','dxcluster_set_qra','')  ))
    tn.write(str.encode('SET/QTH %s\n' % Setting.get_setting_value('*','dxcluster_set_qth','')  ))

    while (1):
        spot="".join(map(chr, tn.read_until(b'\n'))).replace('\n','').replace('\r','')
        
        @ClusterSpot(spot, "KHz", "MHz")
        def parse_spot(*args, **kwargs):
            spot_type=args[0]
            spot=args[1]

            if spot_type=='dx':
                socketio.emit('dxcluter_message', {})
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
