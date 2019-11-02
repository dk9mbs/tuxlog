from model.model import LogLogs
from usecases.tuxlog.band import get_band_by_frequency
from playhouse.signals import pre_save


def execute(sender, instance, created):
    instance.band=get_band_by_frequency(instance.frequency)


def register():
    pre_save.connect(execute, name='set_band_plugin', sender=LogLogs)