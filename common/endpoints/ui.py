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
from common.app import app
import common.bgtask

logger = logging.getLogger(__name__)

ui=Blueprint('ui', __name__, template_folder='htdocs', static_folder='static')

@ui.route('/')
@ui.route('/<file>')
@ui.route('/<path:path>')
def index(file="index.html", path=""):
    if file=='favicon.ico':
        return Response(status=404)

    headers=dict()
    headers['Access-Control-Allow-Origin']='*'
    return Response(render_template(file,config=common.bgtask.get_all(), headers=headers))
