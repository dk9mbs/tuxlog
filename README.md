# tuxlog

## Install
```bash
#!/bin/bash

# npm und nodejs installieren
# https://debianforum.de/forum/viewtopic.php?t=172240
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -
apt-get update
apt-get install nodejs npm

npm install -g @vue/cli

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
./integrationtest.sh
./install.sh
```


## ToDo

* pip3 install venv
* pip3 install pexpect
* apt-get install rigctld
* apt-get install mod-wsgi
* 
* vue create vue-proj
* npm run build && npm run serve 



## How to import adif data

```bash
wget --debug --header "content-type:text/adif" --post-file /tmp/wsjtx_log.adi -O - http://localhost:8081/api/v1.0/import/LogLogs?logbook_id=dk9mbs 
```
