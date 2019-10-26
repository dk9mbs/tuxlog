from playhouse.signals import post_save, pre_save
from model.model import LogLogs
import logging

logger = logging.getLogger(__name__)

def execute(name, params, **kwargs):
    sender=params['sender']
    instance=params['instance']
    created=params['created']
    print("pre_save hook")

    from usecases.hamcall.dxcallinfo import DxCallInfo

    prefix=DxCallInfo.get_dxinfo_by_call(instance.yourcall)

    if prefix==None:
        return

    instance.dxcc=prefix['prefix']
    instance.itu=prefix['itu_zone']
    instance.cq=prefix['cq_zone']
    instance.country=prefix['country']
    instance.entity=prefix['entity']



def register():
    from usecases.hook_main import hook
    hook.register('pre_save', execute)