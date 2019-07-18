from __future__ import print_function

import sys
import services.database.model

class ModelClassFactory:
    _name=""

    def __init__(self, name):
        self._name=name
        pass

    def create(self):
        return getattr(sys.modules["services.database.model"], self._name)


