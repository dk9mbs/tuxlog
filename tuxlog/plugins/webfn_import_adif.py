from jobs.adifimportjob import AdifImportJob
from threading import Thread
from tuxlog.system import webfunction

def execute(name, params, **kwargs):

    logbook_id=params['logbook_id']
    content=params['content']        
    table="LogLogs"

    job=AdifImportJob()
    t = Thread(target=job.execute, args=(content,), kwargs={'table': table, 'logbook_id': logbook_id})
    t.start()

    return {"response": "pending"}


def register():
    webfunction.register('import_adif', execute)