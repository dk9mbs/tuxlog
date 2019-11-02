from usecases.tuxlog import callbook
import logging
import json
from usecases.tuxlog import webfunction

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
