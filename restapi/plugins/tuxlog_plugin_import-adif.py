from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log

from tuxlog_lib_cty import CtyImport
from services.fetchxml import build_fetchxml_by_alias
from core.plugin import ProcessTools
from plugins.tuxlog_lib_adifparserlib import AdifParserLib
from core.file import File
from tuxlog_lib_adifmapping import AdifMappingTools

logger=log.create_logger(__name__)

def __validate(params):
    if 'data' not in params:
        return False

    if 'content' not in params['data']:
        return False

    return True

def execute(context, plugin_context, params):
    if not __validate(params):
        log.create_logger(__name__).warning(f"Missings params")
        return

    context.set_userdata('plugin_context', plugin_context)
    content=params['data']['content']

    connection=context.get_connection()

    fetch=f"""
    <restapi type="select">
    <table name="log_data_exchange_fields"/>
    <filter>
        <condition field="converter_id" operator="eq" value="adif_v2"/>
    </filter>
    </restapi>
    """
    fetchparser=FetchXmlParser(fetch,context)
    rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)

    mapping=rs.get_result()
    mapped_rec={}

    mapped_rec={}

    @AdifParserLib
    def parser(*args, **kwargs):
        mapped_rec=AdifMappingTools.map(args[0],mapping)

        ProcessTools.set_process_status_info(context, plugin_context, f"{args[0]}")

        fetch=build_fetchxml_by_alias(context,"log_logs",None, mapped_rec, type="insert")
        fetchparser=FetchXmlParser(fetch, context)
        DatabaseServices.exec(fetchparser,context,fetch_mode=0, run_as_system=True)

    parser( content, 0 )

    ProcessTools.set_process_status_info(context, plugin_context, f"Ready!")





