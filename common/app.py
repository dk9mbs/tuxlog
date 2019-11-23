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
from flask import Flask
from flask import Blueprint
from flaskext.mysql import MySQL
from model import model
import urllib.parse
from common.solution import find_all_solutions
from flask import Blueprint
from flask import jsonify
from flask_socketio import SocketIO

logging.basicConfig(level=logging.INFO )
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

# create app object

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='<{',
        variable_end_string='}>',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

app = CustomFlask(__name__, template_folder='htdocs', static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

app.debug=False
app.threaded=True

socketio=SocketIO(app)

@app.before_request
def _db_connect():
    try:
        model.database.connect()
    except:
        pass

@app.teardown_request
def _db_close(exc):
    logger.info("Closing database ...")
    if not model.database.is_closed():
        model.database.close()


@app.errorhandler(ConnectionRefusedError)
def handle_error(error):
    message = [str(x) for x in error.args]
    #status_code = error.status_code
    status_code=500
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message,
            'traceback': None
        }
    }
    logger.exception(error)
    return jsonify(response), status_code

# Import the base endpoints
from common.endpoints.data import database
from common.endpoints.webfunction import webfunction

app.register_blueprint(database,url_prefix='/api/v1.0/tuxlog')
app.register_blueprint(webfunction, url_prefix='/api/v1.0/webfunction')
    
find_all_solutions()

