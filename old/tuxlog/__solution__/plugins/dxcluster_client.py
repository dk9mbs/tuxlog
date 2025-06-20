from common.app import socketio
import logging
import time
import threading
from tuxlog.cluster import ClusterSpot
from model.model import LogDxclusters
from tuxlog.system.settungs import Setting
import common.bgtask

logger = logging.getLogger(__name__)

def task():
    import telnetlib
    import re
    from common.app import socketio

    timeout_step=10
    timeout_period=120

    while (1):
        default_cluster_id=Setting.get_setting_value('*','default_dxcluster','1')

        cluster=LogDxclusters.get(LogDxclusters.id==default_cluster_id)
        if cluster==None:
            logger.info("No defalut DXCluster found!")
            return 

        tn = telnetlib.Telnet(cluster.host,cluster.port)

        tn.read_until(str.encode(cluster.prompt_username))
        tn.write(str.encode(cluster.username+'\n'))

        if cluster.prompt_password!=None:
            tn.read_until(str.encode(cluster.prompt_password))
            tn.write(str.encode(cluster.password+'\n'))

        tn.write(str.encode('SET/NAME %s\n' % Setting.get_setting_value('*','dxcluster_set_name','')  ))
        tn.write(str.encode('SET/QRA %s\n' % Setting.get_setting_value('*','dxcluster_set_qra','')  ))
        tn.write(str.encode('SET/QTH %s\n' % Setting.get_setting_value('*','dxcluster_set_qth','')  ))
        init=True
        timeout_count=0

        while (init):
            try:
                spot="".join(map(chr, tn.read_until(b'\n', timeout=timeout_step))).replace('\n','').replace('\r','')
                if spot != "":
                    timeout_count=0
                    @ClusterSpot(spot, "KHz", "MHz")
                    def parse_spot(*args, **kwargs):
                        spot_type=args[0]
                        spot=args[1]

                        if spot_type=='dx':
                            socketio.emit('dxcluter_message', {})
                        elif spot_type=='raw':
                            logger.info(spot)
                        else:
                            logger.info("-------")

                    parse_spot()
                else:
                    timeout_count+=timeout_step
                    logger.info('DXCluster spot timeout after %s secounds. Restart in %s seconds!' % (timeout_step, timeout_period-timeout_count))
                    if timeout_count>=timeout_period:
                        init=False
            except EOFError:
                logger.info('Timeout!')

        logger.info("Restart logon procedure!!!")

def register():
    thread=threading.Thread(target=task)
    thread.setName("Internal DX Cluster Client")
    common.bgtask.register(thread.name, thread)

