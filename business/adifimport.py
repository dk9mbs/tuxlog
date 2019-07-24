from services.converter.adif import AdifParser
from services.database.model import MetaDataExchangeFields
from services.database.model import LogLogs

class BusinessBaseContainer(object):
    _fn=list()

    def register(self, name):
        def wrapper(fn):
            self._fn.append({"name": name, "fn": fn})
            return fn
        return wrapper
    
    def __execute(self, name):
        for fn in self._fn:
            if fn['name']==name:
                fn()

class AdifParserContainer(BusinessBaseContainer):
    def adif_import_str(self, content):

        @AdifParser
        def inner_import(*args, **kwargs):
            print("<SOR>")
            adif_rec=args[0]

            log=LogLogs()

            for key in adif_rec:
                query=MetaDataExchangeFields.select().where((MetaDataExchangeFields.external_fieldname==key) 
                    & (MetaDataExchangeFields.internal_fieldname!='') 
                    & (MetaDataExchangeFields.internal_fieldname.is_null(False))
                    & (MetaDataExchangeFields.converter=='adif_v2')
                    )
                if len(list(query)) > 0:
                    for fld_def in query:
                        #print(key + " =>" + str(fld_def.internal_fieldname) + "=>" + adif_rec[key])
                        log.__dict__[fld_def.internal_fieldname]=adif_rec[key]
                self.__execute("test")

            log.mode_id=adif_rec['mode']
            log.logbook_id="dk9mbs"

            log.save()
            print("<EOR>")

            

        inner_import(content)
        pass