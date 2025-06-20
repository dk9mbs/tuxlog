from model.model import LogBands
from decimal import Decimal
from common import webfunction
from tuxlog.band import frequency_to_band

def execute(name, params, **kwargs):
    frequency=params['frequency']
    band=frequency_to_band(Decimal(frequency))

    return {
        "band": band.name
    }

def register():
    webfunction.register('band', execute)