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
from threading import Thread, Lock
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import abort
from flask import jsonify
from flask import Blueprint
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from flaskext.mysql import MySQL
from playhouse.shortcuts import model_to_dict, dict_to_model
from model.model import LogLogs
from model import model
import urllib.parse
import datetime
from decimal import Decimal
from tuxlog.system.datamodel import get_modellist_by_raw
#import usecases.tuxlog.callbook as callbook
#from usecases.tuxlog.datamodel import ModelClassFactory

logger = logging.getLogger(__name__)

ui=Blueprint('ui', __name__, template_folder='htdocs', static_folder='static')

# UI
@ui.route('/')
@ui.route('/<file>')
@ui.route('/ui/<path:path>')
def index(file="index.html", path=""):
    if file=='favicon.ico':
        return Response(status=404)
    
    return render_template(file, config=config.DatabaseConfig.get_current_cfg() )

@ui.route('/js/<file>', methods=['GET'])
def get_js_file(file):
    logger.info('get file: %s' % file)
    try:
        return Response(render_template('js/'+file, config=config.current_cfg), status=200, content_type="text/javascript", mimetype="test/javascript")
    except Exception as e:
        logger.exception(e)
        return Response( json.dumps( { 'error': 'not found'} ), 404)

#
