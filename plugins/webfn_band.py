

def execute(name, params, **kwargs):
    from usecases.band import get_band_by_frequency
    from model.model import LogBands
    from decimal import Decimal

    frequency=params['frequency']
    band=get_band_by_frequency(Decimal(frequency))

    return {
        "band": band.name
    }

def register():
    from usecases import webfunction
    webfunction.register('band', execute)