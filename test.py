from business.adifimport import AdifImportLogic

f = open("/tmp/wsjtx_log.adi", "r")
content=f.read()

parser = AdifImportLogic("LogLogs", "dk9mbs")
@parser.register("after_save_adif_rec")
def readline(**kwargs):
    print(kwargs['adif_rec'])
    pass

parser.adif_import(content)
