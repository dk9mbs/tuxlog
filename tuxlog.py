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

from dk9mbs.database import ConnectionFactory
from dk9mbs.database import DataSet
from dk9mbs.database import CommandBuilderFactory

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



ConnectionFactory.init(app, cfg)
print(ConnectionFactory.mysql)

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

from datetime import datetime
from datetime import date
from datetime import timedelta
from decimal import Decimal

'''Create an encoder subclassing JSON.encoder. 
Make this encoder aware of our classes (e.g. datetime.datetime objects) 
'''
class JsonTypeConverter(json.JSONEncoder):
    def typeformatter(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return self.default(self, obj)



@app.route('/api/v1.0/<database>/<table>', methods=['GET'])
def get_dataset(database, table):
    data=DataSet().fetch(CommandBuilderFactory.create_builder(ConnectionFactory.create_connection(),{
        "query": 'SELECT * from log_%s ORDER BY id desc' % table,
        "rowcount": 50
        }, '')
    )
    data=json.dumps( data, default=JsonTypeConverter().typeformatter )
    return Response(
            data,
            mimetype="text/json",
            headers={
                "dk9mbs": "yes"
            }
        )     

@app.route('/api/v1.0/<database>/<table>/<recordid>', methods=['GET'])
def get_record(database, table, recordid):
    data=DataSet().fetch(CommandBuilderFactory.create_builder(ConnectionFactory.create_connection(),{
        "query": 'SELECT * from log_%s WHERE id=%s ORDER BY id desc' % (table, recordid),
        "rowcount": 1
        }, '')
    )

    if len(data) == 0:
        print ("FEHLER")
        return
        
    data=json.dumps( data[0], default=JsonTypeConverter().typeformatter )
    print(data)
    return Response(
            data,
            mimetype="text/json",
            headers={
                "dk9mbs": "yes"
            }
        )     

server = WSGIServer((cfg['httpcfg']['host'], int(cfg['httpcfg']['port'])), app, handler_class=WebSocketHandler)
server.serve_forever()






