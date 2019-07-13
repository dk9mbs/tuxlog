from __future__ import print_function
import sys
import dk9mbs.database.model

class ModelClassFactory:
    _name=""

    def __init__(self, name):
        self._name=name
        pass

    def create(self):
        return getattr(sys.modules["dk9mbs.database.model"], self._name)


#Tests
if __name__=="__main__":

    mod=ModelClassFactory("LogLogs").create()

    print(type(mod))
    entry=mod.get(mod.id==736)
    print (entry.__dict__)
    print(__file__)
