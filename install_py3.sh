# 仅在ubuntu20.04下测试，其余系统版本未实机测试
sudo apt update
sudo apt-get -y install build-essential libssl-dev libbz2-dev libsqlite3-dev libreadline-dev zlib1g-dev libffi-dev libncurses5-dev
sudo apt-get -y install gcc make zip unzip
cd ./Python3/
rm -rf ./Python-3.8.18
rm -rf /usr/local/python3.8
sudo mkdir /usr/local/python3.8
tar -zxvf ./Python-3.8.18.tgz
cd ./Python-3.8.18
./configure --prefix=/usr/local/python3.8
make -j6 && make install
sudo rm -f /usr/bin/python3
sudo rm -f /usr/bin/pip3
sudo ln -s /usr/local/python3.8/bin/python3.8 /usr/bin/python3
sudo ln -s /usr/local/python3.8/bin/pip3.8 /usr/bin/pip3
pip3 config --global set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
cd ..
cd ..
python3 ./Simulation.py
