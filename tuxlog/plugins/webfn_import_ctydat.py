from jobs.ctyimportjob import CtyImportJob
from threading import Thread
from tuxlog.system import webfunction

def execute(name, params, **kwargs):

    content=params['content'] 
    
    job=CtyImportJob()

    t = Thread(target=job.execute, args=(content,))
    t.start()
    return {"response": "pending"}

def register():
    webfunction.register('import_ctydat', execute)