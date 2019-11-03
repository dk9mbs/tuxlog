from playhouse.signals import post_save, pre_save
from model.model import LogLogs
import logging
from playhouse.signals import pre_save
from model.model import LogLogs
from tuxlog.callsign.dxcallinfo import DxCallInfo

logger = logging.getLogger(__name__)

def execute(sender, instance, created):
    print("pre_save hook")

    prefix=DxCallInfo.get_dxinfo_by_call(instance.yourcall)

    if prefix==None:
        return

    instance.dxcc=prefix['main_prefix']
    instance.itu=prefix['itu_zone']
    instance.cq=prefix['cq_zone']
    instance.country=prefix['country']
    instance.entity=prefix['entity']

def register():
    pre_save.connect(execute, name='dxcallsigninfo', sender=LogLogs)
