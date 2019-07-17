import requests
import json
from dk9mbs.haminfo.hamdb import HamDbProvider
from dk9mbs.haminfo.hamdb import HamInfoProviderResultFactory
from dk9mbs.haminfo.hamdb import HamBaseInfoProvider

class HamInfoProviderFactory:

    def __init(self):
        pass

    @classmethod    
    def create(cls, provider):
        if provider=="hamdb":
            return HamDbProvider()
        elif provider=="test":
            return HamBaseInfoProvider()
        else:
            return HamBaseInfoProvider()

