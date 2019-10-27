import unittest

from model import model
from model.model import MySQLDatabase
from os import getenv
import os
import config

from jobs.importjob import ImportJob
from usecases.ctyimport import CtyImport

class TestImportJob(unittest.TestCase):
    def test_import(self):
        config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

        job = ImportJob()
        print('Jobid => %s' % job.start("Test Job").id )

        job.stop(20)

        pass




if __name__ == '__main__':
    unittest.main()