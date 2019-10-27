import sys
import json
import time
import argparse
import os
import signal
import logging
import os
import config
from model import model
from model.model import MySQLDatabase
from os import getenv
from common.common import BaseUseCase


class CtyImport(BaseUseCase):

    def execute(self, content, **kwargs):
        user_data=None
        if 'user_data' in kwargs:
            user_data=kwargs['user_data']

        content=content.split('\n')

        @CtyImportLib
        def test(country, **kwargs):
            user_data=None
            if 'user_data' in kwargs:
                user_data=kwargs['user_data']
            dxcc=model.LogDxcc.get_or_none(model.LogDxcc.id==country['prefix'])
            if dxcc==None:
                dxcc=model.LogDxcc()

            dxcc.continent=country['continent']
            dxcc.country=country['country']
            dxcc.cq_zone=country['cq']
            dxcc.itu_zone=country['itu']
            dxcc.time_offset=float(country['time_offset']) 
            dxcc.longitude=float(country['longitude'])
            dxcc.latitude=float(country['latitude'])
            dxcc.entity=0

            if dxcc.id==None:
                dxcc.id=country['prefix']
                dxcc.save(force_insert=True)
            else:
                dxcc.save()


            for item in country['prefixes']:
                prefix=item['prefix']
                exact_match=item['match']
                exists=True

                dxcc_pref=model.LogDxccPrefixes.get_or_none(model.LogDxccPrefixes.id==prefix)
                if dxcc_pref==None:
                    exists=False
                    dxcc_pref=model.LogDxccPrefixes()           

                dxcc_pref.dxcc_id=country['prefix']
                dxcc_pref.cq_zone=country['cq']
                dxcc_pref.itu_zone=country['itu']
                dxcc_pref.time_offset=float(country['time_offset']) 
                dxcc_pref.entity=0
                dxcc_pref.id=prefix
                dxcc_pref.exact_match=exact_match
                dxcc_pref.save(force_insert=not exists)

            self._execute('after_save_cty_rec', record=country, user_data=user_data)
            pass

        test(content, user_data=user_data)



class CtyImportLib:
    def __init__(self, fn):
        self.fn=fn
        pass

    '''
    Read a complete cty.dat.
    content
    '''
    def __call__(self, *args, **kwargs):
        content=args[0]
        prefixes=''
        country=''

        for line in content:
            line=line.replace('\n', '').replace('\r', '')
            if line.find(":")>-1:
                prefixes=''
                country=line
            else:
                prefixes=prefixes+line.strip()
                if line.strip().endswith(';'):
                    prefixes=prefixes[:-1]
                    cty = self.__line_to_list(country, prefixes)
                    self.fn(cty, **kwargs)


    def __line_to_list(self, country_line, prefixes_line):
        cty=country_line.strip().split(':')
        prefixes_list=prefixes_line.strip().split(',')
        country=dict()

        prefix=cty[7].strip()
        darc=False
        cq=cty[1].strip()
        itu=cty[2].strip()
        continent=cty[3].strip()
        latitude=cty[4].strip()
        longitude=cty[5].strip()
        time_offset=cty[6].strip()

        if prefix.startswith('*'):
            prefix=prefix[1:]
            darc=True

        for x in range(len(prefixes_list)):
            item=dict()
            sub_prefix=prefixes_list[x]
            match=False

            if sub_prefix.strip().startswith('='):
                match=True
                sub_prefix=sub_prefix[1:]

            square_bracket_open=sub_prefix.find('[')
            if square_bracket_open > -1:
                sub_prefix=sub_prefix[0:square_bracket_open]

            round_bracket_open=sub_prefix.find('(')
            if round_bracket_open > -1:
                sub_prefix=sub_prefix[0:round_bracket_open]

            item['prefix']=sub_prefix
            item['match']=match
            prefixes_list[x]=item

        country['prefix']=prefix
        country['darc']=darc
        country['country']=cty[0]
        country['cq']=cq
        country['itu']=itu
        country['continent']=continent
        country['latitude']=latitude
        country['longitude']=longitude
        country['time_offset']=time_offset



        country['prefixes']= prefixes_list

        return country

