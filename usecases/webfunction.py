
__hooks=dict()

def register(name, fn):
    __hooks[name]=fn
    #if not name in __hooks:
    #    __hooks[name]=list()
    #(__hooks[name]).append( {'fn': fn, 'name': name} )

'''
name: Name of hook
params: dict with userdata
'''
def execute(name, params, **kwargs):
    if name in __hooks:
        fn=__hooks[name]
        return fn(name, params, **kwargs)
    else:
        return {}

    #for hook, value in __hooks.items():
    #    if hook==name:
    #        for x in range(0, len(value)):
    #            value[x]['fn'](name, params, **kwargs)
