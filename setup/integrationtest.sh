#!/bin/bash
PYTHON="python3.5"

CFG_FILE="/etc/tuxlog/tuxlog_cfg.json"
DATABASE="tuxlog_build"
USERNAME=$($PYTHON ./cfgreader.py $CFG_FILE build mysqlcfg username)
PASSWORD=$($PYTHON ./cfgreader.py $CFG_FILE build mysqlcfg password)
HOST=$($PYTHON ./cfgreader.py $CFG_FILE build mysqlcfg host)
BASEDIR=$(dirname "$0")
TESTDATA="/etc/tuxlog/test/logdatabase_testdata.db"

cd $BASEDIR

echo "Database........:$DATABASE"
echo "Hot.............:$HOST"
echo "Username........:$USERNAME"
echo "Password........:*********"
echo "Basedir.........:$BASEDIR"
echo "Testdata........:$TESTDATA"

echo "DROP DATABASE IF EXISTS $DATABASE ..."
mysql -u$USERNAME -p$PASSWORD -h$HOST -e "DROP DATABASE IF EXISTS $DATABASE;"
echo "CREATE DATABASE $DATABASE ..."
mysql -u$USERNAME -p$PASSWORD -h$HOST -e "CREATE DATABASE IF NOT EXISTS tuxlog_build default character set 'UTF8';"
echo "running sql script ..."
mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source ./logdatabase_init.db;"
mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source ./logdatabase.db;"
mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source ./logdatabase_update.db;"
mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source ./logdatabase_post.db;"

if [ -f $TESTDATA ] 
then
    echo "Executing Testdata script => $TESTDATA"
    mysql -u$USERNAME -p$PASSWORD -h$HOST $DATABASE -e "use $DATABASE;source $TESTDATA;"
    echo "Executed Testdata script => $TESTDATA"
fi

./pwizproxy.py $PYTHON $HOST $DATABASE $USERNAME $PASSWORD "../model/model.py"

cd ../tests/
export PYTHONPATH="../"
export tuxlog_environment="build"

$PYTHON -m unittest discover
TESTRESULT=$?

echo "Testresult => $TESTRESULT"

echo "executing local hooks scripts in /etc/tuxlog/build/"
if [ -d /etc/tuxlog/build/ ]; then
    echo "Hooks"
fi

echo "END of pipeline.sh"

