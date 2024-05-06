#!/bin/bash
groups | grep sudo &>/dev/null || echo "Run \`su root -c \"usermod -aG sudo $(whoami)\"\` and re-log." && exit
mkdir /tmp/setup_pc/
cd /tmp/setup_pc/
sudo apt-add-repository -ync non-free contrib non-free-firmware
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install git
sudo apt install -y $(cat packages)
sudo apt autoremove

#sudo add-apt-repository -yn ppa:obsproject/obs-studio
#sudo add-apt-repository -yn ppa:kicad/kicad-8.0-releases
# replace with lunar of the closest ubuntu release

#sudo apt install kicad kicad-packages3d kicad-doc obs-studio
# deb [signed-by=/etc/apt/keyrings/lutris.gpg] https://download.opensuse.org/repositories/home:/strycore/Debian_12/ ./

sudo usermod -aG tty $(whoami)
sudo usermod -aG libvirt $(whoami)

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
dconf load /org/gnome/terminal/ < gnome-terminal.properties
wget -nc https://jachan.dev/images/gate.jpg -O ~/Pictures/

for i in $(seq 1 254); do
for j in $(seq 1 254); do
echo h$i.$j 10.4.$i.$j >> ~/.hosts
done
done
