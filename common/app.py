#!/usr/bin/python3.5

from __future__ import print_function

import sys
import json
import time
import argparse
import os
import signal
import logging
import config
import importlib
from socket import AF_INET, socket, SOCK_STREAM
from flask import Flask
from flask import Blueprint
from gevent.pywsgi import WSGIServer
from flaskext.mysql import MySQL
from model import model
import urllib.parse
from common.solution import find_all_solutions

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(filename='/tmp/tuxlog.log')
logger = logging.getLogger(__name__)

config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

def handler(signum, frame):
    pass

def handler_int(signum, frame):
    logger.info('Strg+c')
    sys.exit()

signal.signal(signal.SIGINT, handler_int)
signal.signal(signal.SIGTERM, handler)


from common.endpoints.main import app
from common.endpoints.data import database
from common.endpoints.webfunction import webfunction
from ui_view import ui

app.register_blueprint(database,url_prefix='/api/v1.0/tuxlog')
app.register_blueprint(ui, url_prefix='/')
app.register_blueprint(webfunction, url_prefix='/api/v1.0/webfunction')


def test(value):
    print('test')
    
find_all_solutions( test )

