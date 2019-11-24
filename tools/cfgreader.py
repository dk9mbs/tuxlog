#!/usr/bin/python3.5

from __future__ import print_function
import json
import os
import sys

cfg_file=sys.argv[1]
environment=sys.argv[2]

if not os.path.exists(cfg_file):
    cfg={
        "default": "build",
        "build":{
            "mysqlcfg": {"host":"localhost", "port":"3306","database":"database", "username":"username", "password":"password"},
            "security": {"secret_key": "mykey"},
            "client": {"host": "localhost", "port":"5000", "username":"username", "password": "password"}
        },
        "dev":{
            "mysqlcfg": {"host":"localhost", "port":"3306","database":"database", "username":"username", "password":"password"},
                "security": {"secret_key": "mykey"},
            "client": {"host": "localhost", "port":"5000", "username":"username", "password": "password"}
        },
        "test":{
            "mysqlcfg": {"host":"localhost", "port":"3306","database":"database", "username":"username", "password":"password"},
                "security": {"secret_key": "mykey"},
            "client": {"host": "localhost", "port":"5000", "username":"username", "password": "password"}
        },
        "prod":{
            "mysqlcfg": {"host":"localhost", "port":"3306","database":"database", "username":"username", "password":"password"},
                "security": {"secret_key": "mykey"},
            "client": {"host": "localhost", "port":"5000", "username":"username", "password": "password"}
        }
    }

    environments=["build","test","dev"]

    host=input("Host: ")
    port=input("Port: ")
    database=input("Database: ")
    username=input("Database User: ")
    password=input("Password: ")

    for env in environments:
        cfg[env]['mysqlcfg']['host']=host
        cfg[env]['mysqlcfg']['port']=port
        cfg[env]['mysqlcfg']['database']=database
        cfg[env]['mysqlcfg']['username']=username
        cfg[env]['mysqlcfg']['password']=password

    with open(cfg_file,'w') as json_cfg:
        json_cfg.writelines(json.dumps(cfg))
        json_cfg.flush()
        json_cfg.close()


with open (cfg_file, 'r') as json_cfg:
    cfg=json.load(json_cfg)

print("reading "+sys.argv[3]+"."+sys.argv[4]+" from "+sys.argv[2]+" ("+sys.argv[2]+")", file=sys.stderr)

print(cfg[sys.argv[2]][sys.argv[3]][sys.argv[4]])
