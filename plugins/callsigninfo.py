from playhouse.signals import post_save, pre_save
from model.model import LogLogs
import logging

logger = logging.getLogger(__name__)

def execute(sender, instance, created):
    print("pre_save hook")

    from usecases.hamcall.dxcallinfo import DxCallInfo

    prefix=DxCallInfo.get_dxinfo_by_call(instance.yourcall)

    if prefix==None:
        return

    instance.dxcc=prefix['main_prefix']
    instance.itu=prefix['itu_zone']
    instance.cq=prefix['cq_zone']
    instance.country=prefix['country']
    instance.entity=prefix['entity']


def execute_to_upper(sender, instance, created):
    instance.yourcall=str(instance.yourcall).upper()


def register():
    from playhouse.signals import pre_save
    from model.model import LogLogs
    pre_save.connect(execute, name='dxcallsigninfo', sender=LogLogs)
    pre_save.connect(execute_to_upper, name='plugin_callsign_to_upper', sender=LogLogs)