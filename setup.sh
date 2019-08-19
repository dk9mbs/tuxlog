#!/bin/bash

mkdir -p /etc/tuxlog
cp ./tuxlog_cfg.json /etc/tuxlog/





#! /usr/bin/python3.5

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/tmp/virtenv/tuxlog/')
from my_flask_app import app as application
application.secret_key = 'anything you wish'

