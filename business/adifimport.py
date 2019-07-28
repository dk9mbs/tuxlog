from services.converter.adif import AdifParserService
from services.database.model import MetaDataExchangeFields
from services.database.model import LogLogs
from services.database.model import LogModes
import peewee
import sys

class BusinessBaseContainer(object):
    _fn=list()

    def register(self, name):
        def wrapper(fn):
            self._fn.append({"name": name, "fn": fn})
            return fn
        return wrapper
    
    def _execute(self, name, **kwargs):
        for fn in self._fn:
            if fn['name']==name:
                fn['fn'](**kwargs)

class AdifImportLogic(BusinessBaseContainer):
    _logbook_id=""
    _table_name=""

    def __init__(self, table_name, loogbook_id):
        self._table_name=table_name
        self._logbook_id=loogbook_id
        pass

    def adif_import(self, content):

        @AdifParserService
        def inner_import(*args, **kwargs):
            adif_rec=args[0]

            log=LogLogs()

            query=MetaDataExchangeFields.select().where((MetaDataExchangeFields.internal_fieldname!='') 
                & (MetaDataExchangeFields.internal_fieldname.is_null(False))
                & (MetaDataExchangeFields.converter=='adif_v2')
                )

            if len(list(query)) == 0:
                self._execute("nomapping")
                return None


            for adif_fld in adif_rec:
                for fld_def in query:
                    external=str(fld_def.external_fieldname).lower()
                    internal=str(fld_def.internal_fieldname).lower()

                    if external==str(adif_fld).lower():
                        log.__data__[internal]=adif_rec[adif_fld]
                        pass

            log.logbook_id=self._logbook_id

            #print(log.__data__)

            log_exists=LogLogs.get_or_none((LogLogs.logbook==self._logbook_id) 
                & (LogLogs.yourcall==log.yourcall)
                & (LogLogs.mode==log.mode_id)
                & (LogLogs.logdate_utc==log.logdate_utc)
                & (LogLogs.start_utc==log.start_utc)
            )

            if log_exists != None:
                print('Found duplicate logentry => %s' % log_exists.id)
                log.id=log_exists.id

            try:
                log.save()
                self._execute("after_save_adif_rec", adif_rec=log)
            except peewee.IntegrityError as err:
                self._execute("error_save_adif_rec", adif_rec=log, error_desc=str(err))
                print('peewee.IntegrityError:%s' % str(err))
            except:
                self._execute("error_save_adif_rec", adif_rec=log)
                print("Unexpected error:", sys.exc_info()[0])

            

        inner_import(content)
        pass