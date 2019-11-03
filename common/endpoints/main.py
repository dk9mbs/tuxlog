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
from model import model

logger = logging.getLogger(__name__)


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


# Websocket
connections = set()

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        return Response( json.dumps( { 'error': 'Expected WebSocket request.'} ), 400)

    connections.add(wsock)
    
    while True:
        try:
            wsock.receive()
        except WebSocketError:
            break
    connections.remove(wsock)
    abort(500)


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



