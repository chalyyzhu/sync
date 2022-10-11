#!/bin/bash


DIR="/root/sync"

if [ -d "$DIR" ]; then
   rm -rf "$DIR"
   mkdir -p "$DIR"
   echo "Renstalling .. [+]"
else
   mkdir -p "$DIR"
   echo "Installing .. [+]"  
fi

opkg update
opkg install python3 && opkg install python3-pip
pip3 install requests

wget "https://raw.githubusercontent.com/chalyyzhu/sync/main/bug.txt" -O "${DIR}/bug.txt"
wget "https://raw.githubusercontent.com/chalyyzhu/sync/main/config.json" -O "${DIR}/config.json"

wget "https://raw.githubusercontent.com/chalyyzhu/sync/main/autostart-sync" -O /etc/init.d/autostart-sync
wget "https://raw.githubusercontent.com/chalyyzhu/sync/main/sync.py" -O "${DIR}/sync.py"

chmod +x /usr/bin/sync
chmod +x /etc/init.d/autostart-sync 
/etc/init.d/autostart-sync enable
/etc/init.d/autostart-sync start

wget "https://raw.githubusercontent.com/chalyyzhu/sync/main/opreker" -O /usr/bin/opreker
chmod +x /usr/bin/opreker

echo "INSTALATION SUCESS.. [+]"
rm install.sh
