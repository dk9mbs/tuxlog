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
PIP="pip3"
BASEDIR=$(dirname "$0")
SCRIPT=$(readlink -f $0)
APPDIR=$(dirname $SCRIPT)
APPDIR=$(dirname $APPDIR)
CFG_FILE="/etc/tuxlog/tuxlog_cfg.json"

mkdir -p /etc/tuxlog
mkdir -p $APPDIR/htdocs

if [ ! -f /etc/tuxlog/tuxlog_cfg.json ]; then
    cp "$BASEDIR/tuxlog_cfg.json" /etc/tuxlog/
fi

cd $APPDIR
$PIP install -r requirements.txt

cd $APPDIR/setup/
KEY=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" "security" "secret_key")
DATABASE=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" mysqlcfg database)
USERNAME=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" mysqlcfg username)
PASSWORD=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" mysqlcfg password)
HOST=$($PYTHON ./cfgreader.py $CFG_FILE "$ENVIRONMENT" mysqlcfg host)

echo ""
echo "========================================================"
echo "Environment..........:$ENVIRONMENT"
echo "Script base dir......:$BASEDIR"
echo "App base dir.........:$APPDIR"
echo "Secret Key...........:$KEY"
echo "Database.............:$DATABASE"
echo "Hot..................:$HOST"
echo "Username.............:$USERNAME"
echo "Password.............:*********"
echo "========================================================"

echo "CREATE DATABASE $DATABASE ..."
mysql -u$USERNAME -p$PASSWORD -h$HOST -e "CREATE DATABASE IF NOT EXISTS $DATABASE default character set 'UTF8';"
echo "running sql script ..."
mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source ./logdatabase_init.db;"
mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source ./logdatabase.db;"
mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source ./logdatabase_update.db;"
mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source ./logdatabase_post.db;"




cat > "$APPDIR/app.wsgi" << EOF
#! /usr/bin/python3.5

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "$APPDIR/")
#from app import app as application
from common.app import app as application
application.secret_key = "$KEY"
EOF

#cd $APPDIR/vue-ui/
cd $APPDIR/tuxlog/__solution__/ui/vue-ui/
npm install
npm run build

cd $APPDIR/setup/
./pwizproxy.py $PYTHON $HOST $DATABASE $USERNAME $PASSWORD "../model/model.py"

