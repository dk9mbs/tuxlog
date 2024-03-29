# tuxlog

## Install
```bash
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

cd /tmp
python3 -m venv virtenv
chmod 0755 ./virtenv
cd virtenv
git clone https://github.com/dk9mbs/tuxlog.git
cd tuxlog
export NO_SQLITE=1
../bin/pip3 install -r requirements.txt

./setup
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
```


## ToDo

* pip3 install venv
* 
* apt-get install rigctld
* apt-get install mod-wsgi
* 
* vue create vue-proj
* 

## How to run as apache2 www-server

```bash
<VirtualHost *:80>
     # Add machine's IP address (use ifconfig command)
     ServerName tuxlog.servername.de
     # Give an alias to to start your website url with
     WSGIScriptAlias / /var/www/tuxlog/app.wsgi
     <Directory /var/www/tuxlog/>
                # set permissions as per apache2.conf file
            Options FollowSymLinks
            AllowOverride None

            AuthType Basic
            AuthName "Private Documentation Repository"
            AuthUserFile /etc/.htusers
            Require valid-user
            #Require all granted
     </Directory>
     ErrorLog ${APACHE_LOG_DIR}/error.log
     LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```


## How to import adif data?

```bash
./webfn-proxy.sh build import_adif '{"logbook_id":"dk9mbs"}' /tmp/wsjtx_log.adi (deprecated)
python adifimport.py username password https://test.de/api ~/.local/share/WSJT-X/wsjtx_log.adi
```
## How to import cty.dat?

```bash
./webfn-proxy.sh build import_ctydat '{}' /tmp/cty.dat
```


## what is RST(TX) and RST(RX) 

TX(RST) is "sent". RX(RST) is "received". So your outgoing RST goes in TX(RST). Your incoming RST, as given by the other station, goes in RX(RST).


## How to get cty.dat file?

http://www.country-files.com/dx-cluster/dx-spider/
