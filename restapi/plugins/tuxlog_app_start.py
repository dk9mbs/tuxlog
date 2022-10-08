from core import log
from core.appinfo import AppInfo
import tuxlog_endpoint_adif
import tuxlog_endpoint_cty

logger=log.create_logger(__name__)

def execute(context, plugin_context, params):
    AppInfo.get_api("api").add_resource(tuxlog_endpoint_adif.get_endpoint(), "/v1.0/tuxlog/adif", methods=['POST'])
    logger.info("Init tuxlog Adif endpoint done!")
    AppInfo.get_api("api").add_resource(tuxlog_endpoint_cty.get_endpoint(), "/v1.0/tuxlog/cty", methods=['POST'])
    logger.info("Init tuxlog cty endpoint done!")
