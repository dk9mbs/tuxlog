import requests
import json
from services.callbook.hamdb import HamDbProvider
from services.callbook.hamdb import HamBaseInfoProvider

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


def init_haminfo_dict():
    result={"haminfo":{}}
    result['haminfo']['call']=""
    result['haminfo']['name']=""
    result['haminfo']['lat']=""
    result['haminfo']['lon']=""
    result['haminfo']['qth']=""
    result['haminfo']['country']=""
    result['haminfo']['locator']=""
    result['datasource']=""
    print(type(result))
    return result