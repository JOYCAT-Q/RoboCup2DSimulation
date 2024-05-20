#!/bin/bash

#更换系统镜像源 
#modified by Joycat
#time:23/9/24
sudo cp /etc/apt/sources.list /etc/apt/sources.backup.list
sudo rm -f /etc/apt/sources.list
sudo cp ./sources_U20.04.list /etc/apt/sources.list
sudo chmod 777 /etc/apt/sources.list

sudo apt-get update
sudo apt-get -y install -f
sudo apt-cache search boost
sudo apt-get -y install libboost-dev 
sudo apt-get -y install libboost-all-dev 
sudo apt-get -y install autoconf
sudo apt-get -y install libtool
sudo apt-get -y install g++ automake
#Ubuntu22.04版本后缺失
sudo add-apt-repository ppa:rock-core/qt4
sudo apt-get -y install libqt4-dev 
sudo apt-get -y install qt4-dev-tools qt4-doc qt4-designer
sudo apt-get -y install qt4-qtconfig libqt4-opengl-dev
sudo apt-get -y install libqt4-sql-mysql libqt4-sql-odbc libqt4-sql-psql libqt4-sql-sqlite 
sudo apt-get -y install qt5-default
#========================================================================================
sudo apt-get -y install rar unrar p7zip
sudo apt-get -y install build-essential
sudo apt-get -y install xorg-dev
sudo apt-get -y install libxt-dev
sudo apt-get -y install libxi-dev
sudo apt-get -y install libxrender-dev
sudo apt-get -y install flex bison 

sudo apt-get -y install libpng-dev
sudo apt-get -y install libglib2.0-dev
sudo apt-get -y install libaudio-dev
sudo apt-get -y install zlib*
sudo apt-get -y install libfreetype6-dev
sudo apt-get -y install libfontconfig1-dev

#extra add
sudo apt install -y vim qtcreator 
sudo apt install -y python-setuptools python-dev python3-dev
sudo apt install -y python3-pip 
sudo pip3 install --upgrade pip
#extra end

sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock
sudo dpkg --configure -a
sudo apt-get autoclean
sudo apt-get clean

#安装 bison
tar -xvaf bison-3.8.2.tar.gz
cd bison-3.8.2
./configure
sudo ldconfig
make -j4
sudo make install
cd ..

#安装 rcssserver
tar -xvaf rcssserver-17.0.0.tar.gz
cd rcssserver-17.0.0
./bootstrap
./bootstrap
./configure --with-boost-libdir=/usr/lib/x86_64-linux-gnu 
sudo ldconfig
make -j4
sudo make install
cd ..

#安装 rcsslogplayer
tar -xvaf rcsslogplayer-15.2.0.tar.gz
cd rcsslogplayer-15.2.0
./configure --disable-gl --with-boost-libdir=/usr/lib/x86_64-linux-gnu
sudo ldconfig
make -j4
sudo make install
cd ..


#安装 rcssmonitor
tar -xvaf rcssmonitor-17.0.0.tar.gz
cd rcssmonitor-17.0.0
./bootstrap
./bootstrap
./configure
sudo ldconfig
make -j4
sudo make install
cd ..


#安装librcsc 
tar -zxvf librcsc.tar.gz
cd librcsc
./bootstrap
./bootstrap
./configure
make -j4
sudo make install
cd ..


#安装 soccerwindow2
if [ -d soccerwindow2 ]
then 
	rm -r soccerwindow2
fi
tar -zxvf soccerwindow2.tar.gz
cd soccerwindow2
./bootstrap
./configure
make -j4
sudo make install
cd ..

#安装fedit2
tar -zxvf fedit2.tar.gz
cd fedit2
./bootstrap
./configure
make -j4
sudo make install
cd ..
#将lib添加到搜索路径

sudo echo "include /etc/ld.so.conf.d/*.conf
/usr/lib
/usr/local/lib
">ld.so.conf
sudo rm   /etc/ld.so.conf
sudo mv  ld.so.conf  /etc

sudo ldconfig
echo "success!"
#extra end



