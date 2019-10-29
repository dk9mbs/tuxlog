from model.model import LogBands
from decimal import Decimal

def get_band_by_frequency(frequency):
    band=LogBands.get_or_none( (LogBands.frequency_min <= Decimal(frequency)) & (Decimal(frequency) <= LogBands.frequency_max) )
    if band==None:
        return band
    
    return band
    