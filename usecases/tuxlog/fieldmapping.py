from model.model import MetaDataExchangeFields
from model.model import LogLogs
from model.model import LogModes
import peewee
import sys

class FieldMapping():
    _field_defs=dict()

    @classmethod 
    def read_mappings_from_db(cls, table_name):
        if table_name in cls._field_defs:
            return cls._field_defs[table_name]

        query=MetaDataExchangeFields.select().where((MetaDataExchangeFields.internal_fieldname!='') 
            & (MetaDataExchangeFields.internal_fieldname.is_null(False))
            & (MetaDataExchangeFields.converter=='adif_v2')
            )
        cls._field_defs[table_name]=list(query)
        return list(query)


    @classmethod
    def ext_to_int(cls, external_fieldname, field_mapping_list):
        external_fieldname=external_fieldname.lower()

        if len(field_mapping_list) == 0:
            return None

        for fld_def in field_mapping_list:
            external=str(fld_def.external_fieldname).lower()

            if external==str(external_fieldname).lower():
                fld_def.internal_fieldname=fld_def.internal_fieldname.lower()
                return fld_def
