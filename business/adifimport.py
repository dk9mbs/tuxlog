from services.converter.adif import AdifParser
from services.database.model import MetaDataExchangeFields
from services.database.model import LogLogs

def adif_import_str(content):

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


        log.mode_id=adif_rec['mode']
        log.logbook_id="dk9mbs"

        log.save()
        print("<EOR>")

        

    inner_import(content)
    pass