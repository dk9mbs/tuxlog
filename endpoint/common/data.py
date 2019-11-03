#!/usr/bin/python3.5

from __future__ import print_function

import sys
import json
import time
import logging
import config
import importlib
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import abort
from flask import jsonify
from flask import Blueprint
from flaskext.mysql import MySQL
from playhouse.shortcuts import model_to_dict, dict_to_model
from model.model import LogLogs
from model import model
import urllib.parse
import datetime
from decimal import Decimal
from tuxlog.system.datamodel import get_modellist_by_raw, ModelClassFactory

logger = logging.getLogger(__name__)

database=Blueprint('database', __name__, template_folder='templates', static_folder='static')

# Web Api v1.0

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

@database.route('/<table>', methods=['POST', 'PUT'])
@database.route('/<table>/<id>', methods=['POST', 'PUT'])
def save_or_update(table, id=None):
    mod_cls=ModelClassFactory(table).create()
    data_model=dict_to_model(mod_cls, request.json)
    
    if request.method=='POST':
        data_model.save(force_insert=True)
    else:
        data_model.save()

    logger.info('id created after save => %s' % str(data_model.id))

    #for wsock in connections:
    #    wsock.send(json.dumps({'publisher':'save','target': table, 'message': {"id":data_model.id} } ))

    return Response({"id":data_model.id})


@database.route('/<table>', methods=['GET'])
def get_dataset(table):
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

@database.route('/<table>/<recordid>', methods=['GET'])
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

@database.route('/<table>/<recordid>', methods=['DELETE'])
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


