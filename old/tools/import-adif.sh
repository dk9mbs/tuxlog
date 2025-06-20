#!/bin/bash

ENVIRONMENT=$1
LOGBOOK=$2
IMPORTDIR=$3
BASEDIR=$(dirname "$0")
#SERVER=$2
#USERNAME=$3
#PASSWORD=$4
echo "Importdirectory => $IMPORTDIR"

for i in $IMPORTDIR/*.adi; do
    echo "importing => $i ..."
    #wget --debug --header "content-type:text/adif" --post-file $i -O - http://$USERNAME:$PASSWORD@$SERVER/api/v1.0/import/LogLogs?logbook_id=$LOGBOOK >> /tmp/import_adif.log

    $BASEDIR/webfn-proxy.sh $ENVIRONMENT import_adif "{\"logbook_id\":\"$LOGBOOK\"}" $i
    ERRCODE=$?

    if [ $ERRCODE == "0" ] 
    then
        echo "Import OK renaming importfile!"
    	mv $i "$1.imported"
    fi


    echo "============================================="
done
