import unittest

from core.database import CommandBuilderFactory
from core.database import FetchXmlParser
from config import CONFIG
from core.appinfo import AppInfo
from core.fetchxmlparser import FetchXmlParser
from core.plugin import Plugin
from services.database import DatabaseServices
from tuxlog_action_dxcc import execute

class TestFetchxmlParser(unittest.TestCase):
    def setUp(self):
        AppInfo.init(__name__, CONFIG['default'])
        session_id=AppInfo.login("root","password")
        self.context=AppInfo.create_context(session_id)

    def test_dl_call(self):
        record={"call": "dk9mbs"}
        params={"input":record, "output": {}}
        plugin_context=Plugin.create_context("tuxlog_get_dxcc_info","execute","before")
        execute(self.context,plugin_context,params)
        self.assertEqual(params['output']['dxcc'], "DL")
        self.assertEqual(params['output']['itu_zone'], 28)
        self.assertEqual(params['output']['cq_zone'], 14)

    def test_k_call(self):
        record={"call": "ag5zl"}
        params={"input":record, "output": {}}
        plugin_context=Plugin.create_context("tuxlog_get_dxcc_info","execute","before")
        execute(self.context,plugin_context,params)
        self.assertEqual(params['output']['dxcc'], "K")


    def tearDown(self):
        AppInfo.save_context(self.context, True)
        AppInfo.logoff(self.context)


if __name__ == '__main__':
    unittest.main()
