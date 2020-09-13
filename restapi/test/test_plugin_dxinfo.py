import unittest

from core.database import CommandBuilderFactory
from core.database import FetchXmlParser
from config import CONFIG
from core.appinfo import AppInfo
from dxcallinfo import DxCallInfo

class TestDxCallInfo(unittest.TestCase):
    def setUp(self):
        AppInfo.init(__name__, CONFIG['default'])
        session_id=AppInfo.login("root","password")
        self.context=AppInfo.create_context(session_id)

    def test_dxcall_dl(self):
        info=DxCallInfo.get_dxinfo_by_call(self.context, "DK9MBS")
        self.assertEqual(info['dxcc_id'].upper(), "DL")

        info=DxCallInfo.get_dxinfo_by_call(self.context, "DL4AC")
        self.assertEqual(info['dxcc_id'].upper(), "DL")

    def test_dxcall_dl_with_pre_and_post(self):
        info=DxCallInfo.get_dxinfo_by_call(self.context, "oz/DK9MBS/p")
        self.assertEqual(info['dxcc_id'].upper(), "OZ")

    def test_dxcall_us(self):
        info=DxCallInfo.get_dxinfo_by_call(self.context, "AG5ZL")
        self.assertEqual(info['dxcc_id'].upper(), "K")

    def test_dxcall_unknown(self):
        info=DxCallInfo.get_dxinfo_by_call(self.context, "XXXXXXXXXX")
        self.assertEqual(info, None)

    def tearDown(self):
        AppInfo.save_context(self.context, True)
        AppInfo.logoff(self.context)


if __name__ == '__main__':
    unittest.main()
