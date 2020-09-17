import datetime

from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log

def __validate(params):
    if 'data' not in params:
        return False
    if 'frequency' not in params['data']:
        return False

    return True

def execute(context, plugin_context, params):
    if not __validate(params):
        log.create_logger(__name__).warning(f"Missings params")
        return

    if 'band_id' in params['data']:
        log.create_logger(__name__).warning(f"band already set!")
        return

    params['data']['band_id']={"value":None}
    value=params['data']['frequency']['value']

    fetch=f"""
    <restapi type="select">
        <table name="log_bands"/>
        <filter>
            <condition field="frequency_min" operator="leq" value="{value}"/>
            <condition field="frequency_max" operator="geq" value="{value}"/>
        </filter>
    </restapi>
    """
    fetchparser=FetchXmlParser(fetch,context)
    rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)

    if rs.get_result()==None or len(rs.get_result()) == 0:
        #raise NameError(f"band not found {value}")
        log.create_logger(__name__).warning(f"Band not found {value}")
        return

    params['data']['band_id']['value']=rs.get_result()[0]['id']
