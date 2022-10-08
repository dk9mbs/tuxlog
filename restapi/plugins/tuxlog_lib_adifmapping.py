
import sys
import re

class AdifMappingTools:
    def __init__(self):
        pass

    @staticmethod
    def map(adif_rec, mapping):
        result={}
        for k, v in adif_rec.items():
            field_name=AdifMappingTools.__map_field(k, mapping)
            if field_name != None:
                result[field_name]=v

        return result


    @staticmethod
    def __map_field(field_name, mappings):
        for mapping in mappings:
            if str(mapping['external_fieldname']).upper()==field_name.upper() and mapping['internal_fieldname'] != '':
                return mapping['internal_fieldname']

        return None
