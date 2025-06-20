#!/bin/bash

BASEDIR=$(dirname "$0")
PROT="http"
ENVIRONMENT=$1
FUNCTION=$2
PARAMS=$($BASEDIR/urlencode.py $3)
FILENAME=$4

HOST=$($BASEDIR/cfgreader.py /etc/tuxlog/tuxlog_cfg.json $ENVIRONMENT client host)
PORT=$($BASEDIR/cfgreader.py /etc/tuxlog/tuxlog_cfg.json $ENVIRONMENT client port)
USERNAME=$($BASEDIR/cfgreader.py /etc/tuxlog/tuxlog_cfg.json $ENVIRONMENT client username)
PASSWORD=$($BASEDIR/cfgreader.py /etc/tuxlog/tuxlog_cfg.json $ENVIRONMENT client password)

URL="$PROT://$USERNAME:$PASSWORD@$HOST:$PORT/api/v1.0/webfunction/$FUNCTION?params=$PARAMS"

echo "$1" >&2
echo "$PARAMS" >&2
echo "URL => $URL" >&2

#wget  -O - "$URL" 

if [[ ! -z "$FILENAME" ]] 
then
    wget --header "content-type:text/cty" --post-file=$FILENAME  -O - "$URL" 
elif [ -z "$FILENAME" ]
then
    wget -O - "$URL" 
fi

echo ""
