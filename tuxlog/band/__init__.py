from model.model import LogBands
from decimal import Decimal

def frequency_to_band(frequency):
    if frequency==None:
        return None

    band=LogBands.get_or_none( (LogBands.frequency_min <= Decimal(frequency)) & (Decimal(frequency) <= LogBands.frequency_max) )
    if band==None:
        return band
    
    return band
    