import sys

class BaseObject(object):
    _fn=list()

    def register(self, name):
        def wrapper(fn):
            for obj in self._fn:
                if obj['name']==name:
                    return fn

            self._fn.append({"name": name, "fn": fn})
            return fn
        return wrapper
    
    def _execute(self, name, **kwargs):
        for fn in self._fn:
            if fn['name']==name:
                fn['fn'](**kwargs)