import sys
from model.model import BaseModel
from model.model import database as db
db.connect()
for cls in sys.modules["model.model"].__dict__.values():
    try:
        if BaseModel in cls.__bases__:
            print(cls)
            cls.create_table()
            print("...done!")
    except:
        pass

print(db.get_tables())
