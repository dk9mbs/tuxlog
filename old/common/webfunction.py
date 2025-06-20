
__hooks=dict()

def register(name, fn):
    if not name in __hooks:
        __hooks[name]=list()
    (__hooks[name]).append( {'fn': fn, 'name': name} )

'''
name: Name of hook
params: dict with userdata
'''
def execute(name, params, **kwargs):
    params['result']={}
    if name in __hooks:
        hook=__hooks[name]
        for x in range(0, len(hook)):
            params['result']=hook[x]['fn'](name, params, **kwargs)
        
    return params['result']
