import json
import os
from model import model
from peewee import MySQLDatabase

current_cfg={}


class DatabaseConfig:
    _current_cfg={}

    @classmethod
    def get_current_cfg(cls):
        return cls._current_cfg

    @classmethod
    def set_current_cfg(cls, cfg):
        cls._current_cfg=cfg

    @classmethod
    def read_from_file(cls, environment="", file="/etc/tuxlog/tuxlog_cfg.json"):

        print('current environment => %s' % environment)

        with open(file) as json_file:
            cfg=json.load(json_file)[environment]

        cls._current_cfg=cfg
        return cfg

    @classmethod
    def open(cls, database, cfg):
        cfg = cls._current_cfg['mysqlcfg']
        database.initialize(MySQLDatabase(cfg['database'], **{'host': cfg['host'], 
            'use_unicode': True, 'user': cfg['username'], 'password': cfg['password'], 'charset': 'utf8'}))
        database.connect()    
