import logging
import json
from tuxlog.system import webfunction
from tuxlog.callsign import callbook

logger = logging.getLogger(__name__)

def execute(name, params, **kwargs):
    provider=params['provider']
    call=params['callsign']

    result=callbook.init_haminfo_dict()
    callbook.HamInfoProviderFactory.create(provider).read(call, result)
    logger.info('HamInfo => %s' % str(result))
    return result


def register():
    webfunction.register('callbook', execute)
