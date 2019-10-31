
def execute(name, params, **kwargs):
    from jobs.ctyimportjob import CtyImportJob
    from threading import Thread

    content=params['content'] 
    
    job=CtyImportJob()

    t = Thread(target=job.execute, args=(content,))
    t.start()
    return {"response": "pending"}

def register():
    from usecases import webfunction
    webfunction.register('import_ctydat', execute)