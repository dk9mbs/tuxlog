import unittest
from model.model import MetaDataExchangeFields
from model.model import MetaDataExchangeFields
from tuxlog.system.fieldmapping import FieldMapping
from tuxlog.file_import.adifimport import AdifParserLib

class TestAdifParser(unittest.TestCase):

    def test_fieldmapping(self):
        fld_def1=MetaDataExchangeFields()
        fld_def1.external_fieldname="call"
        fld_def1.internal_fieldname="yourcall"

        fld_def2=MetaDataExchangeFields()
        fld_def2.external_fieldname="band"
        fld_def2.internal_fieldname="band"

        fld_def3=MetaDataExchangeFields()
        fld_def3.external_fieldname="GRID"
        fld_def3.internal_fieldname="LOCATOR"

        field_mapping_list=list([fld_def1, fld_def2, fld_def3])

        map=FieldMapping()
        result_fld_def=map.ext_to_int("call", field_mapping_list)

        self.assertEqual(result_fld_def.internal_fieldname, 'yourcall')

        result_fld_def=map.ext_to_int("band", field_mapping_list)
        self.assertEqual(result_fld_def.internal_fieldname, 'band')

        result_fld_def=map.ext_to_int("grid", field_mapping_list)
        self.assertEqual(result_fld_def.internal_fieldname, 'locator')

        result_fld_def=map.ext_to_int("notexists", field_mapping_list)
        self.assertEqual(result_fld_def, None)

if __name__ == '__main__':
    unittest.main()

