import unittest
import config
import os
from model import model

class TestDxCallInfo(unittest.TestCase):

    def test_dxcallinfo(self):
        config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

        from usecases.hamcall.dxcallinfo import DxCallInfo
        from model.model import LogDxccPrefixes

        prefix=DxCallInfo.get_dxinfo_by_call("dk9mbs")
        print(prefix.dxcc.country)

        prefix=DxCallInfo.get_dxinfo_by_call("dl4ac")
        print(prefix.dxcc.country)

        prefix=DxCallInfo.get_dxinfo_by_call("EB1RJ")
        print(prefix.dxcc.country)

        prefix=DxCallInfo.get_dxinfo_by_call("OZ/EB1RJ/p")
        print(prefix.dxcc.country)

        prefix=DxCallInfo.get_dxinfo_by_call("ZS5ZLB/L ")
        print(prefix.dxcc.country)

        #result_fld_def=map.ext_to_int("notexists", field_mapping_list)
        #self.assertEqual(result_fld_def, None)

if __name__ == '__main__':
    unittest.main()

