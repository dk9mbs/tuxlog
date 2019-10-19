#!/bin/bash

IMPORTDIR=$1
SERVER=$2
USERNAME=$3
PASSWORD=$4
LOGBOOK=$5
echo "Importdirectory => $IMPORTDIR"

for i in $1/*.adi; do
    echo "importing => $i ..."
    wget --debug --header "content-type:text/adif" --post-file $i -O - http://$USERNAME:$PASSWORD@$SERVER/api/v1.0/import/LogLogs?logbook_id=$LOGBOOK >> /tmp/import_adif.log
    ERRCODE=$?

    if [ $ERRCODE == "0" ] 
    then
        echo "Import OK renaming importfile!"
    	mv $i "$1.imported"
    fi


    echo "============================================="
done
