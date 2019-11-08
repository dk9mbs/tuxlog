import re
from tuxlog.band import frequency_to_band
from common import BaseObject
from functools import wraps
from tuxlog.callsign.dxcallinfo import DxCallInfo

class ClusterSpot(BaseObject):
    def __init__(self, spot, frequency_unit="KHz", target_frequency_unit="MHz"):
        self.__spot=spot
        self.__frequency_unit=frequency_unit
        self.__target_frequency_unit=target_frequency_unit
        pass

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            fn('raw', self.__spot)
            callsign_pattern = "([a-z|0-9|/]+)"
            frequency_pattern = "([0-9|.]+)"
            pattern = re.compile("^DX de "+callsign_pattern+":\s+"+frequency_pattern \
                +"\s+"+callsign_pattern+"\s+(.*)\s+(\d{4}Z)", re.IGNORECASE)

            match = pattern.match(self.__spot)
            if match != None and len(match.regs) >= 6:
                spotter = match.group(1)
                frequency = float(match.group(2)) / 1000
                callsign = match.group(3)
                comment = match.group(4).strip()
                spot_time = match.group(5)
                band = frequency_to_band(frequency)

                spotter_call_info=DxCallInfo().get_dxinfo_by_call(spotter)
                call_info=DxCallInfo().get_dxinfo_by_call(callsign)

                spotter_prefix=None
                callsign_prefix=None

                if spotter_call_info!=None:
                    spotter_prefix=spotter_call_info['main_prefix']

                if call_info!=None:
                    callsign_prefix=call_info['main_prefix']

                json_spot={'spotter': spotter, 
                        'frequency': frequency, 
                        'callsign': callsign, 
                        'comment': comment,
                        'spot_time': spot_time,
                        'band': band.name,
                        'spotter_prefix': spotter_prefix,
                        'callsign_prefix': callsign_prefix}

                fn('dx', json_spot)

                return json_spot        
        return wrapper