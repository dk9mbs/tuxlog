#!/bin/bash

ENVIRONMENT=$1

if [ -z $ENVIRONMENT ]; then
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "!                                                     !"
    echo "! Missing argument: environment. Call install.sh test !"
    echo "!                                                     !"
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    exit
fi

PYTHON="python3.5"
BASEDIR=$(dirname "$0")
SCRIPT=$(readlink -f $0)
APPDIR=$(dirname $SCRIPT)
APPDIR=$(dirname $APPDIR)
CFG_FILE="/etc/tuxlog/tuxlog_cfg.json"
KEY=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" "security" "secret_key")
DATABASE=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" mysqlcfg database)
USERNAME=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" mysqlcfg username)
PASSWORD=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" mysqlcfg password)
HOST=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" mysqlcfg host)

echo ""
echo "========================================================"
echo "Environment.....:$ENVIRONMENT"
echo "Script base dir.:$BASEDIR"
echo "App base dir....:$APPDIR"
echo "Secret Key......:$KEY"
echo "Database........:$DATABASE"
echo "Hot.............:$HOST"
echo "Username........:$USERNAME"
echo "Password........:*********"
echo "========================================================"


mkdir -p /etc/tuxlog

if [ ! -f /etc/tuxlog/tuxlog_cfg.json ]; then
    cp "$BASEDIR/tuxlog_cfg.json" /etc/tuxlog/
fi


cat > "$APPDIR/app.wsgi" << EOF
#! /usr/bin/python3.5

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "$APPDIR/")
from app import app as application
application.secret_key = "$KEY"
EOF



cd $BASEDIR
$BASEDIR/pwizproxy.py $PYTHON $HOST $DATABASE $USERNAME $PASSWORD "../model/model.py"

