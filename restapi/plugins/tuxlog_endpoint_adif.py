#!/usr/bin/python3

import sys
import json
from flask import Flask, g, session, make_response
from flask import abort
from flask import Blueprint
from flask import request
from flask_restplus import Resource, Api, reqparse
from flaskext.mysql import MySQL

from core.appinfo import AppInfo
from services.fetchxml import build_fetchxml_by_alias
from services.database import DatabaseServices
from core.fetchxmlparser import FetchXmlParser
from core.jsontools import json_serial
from core.exceptions import RestApiNotAllowed
from core import log

from plugins.tuxlog_lib_adifparserlib import AdifParserLib
from core.file import File
from tuxlog_lib_adifmapping import AdifMappingTools

logger=log.create_logger(__name__)

def create_parser_post():
    parser=reqparse.RequestParser()
    return parser

class TuxlogAdif(Resource):
    api=AppInfo.get_api()

    @api.doc(parser=create_parser_post())
    def post(self):
        try:
            context=g.context
            connection=context.get_connection()

            fetch=f"""
            <restapi type="select">
                <table name="log_data_exchange_fields"/>
                <filter>
                    <condition field="converter_id" operator="eq" value="adif_v2"/>
                </filter>
            </restapi>
            """
            fetchparser=FetchXmlParser(fetch,context)
            rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)

            mapping=rs.get_result()
            mapped_rec={}

            for f in request.files.getlist('file'):
                mapped_rec={}

                @AdifParserLib
                def parser(*args, **kwargs):
                    mapped_rec=AdifMappingTools.map(args[0],mapping)
                    #logger.info(mapped_rec)
                    fetch=build_fetchxml_by_alias(context,"log_logs",None, mapped_rec, type="insert")
                    fetchparser=FetchXmlParser(fetch, context)
                    #logger.info(fetch)
                    DatabaseServices.exec(fetchparser,context,fetch_mode=0, run_as_system=True)

                parser( str(f.read(),'UTF-8'), 0 )

            return make_response(dict({"results": mapped_rec,"status":"ok"}) ,200)

        except RestApiNotAllowed as err:
            abort(400, f"{err}")
        except Exception as err:
            abort(500,f"{err}")

def get_endpoint():
    return TuxlogAdif
