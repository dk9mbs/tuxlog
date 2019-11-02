from jobs.ctyimportjob import CtyImportJob
from threading import Thread
from usecases.tuxlog import webfunction

def execute(name, params, **kwargs):

    content=params['content'] 
    
    job=CtyImportJob()

    t = Thread(target=job.execute, args=(content,))
    t.start()
    return {"response": "pending"}

def register():
    webfunction.register('import_ctydat', execute)