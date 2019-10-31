#!/usr/bin/python3.5

from __future__ import print_function
import json
import os
import sys

cfg_file=sys.argv[1]
environment=sys.argv[2]

with open (cfg_file, 'r') as json_cfg:
    cfg=json.load(json_cfg)

print("reading "+sys.argv[3]+"."+sys.argv[4]+" from "+sys.argv[2]+" ("+sys.argv[2]+")", file=sys.stderr)

print(cfg[sys.argv[2]][sys.argv[3]][sys.argv[4]])
