import datetime

from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log

from dxcallinfo import DxCallInfo

logger=log.create_logger(__name__)

def __validate(params):
    if 'data' not in params:
        return False
    if 'yourcall' not in params['data']:
        return False

    return True

def execute(context, plugin_context, params):
    if not __validate(params):
        logger.warning(f"Missings params")
        return

    print (params)
    callsign=params['data']['yourcall']['value']
    now=datetime.datetime.now()

    info=DxCallInfo.get_dxinfo_by_call(context, callsign)
    params['data']['dxcc']={"value": None}
    if info==None:
        return

    params['data']['dxcc']['value']=info['dxcc_id']

