import logging
from playhouse.signals import post_save, pre_save
from model.model import LogLogs
from playhouse.signals import pre_save, post_save
from model.model import LogDxclusterSpots
from tuxlog.callsign.dxcallinfo import DxCallInfo
from tuxlog.band import frequency_to_band

logger = logging.getLogger(__name__)


def execute_pre(sender, instance, created):
    spotter_call_info=DxCallInfo().get_dxinfo_by_call(instance.spotter)
    callsign_info=DxCallInfo().get_dxinfo_by_call(instance.callsign)
    band = frequency_to_band(instance.frequency)

    instance.callsign_dxcc_prefix=callsign_info
    instance.spotter_dxcc_prefix=spotter_call_info
    instance.band=band
    pass

def execute_post(sender, instance, created):
    pass

def register():
    pre_save.connect(execute_pre, name='plugin_pre_save_dxcluster_spot', sender=LogDxclusterSpots)
    post_save.connect(execute_post, name='plugin_post_save_dxcluster_spot', sender=LogDxclusterSpots)