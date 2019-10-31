#!/usr/bin/python3.5

from __future__ import print_function

import sys
import json
import time
import argparse
import os
import signal
import logging
import usecases.callbook as callbook
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
from usecases.datamodel import ModelClassFactory
from model.model import LogLogs
from model import model

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(filename='/tmp/tuxlog.log')
logger = logging.getLogger(__name__)

config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

# ============================================
# Register all plugins
for file in os.listdir( os.path.join(config.AppConfig.get_app_root(), 'plugins')):
    if file.endswith(".py") and not file.startswith('__'):
        logger.info(file)
        i = importlib.import_module('plugins.'+file.replace('.py', ''))
        i.register()
# ============================================

def handler(signum, frame):
    pass

def handler_int(signum, frame):
    logger.info('Strg+c')
    sys.exit()

signal.signal(signal.SIGINT, handler_int)
signal.signal(signal.SIGTERM, handler)

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

# UI
@app.route('/')
@app.route('/<file>')
@app.route('/ui/<path:path>')
def index(file="index.html", path=""):
    if file=='favicon.ico':
        return Response(status=404)
    
    return render_template(file, config=config.DatabaseConfig.get_current_cfg() )

@app.route('/js/<file>', methods=['GET'])
def get_js_file(file):
    logger.info('get file: %s' % file)
    try:
        return Response(render_template('js/'+file, config=config.current_cfg), status=200, content_type="text/javascript", mimetype="test/javascript")
    except Exception as e:
        logger.exception(e)
        return Response( json.dumps( { 'error': 'not found'} ), 404)

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

# Web Api v1.0

import datetime
from decimal import Decimal

'''Create an encoder subclassing JSON.encoder. 
Make this encoder aware of our classes (e.g. datetime.datetime objects) 
'''
def typeformatter(obj):
    if isinstance(obj, datetime.time ) or isinstance(obj, datetime.date) :
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return str(obj)
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        #return json.JSONEncoder.default(self, obj)
        #return json.JSONEncoder.default(obj)
        pass

@app.route('/api/v1.0/tuxlog/<table>', methods=['POST', 'PUT'])
@app.route('/api/v1.0/tuxlog/<table>/<id>', methods=['POST', 'PUT'])
def save_or_update(table, id=None):
    mod_cls=ModelClassFactory(table).create()
    data_model=dict_to_model(mod_cls, request.json)
    
    if request.method=='POST':
        data_model.save(force_insert=True)
    else:
        data_model.save()

    logger.info('id created after save => %s' % str(data_model.id))

    for wsock in connections:
        wsock.send(json.dumps({'publisher':'save','target': table, 'message': {"id":data_model.id} } ))

    return Response({"id":data_model.id})


@app.route('/api/v1.0/tuxlog/<table>', methods=['GET'])
def get_dataset(table):
    import urllib.parse
    order=""
    where=""
    pagesize=0
    page=1

    if request.args.get("page") != None:
        page=request.args.get("page")

    if request.args.get("pagesize") != None:
        pagesize=request.args.get("pagesize")

    if request.args.get("order") != None:
        order = urllib.parse.unquote(request.args.get("order"))

    if request.args.get("where") != None:
        where = urllib.parse.unquote(request.args.get("where"))
    
    from usecases.datamodel import get_modellist_by_raw
    tmp = get_modellist_by_raw(table, where=where, order=order, pagesize=pagesize)

    tmp=json.dumps(tmp, default=typeformatter)
    return Response(
            tmp,
            mimetype="text/json",
            content_type="text/json",
            headers={
                "dk9mbs": "yes"
            }
        )     

@app.route('/api/v1.0/tuxlog/<table>/<recordid>', methods=['GET'])
def get_record(table, recordid):

    mod=ModelClassFactory(table).create()
    data = mod.get_or_none(mod.id==recordid)
    
    if data == None:
        logger.error('get_record: Record with id %s not found in table %s' % (recordid, table))
        return Response(status=404)

    data = model_to_dict(data)
    data=json.dumps( data, default=typeformatter )
 
    return Response(
            data,
            mimetype="text/json",
            headers={
                "dk9mbs": "yes"
            }
        )     

@app.route('/api/v1.0/tuxlog/<table>/<recordid>', methods=['DELETE'])
def del_record(table, recordid):
    #logger.error(recordid)
    mod=ModelClassFactory(table).create()
    query=mod.delete().where(mod.id == recordid)
    query.execute()
    
    return Response(
            {},
            mimetype="text/json",
            headers={
                "dk9mbs": "yes"
            }
        )     

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

# webfunction api
@app.route('/api/v1.0/webfunction/<name>', methods=['POST', 'GET'])
def call_action(name):
    from usecases import webfunction

    content=None

    if request.args.get('params', default=None) != None:
        #in case of query args read the content from body
        params=json.loads(request.args.get('params'))
        content="".join(map(chr, request.data))        
    else:
        params= json.loads("".join(map(chr, request.data)))  

    params['content']=content
    params['status_code']=200
    
    result=webfunction.execute(name, params)

    return Response(json.dumps(result) ,mimetype="text/json",content_type="text/json" , status=params['status_code'])


#server = WSGIServer((cfg['httpcfg']['host'], int(cfg['httpcfg']['port'])), app, handler_class=WebSocketHandler)
#server.serve_forever()





