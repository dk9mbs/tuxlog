from usecases import webfunction
import json

def execute(name, params, **kwargs):
    from usecases.hamcall.dxcallinfo import DxCallInfo
    from model.model import LogDxccPrefixes

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