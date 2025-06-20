import unittest
#from model.model import *
from model.model import *
class CreateTestDatabase(unittest.TestCase):
    def test_create(self):
        """
        Test that it can sum a list of integers
        """

        import sys
        from model.model import BaseModel
        from model import model
        import peewee
        #from model.model import database as db

        models=list()

        for cls in sys.modules["model.model"].__dict__.values():
            try:
                if BaseModel in cls.__bases__:
                    if type(cls) is peewee.ModelBase:
                        #print(type(cls))
                        models.append(cls)
            except:
                pass

        #model.database.initialize(MySQLDatabase('tuxlog_build', **{'host': '10.8.1.1', 'use_unicode': True, 'user': 'root', 'password': 'messwert', 'charset': 'utf8'}))
        model.database.initialize(SqliteDatabase(':memory:'))
        model.database.connect()

        for table in models:
            try:
                model.database.create_tables([table])
            except:
                print (  "Exception => %s (%s)" % (table, str(sys.exc_info()))   )


        #print( model.database.get_tables() )