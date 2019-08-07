import requests
#from .. import modelfactory as test

class HamBaseInfoProvider:
    def read(self, call, info_json):
        pass

class HamDbProvider(HamBaseInfoProvider):
    def read(self, call, info_json):
        headers={"Accept":"text/html,text/json,application/xhtml+xml,application/xml;"}
        r = requests.get('http://api.hamdb.org/%s/json/APPNAME' % call, headers=headers)

        if r.json()['hamdb']['messages']['status'] != "OK":
            pass

        info_json['haminfo']['call']=r.json()['hamdb']['callsign']['call']
        info_json['haminfo']['name']=r.json()['hamdb']['callsign']['name']
        info_json['haminfo']['lat']=r.json()['hamdb']['callsign']['lat']
        info_json['haminfo']['lon']=r.json()['hamdb']['callsign']['lon']
        info_json['haminfo']['qth']=r.json()['hamdb']['callsign']['addr2']
        info_json['haminfo']['country']=r.json()['hamdb']['callsign']['country']
        info_json['haminfo']['locator']=r.json()['hamdb']['callsign']['grid']
        info_json['datasource']="hamdb"