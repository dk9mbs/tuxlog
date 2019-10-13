#!/usr/bin/python3.5

from __future__ import print_function

import sys
import json
import time
import argparse
import os
import signal
import logging

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



if __name__=="__main__":
    with open('/tmp/cty.dat', 'r') as file:
        content=file.readlines()

        @CtyImportLib
        def test(country, **kwargs):
            print('%s => %s (%s) offset:%s' % (country['prefix'], country['country'], country['continent'], country['time_offset'])  )
            pass

        test(content)