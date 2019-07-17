import sys
from modelfactory import ModelClassFactory
#import dk9mbs.database.model
#from dk9mbs.database.model import LogRigs

from dk9mbs.haminfoproviderfactory import HamInfoProviderResultFactory

HamInfoProviderResultFactory("hamdb").create()

#mod=ModelClassFactory("LogLogs").create()
#entry=mod.get(mod.id==736)
#print (entry.__dict__)
#print(__file__)




#LogRigs.create(id="ic957", description="test")
