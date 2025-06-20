from model.model import LogLogs
from tuxlog.band import frequency_to_band
from playhouse.signals import pre_save


def execute(sender, instance, created):
    instance.band=frequency_to_band(instance.frequency)


def register():
    pre_save.connect(execute, name='set_band_plugin', sender=LogLogs)