import logging
from playhouse.signals import post_save, pre_save
from model.model import LogLogs
from playhouse.signals import pre_save
from model.model import LogLogs

logger = logging.getLogger(__name__)


def execute(sender, instance, created):
    instance.yourcall=str(instance.yourcall).upper()


def register():
    pre_save.connect(execute, name='plugin_callsign_to_upper', sender=LogLogs)