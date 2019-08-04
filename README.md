# tuxlog

## Install
´´´bash
cd /tmp
python3 -m venv virtenv
cd virtenv
git clone https://github.com/dk9mbs/tuxlog.git
cd tuxlog
../bin/pip3 -r requirements.txt
cd setup
./pipeline
´´´


## ToDo

requets is missing in /requirements.txt
sudo apt-get install expect


## How to import adif data

wget --debug --header "content-type:text/adif" --post-file /tmp/wsjtx_log.adi -O - http://localhost:8081/api/v1.0/tuxlog/LogLogs?logbook_id=dk9mbs 

