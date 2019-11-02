import unittest
import config
import os
from model import model
from usecases.tuxlog.dxcallinfo import DxCallInfo
from model.model import LogDxccPrefixes

class TestDxCallInfo(unittest.TestCase):

    def test_dxcallinfo(self):
        config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

        prefix=DxCallInfo.get_dxinfo_by_call("dk9mbs")
        self.assertEqual(prefix['main_prefix'] , 'DL')
        
        prefix=DxCallInfo.get_dxinfo_by_call("dl4ac")
        self.assertEqual(prefix['main_prefix'], 'DL')

        prefix=DxCallInfo.get_dxinfo_by_call("EB1RJ")
        self.assertEqual(prefix['main_prefix'], 'EA')

        prefix=DxCallInfo.get_dxinfo_by_call("OZ/EB1RJ/p")
        self.assertEqual(prefix['main_prefix'], 'OZ')

        prefix=DxCallInfo.get_dxinfo_by_call("ZS5ZLB/L ")
        self.assertEqual(prefix['main_prefix'], 'ZS')

        prefix=DxCallInfo.get_dxinfo_by_call(" oz-dl4ay-p")
        self.assertEqual(prefix['main_prefix'], 'OZ')


if __name__ == '__main__':
    unittest.main()

