#! /usr/bin/python3.5

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/dk9mbs/src/tuxlog/")
#from app import app as application
from common.app import app as application
application.secret_key = ""
