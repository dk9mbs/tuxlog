from __future__ import print_function
import json
import os
import sys

cfg_file=sys.argv[1]

with open (cfg_file, 'r') as json_cfg:
    cfg=json.load(json_cfg)

print("reading "+sys.argv[2]+"."+sys.argv[3]+" from "+sys.argv[1], file=sys.stderr)

print(cfg[sys.argv[2]][sys.argv[3]])
