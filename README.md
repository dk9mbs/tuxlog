# tuxlog

## Install
```bash
#!/bin/bash

cd /tmp
python3 -m venv virtenv
cd virtenv
git clone https://github.com/dk9mbs/tuxlog.git
cd tuxlog
../bin/pip3 -r requirements.txt
./setup
#
# configure manually /etc/tuxlog/tuxlog_cfg.json
#
cd setup
./pipeline
```


## ToDo

* pip3 install venv
* pip3 install pexpect


## How to import adif data

wget --debug --header "content-type:text/adif" --post-file /tmp/wsjtx_log.adi -O - http://localhost:8081/api/v1.0/tuxlog/LogLogs?logbook_id=dk9mbs 

