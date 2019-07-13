import sys
from modelfactory import ModelClassFactory
#import dk9mbs.database.model
from dk9mbs.database.model import LogRigs

mod=ModelClassFactory("LogLogs").create()
entry=mod.get(mod.id==736)
print (entry.__dict__)
print(__file__)




#LogRigs.create(id="ic957", description="test")
