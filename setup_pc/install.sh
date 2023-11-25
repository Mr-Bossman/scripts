#!/bin/bash
mkdir /tmp/setup_pc/
cd /tmp/setup_pc/
sudo apt update
wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -O chrome.deb
wget "https://discord.com/api/download?platform=linux&format=deb" -O discord.deb
wget "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64" -O vscode.deb
wget "https://get.skype.com/getskype-webwrap-deb" -O skype.deb
wget "https://launcher.mojang.com/download/Minecraft.deb" -O minecraft.deb

cat bashrc >> ~/.bashrc
cat bash_aliases >> ~/.bash_aliases
cp gitconfig ~/.gitconfig
cp ssh_config ~/.ssh/config
cp -bS.bak tmux.conf ~/tmux.conf
cp -abS.bak config ~/.config
sudo cp -bS.bak sshd_config /etc/ssh/sshd_config
