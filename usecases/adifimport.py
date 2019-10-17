from model.model import MetaDataExchangeFields
from model.model import LogLogs
from model.model import LogModes, LogImportlogs
from usecases.fieldmapping import FieldMapping
from services.adifimport import AdifParserLib
from common.common import BaseUseCase

import peewee
import sys
import re


class AdifImport(BaseUseCase):
    _logbook_id=""
    _table_name=""

    def __init__(self, table_name, loogbook_id):
        self._table_name=table_name
        self._logbook_id=loogbook_id
        pass

    def adif_import(self, content):

        @AdifParserLib
        def inner_import(*args, **kwargs):
            adif_rec=args[0]

            log=LogLogs()

            import_log=LogImportlogs()
            import_log.internal_record=adif_rec
            import_log.external_record=args[1]
            import_log.save(force_insert=True)

            for adif_fld in adif_rec:
                
                fld_def=FieldMapping.ext_to_int(adif_fld, 
                    FieldMapping.read_mappings_from_db(self._table_name))

                if fld_def!=None:
                    internal=str(fld_def.internal_fieldname).lower()
                    #print(internal)
                    if internal.endswith('_id'):
                        internal=internal[:-3]

                    if internal=='start_utc' and (len(adif_rec[adif_fld])==4):
                        adif_rec[adif_fld]=adif_rec[adif_fld]+"00"

                    if fld_def.internal_datatype=='Number':
                        adif_rec[adif_fld]=re.sub('[^0-9]','', adif_rec[adif_fld])
                    
                    if fld_def.internal_datatype=='Boolean':
                        if str(adif_rec[adif_fld]).strip()=='N':
                            adif_rec[adif_fld]=0
                        if str(adif_rec[adif_fld]).strip()=='Y':
                            adif_rec[adif_fld]=1

                    log.__data__[internal]=adif_rec[adif_fld]

            log.logbook_id=self._logbook_id



            self._execute('duplicate_search_%s' % self._table_name, model=log, logbook_id=self._logbook_id)
            self._execute('before_save_adif_rec', model=log, logbook_id=self._logbook_id)

            try:
                if log.id==None:
                    log.save()
                import_log.log=log.id
                import_log.statuscode=10
                import_log.save(force_insert=False)
                self._execute("after_save_adif_rec", adif_rec=log)
            except peewee.IntegrityError as err:
                self._execute("error_save_adif_rec", adif_rec=log, error_desc=str(err))
                print('peewee.IntegrityError:%s' % str(err))
            except:
                self._execute("error_save_adif_rec", adif_rec=log)
                print("Unexpected error:", sys.exc_info()[0])

            

        inner_import(content)
        pass



if __name__ == "__main__":
    
    f = open("/tmp/wsjtx_log.adi", "r")
    content=f.read()

    @AdifParserLib
    def test(*args, **kwargs):
        print("Test => " + str(args[0]))

    test(content)

    #f = open("c:\\temp\\wsjtx_log.adi", "r")
    #content=f.read()
    #parser=AdifParser2()
    #@parser.parse("")
    #def test(*args, **kwargs):
    #    print(type(*args))
    #    print (*args, **kwargs)
        
    #test(content)
