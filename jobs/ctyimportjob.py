from model import model
from model.model import LogImportjobs
from jobs.importjob import ImportJob
from tuxlog.file_import.ctyimport import CtyImport
class BaseImportJob:

    def __init__(self):
        self._job=None

    def start(self):
        job=ImportJob()
        job.start("cty.dat import")
        self._job=job
        pass

    def end(self, status_id):
        self._job.stop(20)
        pass

    def execute(self, *args, **kwargs):
        pass


class CtyImportJob(BaseImportJob):

    def execute(self, content, **kwargs):
        self.start()

        parser = CtyImport()
        @parser.register("error_save_cty_rec")
        def error_save_adif_record(**kwargs):
            #nonlocal saved_rec
            pass

        @parser.register("after_save_cty_rec")
        def after_save_adif_rec(**kwargs):
            #nonlocal saved_rec
            country=kwargs['record']
            message='JOB: %s => %s (%s) offset:%s' % (country['prefix'], country['country'], country['continent'], country['time_offset']  )
            
            job=kwargs['user_data']['job']
            job.increment_success(message)
            pass

        parser.execute(content,user_data={'job': self._job} )

        self.end(20)
