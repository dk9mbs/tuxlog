# tuxlog

## Install

## ToDo

requets is missing in /requirements.txt


## How to import adif data

wget --debug --header "content-type:text/adif" --post-file /tmp/wsjtx_log.adi -O - http://localhost:8081/api/v1.0/tuxlog/LogLogs?logbook_id=dk9mbs 

