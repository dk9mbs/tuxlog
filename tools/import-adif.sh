#!/bin/bash

IMPORTDIR=$1
USERNAME=$2
PASSWORD=$3
LOGBOOK=$4
echo "Importdirectory => $IMPORTDIR"

for i in $1/*.adi; do
    echo "importing => $i ..."
    wget --debug --header "content-type:text/adif" --post-file $i -O - http://$USERNAME:$PASSWORD@localhost:5000/api/v1.0/import/LogLogs?logbook_id=$LOGBOOK
    echo "============================================="
done
