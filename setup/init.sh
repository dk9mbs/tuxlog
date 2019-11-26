#!/bin/bash

BASEDIR=$(dirname "$0")
SCRIPT=$(readlink -f $0)
APPDIR=$(dirname $SCRIPT)
APPDIR=$(dirname $APPDIR)

echo "====================="
echo "$SCRIPT"
echo "$APPDIR"
echo "====================="

# npm und nodejs installieren
# https://debianforum.de/forum/viewtopic.php?t=172240
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -
apt-get update
apt-get install -y nodejs gcc g++ make mycli default-mysql-client
npm install -g @vue/cli

cd $APPDIR
python3 -m venv virtenv
chmod 0755 ./virtenv
source virtenv/bin/activate

pip3 install --upgrade pip
export NO_SQLITE=1
pip3 install -r requirements.txt

echo "========================================="
echo "========================================="
echo "========================================="
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo "                 =======                 "
echo ""
echo "Thank you for installing tuxLog!"
echo "pse run integrationtest.sh first then"
echo "run install.sh"
echo ""
echo "vy 73 de DK9MBS / KI5HDH"
