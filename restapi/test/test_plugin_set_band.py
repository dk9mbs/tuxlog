import unittest

from core.database import CommandBuilderFactory
from core.database import FetchXmlParser
from config import CONFIG
from core.appinfo import AppInfo
from core.fetchxmlparser import FetchXmlParser
from core.plugin import Plugin
from services.database import DatabaseServices
from tuxlog_set_band import execute

class TestFetchxmlParser(unittest.TestCase):
    def setUp(self):
        AppInfo.init(__name__, CONFIG['default'])
        session_id=AppInfo.login("root","password")
        self.context=AppInfo.create_context(session_id)

    def test_20m(self):
        record={"frequency": {"value":"14.075"}}
        plugin_context=Plugin.create_context("log_logs","insert","before")
        execute(self.context,plugin_context, {"data": record})
        self.assertEqual(record['band_id']['value'], 90)

    def test_40m(self):
        record={"frequency": {"value":"7.075"}}
        plugin_context=Plugin.create_context("log_logs","insert","before")
        execute(self.context,plugin_context, {"data": record})
        self.assertEqual(record['band_id']['value'], 70)

    def test_no_band(self):
        record={"frequency": {"value":"0.075"}}
        plugin_context={"publisher":"log_logs", "trigger":"insert", "type":f"before","cancel":False }
        execute(self.context,plugin_context, {"data": record})
        self.assertEqual(record['band_id']['value'], None)

    def tearDown(self):
        AppInfo.save_context(self.context, True)
        AppInfo.logoff(self.context)


if __name__ == '__main__':
    unittest.main()
