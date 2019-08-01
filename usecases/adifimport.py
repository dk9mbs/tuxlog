from model.model import MetaDataExchangeFields
from model.model import LogLogs
from model.model import LogModes
from usecases.externalfieldmapping import ExternalFieldMapping
import peewee
import sys
import re

class BaseUseCase(object):
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

class AdifImportLogic(BaseUseCase):
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

            for adif_fld in adif_rec:
                fld_def=ExternalFieldMapping.map_to_internal(self._table_name,adif_fld)
                if fld_def!=None:
                    internal=str(fld_def.internal_fieldname).lower()
                    log.__data__[internal]=adif_rec[adif_fld]

            log.logbook_id=self._logbook_id

            self._execute('duplicate_search_%s' % self._table_name, model=log, logbook_id=self._logbook_id)
            self._execute('before_save_adif_rec', model=log, logbook_id=self._logbook_id)

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



class AdifParserLib:
    def __init__(self,fn):
        self.fn=fn
        pass

    def __call__(self, *args, **kwargs):
        adif_str=args[0]
        #do not assign adif_str to another value!!!  
        adif=adif_str.replace("\r", "")
        adif=adif_str.replace("\n", "")
        adif=adif_str.replace("\t", "")

        records=str(adif).split("<eoh>")
        records=str(records[1]).split("<eor>")
        adif_recs=list()

        for rec in records:
            adif_rec=self._extract_fields(rec)
            if len(adif_rec) >0:

                edit_adif_rec=self.fn(adif_rec, **kwargs)
                
                if edit_adif_rec != None:
                    adif_recs.append(edit_adif_rec)
                else:
                    adif_recs.append(adif_rec)

        return adif_recs

    def _extract_fields(self, adif_record):
        attr = re.findall(r"(.*?):(\d)>(.*?)\s(<.*?)", adif_record) 
        json={}         
        for m in attr:
            name=str(m[0]).replace("<","")
            value=m[2]
            json[name]=value  

        return json



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