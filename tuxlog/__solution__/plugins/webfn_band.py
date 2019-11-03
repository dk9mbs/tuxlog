from model.model import LogBands
from decimal import Decimal
from common import webfunction
from tuxlog.band import get_band_by_frequency

def execute(name, params, **kwargs):
    frequency=params['frequency']
    band=get_band_by_frequency(Decimal(frequency))

    return {
        "band": band.name
    }

def register():
    webfunction.register('band', execute)