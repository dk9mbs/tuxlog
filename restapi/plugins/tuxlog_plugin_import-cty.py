from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log

from tuxlog_lib_cty import CtyImport
from services.fetchxml import build_fetchxml_by_alias
from core.plugin import ProcessTools

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
    imp=CtyImport(context, __after_read_country, __after_read_prefix)
    imp.parse(content)
    ProcessTools.set_process_status_info(context, plugin_context, f"Ready!")



def __after_read_country(context, dxcc):
    plugin_context=context.get_userdata('plugin_context')

    ProcessTools.set_process_status_info(context, plugin_context, f"Importing {dxcc['country']}")

    fetch=build_fetchxml_by_alias(context,"log_dxcc",dxcc['id'], None, type="select")
    fetchparser=FetchXmlParser(fetch, context)
    rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)
    if rs.get_result()==[]:
        fetch=build_fetchxml_by_alias(context,"log_dxcc",None, dxcc, type="insert")
        fetchparser=FetchXmlParser(fetch, context)
        rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)

def __after_read_prefix(context, dxcc, dxcc_prefix):

    fetch=build_fetchxml_by_alias(context,"log_dxcc_prefixes",dxcc_prefix['id'], None, type="select")
    fetchparser=FetchXmlParser(fetch, context)
    rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)
    if rs.get_result()==[]:
        fetch=build_fetchxml_by_alias(context,"log_dxcc_prefixes",None, dxcc_prefix, type="insert")
        fetchparser=FetchXmlParser(fetch, context)
        DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)


