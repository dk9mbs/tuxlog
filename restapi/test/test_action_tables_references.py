import unittest

from core.database import CommandBuilderFactory
from core.database import FetchXmlParser
from config import CONFIG
from core.appinfo import AppInfo
from core.fetchxmlparser import FetchXmlParser
from core.plugin import Plugin
from services.database import DatabaseServices
from tuxlog_combo_sources import execute

class TestFetchxmlParser(unittest.TestCase):
    def setUp(self):
        AppInfo.init(__name__, CONFIG['default'])
        session_id=AppInfo.login("root","password")
        self.context=AppInfo.create_context(session_id)

    def test_combo_source(self):
        params={"table_name": "log_logbooks", "filter":"""<filter type="and"><condition field="id" operator="neq" value="*"/> </filter>"""}
        plugin_context=Plugin.create_context("generate_data_combo_source","execute","before")
        print(execute(self.context,plugin_context, {"data": params}))

    def tearDown(self):
        AppInfo.save_context(self.context, True)
        AppInfo.logoff(self.context)


if __name__ == '__main__':
    unittest.main()
