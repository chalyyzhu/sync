#!/bin/bash
DIR="/root/sync"

user_data(){
    read -p "Masukan private key nya > " private_key
    clear
    echo "pilih mode..!"
    echo
    echo "1. Mode WS"
    echo "2. Mode SSL"
    echo "3. Mode Proxy"
    echo
    read -p "Select From Options [1-2 or ctrl +c for exit] :  " opt_mode
    case $opt_mode in
    1)
    mode="ws"
    ;;
    2)
    mode="ssl"
    ;;
    3)
    mode="proxy"
    clear
    read -p "Masukan Proxy nya.. > " proxy
    printf %s $proxy > ${DIR}/proxy
    ;;
    *)
    echo "Input The Correct Number !"
    exit
    ;;
    esac
    clear
    read -p "Masukan bug nya.. > " bug
    clear
    echo "======== USER SETTINGS ========="
    echo
    echo "• PRIVATE KEY : $private_key"
    echo "• MODE         : $mode"
    echo "• BUG         : $bug"
    echo "• PROXY         : $proxy"
    echo
    echo "================================"
    echo
}

write_data(){
  json=$(cat <<-END
{
    "private_key": "$private_key",
    "mode_": "$mode",
    "file_public": ["sync.yaml"],
    "file_private": ["zhoe.yaml"],
    "time_loop": 10
    
}
END
)
  printf %s "${json}" > ${DIR}/config.json
  printf %s $bug > ${DIR}/bug.txt
}

setup(){
    if [ -d "$DIR" ]; then
      rm -rf "$DIR"
      mkdir -p "$DIR"
      echo "Renstalling .. [+]"
    else
      mkdir -p "$DIR"
      echo "Installing .. [+]"  
    fi
    write_data
    
    opkg update && opkg install python3 && opkg install python3-pip
    pip3 install requests
    
    wget "https://raw.githubusercontent.com/chalyyzhu/sync/main/autostart-sync" -O /etc/init.d/autostart-sync
    wget "https://raw.githubusercontent.com/chalyyzhu/sync/main/sync.py" -O "${DIR}/sync.py"
    
    chmod +x /etc/init.d/autostart-sync 
    /etc/init.d/autostart-sync enable
    /etc/init.d/autostart-sync start
    
    wget "https://raw.githubusercontent.com/chalyyzhu/sync/main/opreker" -O /usr/bin/opreker
    chmod +x /usr/bin/opreker
    
    echo "INSTALATION SUCESS.. [+]"
    rm install.sh
}


main(){
    user_data
    read -p "Apakah datanya konfigurasinya sudah benar? (y/n)? " answer
    case ${answer:0:1} in
      y|Y )
        setup
      ;;
      * )
        echo "Seting ulang datamu...!"
        user_data
      ;;
    esac
}

main

