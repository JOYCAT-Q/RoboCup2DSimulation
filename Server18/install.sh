#!/bin/bash

#更换系统镜像源 
#modified by Joycat
#time:23/9/24
sudo cp /etc/apt/sources.list /etc/apt/sources.backup.list
sudo rm -f /etc/apt/sources.list
sudo cp ./sources_U22.04.list /etc/apt/sources.list
sudo chmod 777 /etc/apt/sources.list

#download predependency
sudo apt-get update
sudo apt-get -y install -f
sudo apt-get -y install build-essential 
sudo apt-get -y install libboost-all-dev 
sudo apt-get -y install autoconf 
sudo apt-get -y install automake 
sudo apt-get -y install libtool
sudo apt-get -y install flex
sudo apt-get -y install bison
sudo apt-get -y install libfontconfig1-dev
sudo apt-get -y install libaudio-dev
sudo apt-get -y install libxt-dev
sudo apt-get -y install libglib2.0-dev
sudo apt-get -y install libxi-dev
sudo apt-get -y install libxrender-dev
sudo apt-get -y install qtbase5-dev
sudo apt-get -y install qt5-qmake
sudo apt-get -y install g++
#download tools
sudo apt-get -y install rar unrar p7zip
sudo apt-get -y install libfreetype6-dev
sudo apt-get -y install zlib*
sudo apt-get -y install libpng-dev
sudo apt install -y vim qtcreator 
sudo apt install -y python-setuptools
sudo apt install -y python3-dev
sudo apt install -y python3-pip
sudo pip3 install --upgrade pip
#删除 APT 的锁文件,因為有时这个文件可能被损坏或无法获取锁,从而导致其他 APT 命令无法执行
sudo rm /var/cache/apt/archives/lock
#删除 dpkg 的锁文件,确保可以正常获取锁
sudo rm /var/lib/dpkg/lock
#配置所有因某些原因而被中断了的安装过程
sudo dpkg --configure -a
#清理旧的已下载的软件包
sudo apt-get autoclean
#清理全部已下载的软件包
sudo apt-get clean

#librcsc
if [ -d librcsc-rc2023 ]
then 
	rm -r librcsc-rc2023
fi
tar -zxvf librcsc-rc2023.tar.gz
cd librcsc-rc2023
./bootstrap
./configure --disable-unit-test
make -j$(nproc)
sudo make install
cd ..

#rcssserver
if [ -d rcssserver-18.1.3 ]
then 
	rm -r rcssserver-18.1.3
fi
tar xzvfp rcssserver-18.1.3.tar.gz
cd rcssserver-18.1.3
./configure
make -j$(nproc)
sudo make install
sudo ldconfig
cd ..

#rcssmonitor
if [ -d rcssmonitor-18.0.0 ]
then 
	rm -r rcssmonitor-18.0.0
fi
tar xzvfp rcssmonitor-18.0.0.tar.gz
cd rcssmonitor-18.0.0
./configure
make -j$(nproc)
sudo make install
sudo ldconfig
cd ..

#rcsslogplayer
#缺失qt4 core library
#if [ -d rcsslogplayer-15.2.1 ]
#then 
#	rm -r rcsslogplayer-15.2.1
#fi
#tar xzvfp rcsslogplayer-15.2.1.tar.gz
#cd rcsslogplayer-15.2.1
#./configure
#make -j$(nproc)
#sudo make install
#sudo ldconfig
#cd ..

#fedit2
if [ -d fedit2-support-v18 ]
then 
	rm -r fedit2-support-v18
fi
tar -zxvf fedit2-support-v18.tar.gz
cd fedit2-support-v18
./bootstrap
./configure
make -j$(nproc)
sudo make install
cd ..

#soccerwindow2
if [ -d soccerwindow2-rc2023 ]
then 
	rm -r soccerwindow2-rc2023
fi
tar -zxvf soccerwindow2-rc2023.tar.gz
cd soccerwindow2-rc2023
./bootstrap
./configure
make -j$(nproc)
sudo make install


sudo ldconfig

echo "Successful! Enjoy Yourself!"
