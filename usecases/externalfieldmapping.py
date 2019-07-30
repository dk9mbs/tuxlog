#from services.converter.adif import AdifParserService
from model.model import MetaDataExchangeFields
from model.model import LogLogs
from model.model import LogModes
import peewee
import sys

class ExternalFieldMapping():
    _field_defs=dict()

    @classmethod 
    def _read_defs(cls, table_name):
        query=MetaDataExchangeFields.select().where((MetaDataExchangeFields.internal_fieldname!='') 
            & (MetaDataExchangeFields.internal_fieldname.is_null(False))
            & (MetaDataExchangeFields.converter=='adif_v2')
            )
        cls._field_defs[table_name]=list(query)
        

    @classmethod
    def map_to_internal(cls, table_name, adif_fld):
        adif_fld=adif_fld.lower()
        if not table_name in cls._field_defs:
            cls._read_defs(table_name)

        mapping_list=cls._field_defs[table_name]
        if len(mapping_list) == 0:
            return None

        for fld_def in mapping_list:
            external=str(fld_def.external_fieldname).lower()

            if external==str(adif_fld).lower():
                return fld_def
