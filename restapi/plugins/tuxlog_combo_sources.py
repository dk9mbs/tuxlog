import datetime

from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log
from core.meta import read_table_meta

logger=log.create_logger(__name__)

def __validate(params):
    if 'input' not in params:
        return False

    return True

def execute(context, plugin_context, params):
    if not __validate(params):
        logger.warning(f"Missings params")
        return

    filter=""
    data=params['input']

    table_name=data['table_name']
    if 'filter' in data:
        filter=data['filter']

    meta=read_table_meta(context, table_name=table_name)

    if meta==None:
        log.create_logger(__name__).warning(f"Table {table_name} not found in meta data!")
        return

    id_fld=meta['id_field_name']
    desc_fld=meta['desc_field_name']

    fetch=f"""
    <restapi type="select">
        <table name="{table_name}"/>
        <select>
            <field name="{id_fld}" alias="id" />
            <field name="{desc_fld}" alias="name" />
        </select>
        {filter}
        <orderby>
            <field name="{desc_fld}" sort="ASC"/>
        </orderby>
    </restapi>
    """

    fetchparser=FetchXmlParser(fetch,context)
    rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)

    params['output']['data_source']=rs.get_result()
