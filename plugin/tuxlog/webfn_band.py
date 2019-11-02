from usecases.tuxlog.band import get_band_by_frequency
from model.model import LogBands
from decimal import Decimal
from usecases.tuxlog import webfunction


def execute(name, params, **kwargs):
    frequency=params['frequency']
    band=get_band_by_frequency(Decimal(frequency))

    return {
        "band": band.name
    }

def register():
    webfunction.register('band', execute)