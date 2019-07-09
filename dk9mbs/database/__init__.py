from __future__ import print_function

import sys
import json
import time
import argparse
import os
import signal

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock

from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import abort
from flask import jsonify

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import pymysql
from flaskext.mysql import MySQL

class MetaDataCache:
    __meta_data=dict()

    @classmethod
    def add(cls, key, meta_json):
        cls.__meta_data[key]=meta_json

    @classmethod
    def exists(cls, key):
        return key in cls.__meta_data

    @classmethod
    def get(cls,key):
        return cls.__meta_data[key]


class FieldMetaData:
    __json=None

    def __init__(self, meta_json):
        self.__meta_json=meta_json

    def is_auto_increment(self):
        return self.__meta_json['Extra']=="auto_increment"
    
    def is_editable(self):
        return not self.__meta_json['Extra']=="auto_increment"

    def is_numeric(self):
        return str(self.__meta_json['Type']).startswith("decimal") or \
            str(self.__meta_json['Type']).startswith("smallint") or \
            str(self.__meta_json['Type']).startswith("int")

    def is_text(self):
        return str(self.__meta_json['Type']).startswith("varchar") or \
            str(self.__meta_json['Type']).startswith("text") 

    def get_name(self):
        return self.__meta_json['Field']

class ConnectionFactory:
    mysql=None

    @classmethod
    def init(cls, app, cfg):
        cls.mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = cfg['mysqlcfg']['username']
        app.config['MYSQL_DATABASE_PASSWORD'] = cfg['mysqlcfg']['password']
        app.config['MYSQL_DATABASE_DB'] = cfg['mysqlcfg']['database']
        app.config['MYSQL_DATABASE_HOST'] = cfg['mysqlcfg']['host']
        cls.mysql.init_app(app)

 
    @classmethod
    def create_connection(cls):
        return cls.mysql.connect()


class DataSet:

    def __init__(self):
        pass

    def fetch(self, cmd_builder):
        args=cmd_builder.build_select()
        sql=args[0]
        rowcount=args[1]

        cursor =cmd_builder.get_connection().cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        data = cursor.fetchmany(size=rowcount)
        return data

'''
{
    "query": "SELECT * FROM logs where id>100",
    "rowcount": 50
}
'''
class CommandBuilder:
    __query_json=None
    __conn=None

    def __init__(self,conn, query_json={}):
        self.__query_json=query_json
        self.__conn=conn
        pass

    def set_connection(self, conn):
        self.__conn=conn
    
    def get_connection(self):
        return self.__conn

    # build the commands
    def build_select(self):
        if "query" in self.__query_json:
            sql=self.__query_json['query']

        if "rowcount" in self.__query_json:
            rowcount=int(self.__query_json['rowcount'])

        if sql != "":
            return sql, rowcount


    def build_insert(self):
        table="logs"
        
        fields=""
        values=""
        for key in self.__query_json:
            meta=self.__get_metadata(table, key)                    
            if meta!=None and meta.is_editable():
                if fields!="":
                    fields=fields+","
                    values=values+","

                fields=fields+key

                if meta.is_text():
                    values=values+"'"+self.__query_json[key]+"'"
                else:
                    values=values+str(self.__query_json[key]).replace(",",".")

        sql="INSERT INTO log_%s (%s) VALUES (%s);" % (table,fields,values)
        print(sql)
        return sql

    def __get_metadata(self, table, field):
        key='db_field_%s.%s' % (table, field)
        if MetaDataCache.exists(key):
            meta=MetaDataCache.get(key)
        else:
            meta=DataSet().fetch(
                CommandBuilderFactory.create_builder(self.__conn,{
                    "query": 'SHOW columns from log_%s WHERE Field=\'%s\'' % (table,field), "rowcount":0}, '')
            )
            if len(meta)==0:
                return None

            meta=FieldMetaData(meta[0])
            MetaDataCache.add(key, meta)
            
        return meta



class CommandBuilderFactory:
    @classmethod
    def create_builder(cls,conn, json_query={}, type='default'):
        return CommandBuilder(conn,json_query)


#Tests
if __name__=="__main__":
    app = Flask(__name__)
    with open('/etc/tuxlog/tuxlog_cfg.json') as json_file:
        cfg=json.load(json_file)
    ConnectionFactory.init(app,cfg)

    cmd = CommandBuilder(ConnectionFactory.create_connection(), {"yourcall":"dk9mbs", "power": "50", "id": "0"})
    cmd.build_insert()

    cmd = CommandBuilder(ConnectionFactory.create_connection(), {"yourcall":"dk9mbs", "power": "50", "id": "0", "name": "test"})
    cmd.build_insert()