from usecases.tuxlog import webfunction
import json
from usecases.tuxlog.dxcallinfo import DxCallInfo
from model.model import LogDxccPrefixes

def execute(name, params, **kwargs):

    callsign=params['callsign']
    prefix=DxCallInfo.get_dxinfo_by_call(callsign)

    return {
        "main_prefix": prefix['main_prefix'],
        "itu": prefix['itu_zone'],
        "cq": prefix['cq_zone'],
        "country": prefix['country'],
        "entity": prefix['entity']
    }


def register():
    webfunction.register('callsigninfo', execute)