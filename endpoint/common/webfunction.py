#!/usr/bin/python3.5

from __future__ import print_function

import sys
import json
import time
import argparse
import os
import signal
import logging
import usecases.tuxlog.callbook as callbook
from usecases.tuxlog.datamodel import ModelClassFactory
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
from usecases.tuxlog.datamodel import get_modellist_by_raw
import datetime
from decimal import Decimal
from usecases.tuxlog import webfunction


logger = logging.getLogger(__name__)

webfunction=Blueprint('webfunction', __name__, template_folder='templates', static_folder='static')

# webfunction api
@webfunction.route('/api/v1.0/webfunction/<name>', methods=['POST', 'GET'])
def call_action(name):
    from usecases.tuxlog import webfunction

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
