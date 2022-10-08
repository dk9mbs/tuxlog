import unittest

from core.database import CommandBuilderFactory
from core.database import FetchXmlParser
from config import CONFIG
from core.appinfo import AppInfo
from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from tuxlog_lib_cty import CtyImport
from services.fetchxml import build_fetchxml_by_alias
from core.plugin import Plugin, ProcessTools

class TestImportCtyDat(unittest.TestCase):
    def setUp(self):
        AppInfo.init(__name__, CONFIG['default'])
        session_id=AppInfo.login("root","password")
        self.context=AppInfo.create_context(session_id)

    def test_plugin(self):
        record={"yourcall": {"value": "dk9mbs"}}
        params={"data":record}

        #def create_context(publisher, trigger, type, event_handler_id, run_async, plugin_config, process_id, **kwargs):
        plugin_context=ProcessTools.create_context("log_logs","update","before",1,0,'{}',0)

        #execute(self.context,plugin_context,params)
        #self.assertEqual(params['data']['dxcc']['value'], "DL")

    def xtest_import(self):

        f=open('/tmp/cty.dat', 'r')
        content=f.read()
        f.close()

        imp=CtyImport(self.context, self.__after_read_country, self.__after_read_prefix)
        imp.parse(content)
        #self.assertEqual(params['output']['cq_zone'], 14)


    def __after_read_country(self, context, dxcc):
        print(dxcc)
        fetch=build_fetchxml_by_alias(context,"log_dxcc",dxcc['id'], None, type="select")
        fetchparser=FetchXmlParser(fetch, context)
        rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)
        if rs.get_result()==[]:
            fetch=build_fetchxml_by_alias(context,"log_dxcc",None, dxcc, type="insert")
            fetchparser=FetchXmlParser(fetch, context)
            rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)

    def __after_read_prefix(self, context, dxcc, dxcc_prefix):

        fetch=build_fetchxml_by_alias(context,"log_dxcc_prefixes",dxcc_prefix['id'], None, type="select")
        fetchparser=FetchXmlParser(fetch, context)
        rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)
        if rs.get_result()==[]:
            fetch=build_fetchxml_by_alias(context,"log_dxcc_prefixes",None, dxcc_prefix, type="insert")
            fetchparser=FetchXmlParser(fetch, context)
            DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)

    def tearDown(self):
        AppInfo.save_context(self.context, True)
        AppInfo.logoff(self.context)


if __name__ == '__main__':
    unittest.main()
