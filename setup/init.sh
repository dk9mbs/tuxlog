#!/bin/bash

# npm und nodejs installieren
# https://debianforum.de/forum/viewtopic.php?t=172240
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -
apt-get update
apt-get install -y nodejs gcc g++ make

#git clone https://github.com/coleifer/peewee.git
#cd peewee
#python setup.py install

npm install -g @vue/cli

#cd /tmp
cd ../
python3 -m venv virtenv
chmod 0755 ./virtenv
source virtenv/bin/activate
#cd virtenv
#git clone https://github.com/dk9mbs/tuxlog.git
#cd tuxlog
export NO_SQLITE=1
#../bin/pip3 install -r requirements.txt
pip3 install -r requirements.txt

#./setup
#
# configure manually /etc/tuxlog/tuxlog_cfg.json
#
cd setup
./integrationtest.sh
./install.sh

#cd ../vue-ui
cd ../tuxlog/__solution__/ui_/vue-ui
npm install
npm run build
