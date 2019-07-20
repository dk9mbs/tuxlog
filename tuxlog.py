#!/usr/bin/python3.5

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

from flaskext.mysql import MySQL

from playhouse.shortcuts import model_to_dict, dict_to_model

#from modelfactory import ModelClassFactory
#import haminfoproviderfactory as haminfo
from business.modelfactory import ModelClassFactory
import business.haminfo as haminfo


with open('/etc/tuxlog/tuxlog_cfg.json') as json_file:
    cfg=json.load(json_file)


parser = argparse.ArgumentParser(description='Get iq datastream form radio device')

parser.add_argument("-f", "--frequency", dest="frequency",
                        help="Frequency (in Hz)", metavar="FREQUENCY")
parser.add_argument("-o", "--output", dest="outputfile",
                        help="Onput file", metavar="FILE")
parser.add_argument("-s", "--sample-rate", dest="samplerate",
                        help="Samplerate", metavar="SAMPLERATE")
parser.add_argument("-g", "--gain", dest="gain",
                        help="Gain", metavar="GAIN")
parser.add_argument("-p", "--port", dest="port",
                        help="TCP port for listening iq stream", metavar="PORT")
parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")

args = parser.parse_args()


if args.frequency:
    cfg['hwcfg']['frequency']=args.frequency

def handler(signum, frame):
    pass

def handler_int(signum, frame):
    print('Strg+c', signum)
    sys.exit()

signal.signal(signal.SIGINT, handler_int)
signal.signal(signal.SIGTERM, handler)

app = Flask(__name__, template_folder='htdocs', static_url_path='/htdocs/')
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

app.debug=False
app.host=cfg['httpcfg']['host']
app.port=cfg['httpcfg']['port']
app.threaded=True


# UI
@app.route('/')
def index():
    return render_template('index.htm', config=cfg)

@app.route('/js/<file>', methods=['GET'])
def get_js_file(file):
    print('get file: %s' % file, file=sys.stderr)

    #return app.send_static_file(file)
    try:
        return render_template(file, config=cfg)
    except:
        print('error')
        abort(404)


# Websocket
connections = set()

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

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
    #print("##############TYPE#############"+str(type(obj)))
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

@app.route('/api/v1.0/<database>/<table>', methods=['POST'])
def save_or_update(database, table):
    mod_cls=ModelClassFactory(table).create()
    data_model=dict_to_model(mod_cls, request.json)
    #data_model.save(force_insert=True)
    data_model.save()
    print(data_model.id)

    for wsock in connections:
        wsock.send(json.dumps({'publisher':'save','target': table, 'message': {"id":data_model.id} } ))

    return Response({"id":data_model.id})


@app.route('/api/v1.0/<database>/<table>/<page>/<pagesize>', methods=['GET'])
@app.route('/api/v1.0/<database>/<table>/<pagesize>', methods=['GET'])
@app.route('/api/v1.0/<database>/<table>', methods=['GET'])
def get_dataset(database, table, page=1, pagesize=0):
    from peewee import Ordering
    from operator import attrgetter
    from peewee import RawQuery

    order=""
    limit=""
    where=""

    if request.args.get("order") != None:
        order = request.args.get("order")

    if request.args.get("where") != None:
        where = request.args.get("where")
    
    mod_cls=ModelClassFactory(table).create()

    table=mod_cls._meta.table_name


    if order!="":
        order=" ORDER BY %s" % order

    if int(pagesize)>0:
        limit=" LIMIT %s" % str(pagesize)

    if where!="":
        where = " WHERE %s" % where

    sql='Select * from %s %s %s %s;' % (table, where, order, limit)
    print(sql)
    query=mod_cls.raw(sql)
    
    #print(query)
    tmp=[]
    #for item in query:
    #    print(item.id)
    #    tmp.append(model_to_dict(item))

    tmp = list(query.dicts())
    tmp=json.dumps(tmp, default=typeformatter)
    return Response(
            tmp,
            mimetype="text/json",
            headers={
                "dk9mbs": "yes"
            }
        )     

@app.route('/api/v1.0/<database>/<table>/<recordid>', methods=['GET'])
def get_record(database, table, recordid):

    mod=ModelClassFactory(table).create()
    data = model_to_dict(mod.get(mod.id==recordid))
    
    if len(data) == 0:
        print ("FEHLER")
        return
        
    #data=json.dumps( data, default=JsonTypeConverter().typeformatter )
    data=json.dumps( data, default=typeformatter )
 
    print(data)

    return Response(
            data,
            mimetype="text/json",
            headers={
                "dk9mbs": "yes"
            }
        )     

@app.route('/api/v1.0/haminfo/<provider>/<call>', methods=['GET'])
def get_ham_info(provider, call):
    result=haminfo.init_haminfo_dict()
    haminfo.HamInfoProviderFactory.create(provider).read(call, result)
    print("HamInfo => "+str(result))
    return Response(json.dumps(result), mimetype="text/json")

server = WSGIServer((cfg['httpcfg']['host'], int(cfg['httpcfg']['port'])), app, handler_class=WebSocketHandler)
server.serve_forever()






