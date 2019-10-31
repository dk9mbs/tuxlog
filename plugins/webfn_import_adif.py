
def execute(name, params, **kwargs):
    from jobs.adifimportjob import AdifImportJob
    from threading import Thread

    logbook_id=params['logbook_id']
    content=params['content']        
    table="LogLogs"

    job=AdifImportJob()
    t = Thread(target=job.execute, args=(content,), kwargs={'table': table, 'logbook_id': logbook_id})
    t.start()

    return {"response": "pending"}


def register():
    from usecases import webfunction
    webfunction.register('import_adif', execute)