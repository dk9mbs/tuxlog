
def execute(name, params, **kwargs):
    rig_id=params['rig_id']
    command=params['command']

    from usecases.rigctl import RigCtl
    from model.model import LogRigs
    
    rig=LogRigs.get_or_none(LogRigs.id==rig_id)

    if rig==None:
        params['status_code']=500
        return {'error': 'Rig not found in LogRigs table!' } #500

    try:
        rig_ctl=RigCtl( {"host": rig.remote_host, "port": rig.remote_port } )
        result=rig_ctl.get_rig(command)
        return result
    except Exception:
        params['status_code']=500
        return {'error': 'Error while reading data from rig!' } #500


def register():
    from usecases import webfunction
    webfunction.register('get_rig_data', execute)