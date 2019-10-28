from playhouse.signals import post_save, pre_save
from model.model import LogLogs
import logging

logger = logging.getLogger(__name__)

def execute(sender, instance, created):
    #sender=params['sender']
    #instance=params['instance']
    #created=params['created']
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



def register():
    from playhouse.signals import pre_save
    from model.model import LogLogs
    #from usecases import app_hooks 
    #app_hooks.register('pre_save', execute)
    pre_save.connect(execute, name='dxcallsigninfo', sender=LogLogs)
