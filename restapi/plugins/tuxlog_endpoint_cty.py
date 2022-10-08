#!/usr/bin/python3

import sys
import json
from flask import Flask, g, session, make_response
from flask import abort
#from flask import Blueprint
from flask import request
from flask_restplus import Resource, Api, reqparse

from core.appinfo import AppInfo
from services.fetchxml import build_fetchxml_by_alias
from services.database import DatabaseServices
from core.fetchxmlparser import FetchXmlParser
from core.jsontools import json_serial
from core.exceptions import RestApiNotAllowed
from core import log
from core.file import File
from core.plugin import Plugin

logger=log.create_logger(__name__)

def create_parser_post():
    parser=reqparse.RequestParser()
    return parser

class TuxlogCty(Resource):
    api=AppInfo.get_api()

    @api.doc(parser=create_parser_post())
    def post(self):
        try:
            context=g.context
            connection=context.get_connection()

            for f in request.files.getlist('file'):
                content=str(f.read(),'UTF-8')
                plugin=Plugin(context, "tuxlog_cty_endpoint", "post")
                plugin.execute("before", {"data": {"content": content}})


            return make_response(dict({"results": "" ,"status":"ok"}) ,200)

        except RestApiNotAllowed as err:
            abort(400, f"{err}")
        except Exception as err:
            abort(500,f"{err}")

def get_endpoint():
    return TuxlogCty
