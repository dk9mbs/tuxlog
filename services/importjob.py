from model.model import LogImportjobs
import datetime

class ImportJob:
    __importjob=None

    def __init__(self):
        self.__importjob=None
        pass

    def start(self, job_name):
        job = LogImportjobs()
        job.start_date=datetime.datetime.now()
        job.status=0
        job.job_name=job_name
        job.import_fail=0
        job.import_success=0
        job.save()
        self.__importjob=job
        return job

    def increment_success(self, message):
        job=self.__importjob
        job.message=message
        job.import_success=self.__importjob.import_success+1
        job.status_id=10
        job.save()

    def stop(self, status_id):
        job=self.__importjob
        job.end_date=datetime.datetime.now()
        job.status=status_id
        job.save()
        #self.__importjob=None
