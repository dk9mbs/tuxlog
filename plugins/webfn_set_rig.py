
def execute(name, params, **kwargs):
    from usecases.rigctl import RigCtl
    from model.model import LogRigs

    command=params['command']
    value=params['value']
    rig_id=params['rig_id']
    value2=None

    if 'value2' in params:
        value2=params['value2']
    
    value_list=[value, value2]

    rig=LogRigs.get_or_none(LogRigs.id==rig_id)

    if rig==None:
        params['status_code']=500
        return {'error': 'Rig not found in LogRigs table!' }

    rig_ctl=RigCtl( {"host": rig.remote_host, "port": rig.remote_port } )
    result=rig_ctl.set_rig(command, value_list)
    return {"response": result}


def register():
    from usecases import webfunction
    webfunction.register('set_rig_data', execute)