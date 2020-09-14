import requests
import logging
import json
from datetime import datetime
from datetime import date
from datetime import time

class RestApiClient:
    def __init__(self, root_url="http://localhost:5000/api"):
        self.__session_id=None
        self.__cookies=None
        self.__root=f"{root_url}/v1.0"

    def login(self, username, password):
        headers={
            "username":username,
            "password":password
        }

        r=requests.post(f'{self.__root}/core/login', headers=headers)

        if r.status_code==200:
            session=r.cookies['session']
        else:
            session=None

        if r.status_code!=200:
            raise NameError(f"{r.text}")

        self.__cookies={"session": session}
        self.__session_id=session
        return r.text

    def logoff(self):
        r=requests.post(f'{self.__root}/core/logoff', cookies=self.__cookies)
        self.__session_id=None
        if r.status_code!=200:
            raise NameError(f"{r.text}")
        return r.text

    def delete(self, table, id):
        url=f"{self.__root}/data/{table}/{id}"
        r=requests.delete(url, cookies=self.__cookies)
        print(r.status_code)
        if r.status_code!=200:
            raise NameError(f"{r.status_code} {r.text}")
        return r.text

    def add(self, table,data):
        logging.warning("Method add ist deprecated! Pse use create")
        return self.create(table,data)

    def create(self, table,data):
        url=f"{self.__root}/data/{table}"
        headers={"Content-Type":"application/json"}
        data=json.dumps(data,default=self.__json_serial)
        data=json.loads(data)
        r=requests.post(url, headers=headers, json=data, cookies=self.__cookies)
        if r.status_code!=200:
            raise NameError(f"{r.status_code} {r.text}")
        return r.text

    def read(self, table, id):
        url=f"{self.__root}/data/{table}/{id}"
        r=requests.get(url, cookies=self.__cookies)
        if r.status_code!=200:
            raise NameError(f"{r.status_code} {r.text}")
        return r.text

    def update(self,table,id, data):
        url=f"{self.__root}/data/{table}/{id}"
        headers={"Content-Type":"application/json"}
        data=json.dumps(data,default=self.__json_serial)
        data=json.loads(data)
        r=requests.put(url, headers=headers, json=data, cookies=self.__cookies)
        if r.status_code!=200:
            raise NameError(f"{r.status_code} {r.text}")
        return r.text

    def read_multible(self, table, fetchxml=None):
        if fetchxml==None:
            url=f"{self.__root}/data/{table}"
            r=requests.get(url, cookies=self.__cookies)
        else:
            url=f"{self.__root}/data"
            headers={"Content-Type":"application/xml"}
            r=requests.post(url, cookies=self.__cookies, data=fetchxml, headers=headers)

        if r.status_code!=200:
            raise NameError(f"{r.status_code} {r.text}")
        return r.text

    def __json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))


if __name__=='__main__':
    client=RestApiClient()
    print(client.login("guest", "password"))

    print(client.delete("dummy",99))
    print(client.delete("dummy",100))
    print(client.add("dummy", {'id':99,'name':'IC735', 'port':3306}))
    print(client.add("dummy", {'id':100,'name':'TEST', 'port':3306}))
    print(client.read("dummy", 99))
    print(client.update("dummy", 99, {'id':99,'name':'GD77', 'port':3307}))
    print(client.read("dummy", 99))
    print(client.read_multible("dummy"))


    fetch="""
    <restapi>
        <table name="dummy"/>
        <comment text="from admin.py"/>
        <filter type="OR">
            <condition field="name" value="GD77" operator="="/>
            <condition field="name" value="TEST" operator="="/>
        </filter>
    </restapi>
    """
    print(client.read_multible("dummy", fetch))


    print(client.logoff())



