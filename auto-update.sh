#!/bin/bash
out=/home/jesse/verus
function install(){
    echo installing
    cat <<EOF > /usr/lib/systemd/system/verus.service 
[Unit]
Description=verusd
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/bin/verusd

[Install]
WantedBy=multi-user.target
EOF
    touch $out/verus-cli/verusd 
    ln -s $out/verus-cli/verusd /bin/verusd
    systemctl daemon-reload 
    systemctl enable verus
}
ver=`curl -s https://api.github.com/repos/VerusCoin/VerusCoin/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")'`
test -f /var/ver || touch /var/ver
test -f  /usr/lib/systemd/system/verus.service || install
cur=`cat /var/ver`
if [[ $ver != $cur ]]; then
    file=`curl -s https://api.github.com/repos/VerusCoin/VerusCoin/releases/latest | awk '/browser_download_url/ && /x86_64/ {print $2}' | tr -d '"'`
    wget $file -P /tmp
    file=`basename $file`
    tar -xvf /tmp/$file -C /tmp
    systemctl stop verus
    tar -xvf  /tmp/"${file%.*}".tar.gz -C $out
    systemctl start verus
    rm  /tmp/${file%.*}*
    echo $ver > /var/ver
fi
