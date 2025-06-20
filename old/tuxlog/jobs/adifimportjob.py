import datetime
import logging
from model import model
from model.model import LogImportjobs
from model.model import LogLogs
from tuxlog.file_import.ctyimport import CtyImport
from tuxlog.file_import.adifimport import AdifImport
from tuxlog.jobs.importjob import ImportJob
from tuxlog.jobs.ctyimportjob import BaseImportJob

logger = logging.getLogger(__name__)

class AdifImportJob(BaseImportJob):
    def __init__(self):
        pass

    def execute(self, content, **kwargs):
        self.start()

        table=kwargs['table']
        logbook_id=kwargs['logbook_id']
        saved_rec=[]

        parser = AdifImport(table,logbook_id)
        @parser.register("error_save_adif_rec")
        def error_save_adif_record(**kwargs):
            job=kwargs['user_data']['job']
            nonlocal saved_rec
            saved_rec.append({"status":"Error", "message": {"error":kwargs['error_desc']}})

        @parser.register("after_save_adif_rec")
        def after_save_adif_rec(**kwargs):
            nonlocal saved_rec
            saved_rec.append({"status":"OK", "message": {"id": kwargs['adif_rec'].__data__['id']}})

            message='ID=>%s Call=>%s' % (kwargs['adif_rec'].__data__['id'],kwargs['adif_rec'].__data__['yourcall'])
            job=kwargs['user_data']['job']
            job.increment_success(message)
            
            #for wsock in connections:
            #    wsock.send(json.dumps({'publisher':'save','target': table, 'message': {"id":kwargs['adif_rec'].__data__['id']} } ))

        @parser.register('duplicate_search_LogLogs')
        def duplicate_search(**kwargs):
            job=kwargs['user_data']['job']
            log=kwargs['model']
            #log_exists=LogLogs.get_or_none((LogLogs.logbook==kwargs['logbook_id']) 
            #    & (LogLogs.yourcall==log.yourcall)
            #    & (LogLogs.logdate_utc==log.logdate_utc)
            #    & (LogLogs.start_utc==log.start_utc)
            #)

            start_utc=datetime.time(int(log.start_utc[0:2]), int(log.start_utc[2:4]), int(log.start_utc[4:6]))

            log_exists=LogLogs.get_or_none( 
                (LogLogs.yourcall==log.yourcall) & (LogLogs.logdate_utc==log.logdate_utc)
                & (LogLogs.start_utc==start_utc ) 
            )

            if log_exists != None:
                logger.info('Found duplicate logentry => %s' % log_exists.id)
                log.id=log_exists.id

            pass

        parser.execute(content, user_data={'job': self._job} )
        
        self.end(20)
