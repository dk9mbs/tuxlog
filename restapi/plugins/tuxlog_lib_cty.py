import sys
import json
import time
import argparse
import os
import signal
import logging
import os
import config
from os import getenv


class CtyImport:

    def __init__(self, context, fn_read_country_callback=None, fn_read_prefix_callback=None):
        self._fn_country=fn_read_country_callback
        self._fn_prefix=fn_read_prefix_callback
        self._context=context

    def parse(self, content, **kwargs):
        user_data=None
        if 'user_data' in kwargs:
            user_data=kwargs['user_data']

        content=content.split('\n')

        @CtyImportLib
        def test(country, **kwargs):
            user_data=None
            if 'user_data' in kwargs:
                user_data=kwargs['user_data']

            dxcc={}
            dxcc['continent']=country['continent']
            dxcc['country']=country['country']
            dxcc['cq_zone']=country['cq']
            dxcc['itu_zone']=country['itu']
            dxcc['time_offset']=float(country['time_offset']) 
            dxcc['longitude']=float(country['longitude'])
            dxcc['latitude']=float(country['latitude'])
            dxcc['entity']=0

            if not 'id' in dxcc:
                dxcc['id']=country['prefix']

            if self._fn_country!=None:
                self._fn_country(self._context,dxcc)


            for item in country['prefixes']:
                prefix=item['prefix']
                exact_match=item['match']
                if exact_match==True:
                    exact_match=1
                else:
                    exact_match=0
                exists=True

                dxcc_pref={}
                dxcc_pref['dxcc_id']=country['prefix']
                dxcc_pref['cq_zone']=country['cq']
                dxcc_pref['itu_zone']=country['itu']
                dxcc_pref['time_offset']=float(country['time_offset'])
                dxcc_pref['entity']=0

                dxcc_pref['id']=f"{prefix}"

                dxcc_pref['exact_match']=exact_match

                if self._fn_prefix!=None:
                    self._fn_prefix(self._context, dxcc, dxcc_pref)

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

