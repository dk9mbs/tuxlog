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

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(filename='/tmp/tuxlog.log')
logger = logging.getLogger(__name__)

config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

# ============================================
# Register all plugins
for file in os.listdir( os.path.join(config.AppConfig.get_app_root(), 'tuxlog/plugins')):
    if file.endswith(".py") and not file.startswith('__'):
        logger.info(file)
        i = importlib.import_module('tuxlog.plugins.'+file.replace('.py', ''))
        i.register()
# ============================================

def handler(signum, frame):
    pass

def handler_int(signum, frame):
    logger.info('Strg+c')
    sys.exit()

signal.signal(signal.SIGINT, handler_int)
signal.signal(signal.SIGTERM, handler)


from common.endpoints.common import app
from common.endpoints.common.data import database
from common.endpoints.common.webfunction import webfunction
from ui_view import ui

app.register_blueprint(database,url_prefix='/api/v1.0/tuxlog')
app.register_blueprint(ui, url_prefix='/')
app.register_blueprint(webfunction, url_prefix='/api/v1.0/webfunction')




