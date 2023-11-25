#!/bin/bash
groups | grep sudo &>/dev/null || echo "Run \`su root -c \"usermod -aG sudo $(whoami)\"\` and re-log." && exit
mkdir /tmp/setup_pc/
cd /tmp/setup_pc/
sudo apt-add-repository -ync non-free contrib non-free-firmware
sudo apt update
sudo apt install git
sudo apt install -y $(cat packages)
sudo apt autoremove

wget -nc "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -O chrome.deb
wget -nc "https://discord.com/api/download?platform=linux&format=deb" -O discord.deb
wget -nc "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64" -O vscode.deb
wget -nc "https://get.skype.com/getskype-webwrap-deb" -O skype.deb
wget -nc "https://launcher.mojang.com/download/Minecraft.deb" -O minecraft.deb

cat bashrc >> ~/.bashrc
cat bash_aliases >> ~/.bash_aliases
cp gitconfig ~/.gitconfig
cp ssh_config ~/.ssh/config
cp -bS.bak tmux.conf ~/.tmux.conf
cp -abS.bak config/* ~/.config
sudo cp -bS.bak sshd_config /etc/ssh/sshd_config
