

from dk9mbs.database import ConnectionFactory
import sys

def create_model():
    import model
    rig=getattr(sys.modules["model"], "LogRigs")
    rig.create(id="ft857", description="ICOM FT 857")
    
    rig.save()
    #print(rig)

create_model()


