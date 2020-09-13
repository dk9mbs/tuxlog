#!/bin/bash

if [ -z $RESTAPIPATH ];
then
    echo "please source init.sh from restapi project"
fi

export PYTHONPATH=../plugins:$PYTHONPATH
echo "$PYTHONPATH"

python -m unittest discover -v
