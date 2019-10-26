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

# ============================================
from playhouse.signals import post_save, pre_save
from usecases.hook_main import hook

def pre_save_exec_hook(sender, instance, created):
    params={'sender': sender, 'instance': instance, 'created': created}
    hook.execute('pre_save', params)

pre_save.connect(pre_save_exec_hook ,sender=LogLogs)

# Register hooks

for file in os.listdir( os.path.join(config.AppConfig.get_app_root(), 'plugins')):
    if file.endswith(".py") and not file.startswith('__'):
        logger.info(file)
        i = importlib.import_module('plugins.'+file.replace('.py', ''))
        i.register()
# ============================================

config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

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


# dataimport api
@app.route('/api/v1.0/import/<table>', methods=['POST'])
def adif_import(table):
    if request.headers.get("content-type")=="text/adif":
        from jobs.adifimportjob import AdifImportJob
        from threading import Thread

        if request.args.get("logbook_id") != None:
            logbook_id = request.args.get("logbook_id")
        else:
            return Response(json.dumps({'error':'Cannot find logbook_id in querystring!!!'}), 500)

        content="".join(map(chr, request.data))        

        job=AdifImportJob()
        t = Thread(target=job.execute, args=(content,), kwargs={'table': table, 'logbook_id': logbook_id})
        t.start()

        return Response(json.dumps({"response": "pending"}) ,mimetype="text/json")

    elif request.headers.get("content-type")=="text/cty":

        from jobs.ctyimportjob import CtyImportJob
        from threading import Thread

        content="".join(map(chr, request.data))  
        job=CtyImportJob()

        t = Thread(target=job.execute, args=(content,))
        t.start()
        return Response(json.dumps({"response": "pending"}) ,mimetype="text/json")


# callbook api
@app.route('/api/v1.0/callbook/<provider>/<call>', methods=['GET'])
def get_ham_info(provider, call):
    result=callbook.init_haminfo_dict()
    callbook.HamInfoProviderFactory.create(provider).read(call, result)
    logger.info('HamInfo => %s' % str(result))
    return Response(json.dumps(result), mimetype="text/json")



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


# rig api
@app.route('/api/v1.0/rigctl/<rig_id>/<command>', methods=['GET'])
def get_rig(rig_id, command):
    from usecases.rigctl import RigCtl
    from model.model import LogRigs
    
    rig=LogRigs.get_or_none(LogRigs.id==rig_id)

    if rig==None:
        return Response( json.dumps( {'error': 'Rig not found in LogRigs table!' }), content_type="text/json" , status=500)

    try:
        rig_ctl=RigCtl( {"host": rig.remote_host, "port": rig.remote_port } )
        result=rig_ctl.get_rig(command)
        return Response(json.dumps(result) ,mimetype="text/json")
    except Exception as e:
        return Response(json.dumps( {'error': 'Error while reading data from rig!' }), content_type="text/json" , status=500)

@app.route('/api/v1.0/rigctl/<rig_id>/<command>/<value>', methods=['GET'])
@app.route('/api/v1.0/rigctl/<rig_id>/<command>/<value>/<value2>', methods=['GET'])
def set_rig(rig_id, command, value, value2=None):
    from usecases.rigctl import RigCtl
    from model.model import LogRigs
    
    value_list=[value, value2]

    rig=LogRigs.get_or_none(LogRigs.id==rig_id)

    if rig==None:
        return Response( json.dumps( {'error': 'Rig not found in LogRigs table!' }) , 500)

    rig_ctl=RigCtl( {"host": rig.remote_host, "port": rig.remote_port } )
    result=rig_ctl.set_rig(command, value_list)
    return Response(json.dumps({"response": result}) ,mimetype="text/json")


#server = WSGIServer((cfg['httpcfg']['host'], int(cfg['httpcfg']['port'])), app, handler_class=WebSocketHandler)
#server.serve_forever()





