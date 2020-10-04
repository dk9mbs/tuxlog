import datetime

from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log

from dxcallinfo import DxCallInfo

logger=log.create_logger(__name__)

def __validate(params):
    if 'input' not in params:
        return False
    if 'call' not in params['input']:
        return False

    return True

def execute(context, plugin_context, params):
    if not __validate(params):
        logger.warning(f"Missings params")
        return

    callsign=params['input']['call']

    info=DxCallInfo.get_dxinfo_by_call(context, callsign)
    params['output']['dxcc']=None
    params['output']['cq_zone']=None
    params['output']['itu_zone']=None
    if info==None:
        return

    params['output']['dxcc']=info['dxcc_id']
    params['output']['itu_zone']=info['itu_zone']
    params['output']['cq_zone']=info['cq_zone']

