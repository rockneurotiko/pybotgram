#!/usr/bin/env bash
THIS_DIR=$(cd $(dirname $0); pwd)
RAM=`grep MemTotal /proc/meminfo | awk '{print $2}'`
cd $THIS_DIR

update() {
    git pull
    git submodule update --init --recursive
    pip3 install -r requirements.txt
}

install_no_lua() {
    if [ $RAM -lt 307200 ]; then
        ./configure --disable-extf --disable-liblua && make
    else
        ./configure --disable-liblua && make
    fi
    if [ $? -ne 0 ];then
        echo "Error installing tg"; exit $RET;
    fi
}

install() {
    virtualenv-3.4 env
    source env/bin/activate
    update
    if [ $RAM -lt 307200 ]; then
        cd tg && ./configure --disable-extf && make
    else
        cd tg && ./configure && make
    fi
    if [ $? -ne 0 ]; then
       install_no_lua
    fi
    cd ..
}

if [ "$1" = "install" ]; then
    install
elif [ "$1" = "update" ]; then
    update
else
    if [ ! -f ./tg/telegram.h ]; then
        echo "tg not found"
        echo "Run $0 install"
        exit 1
    fi
    if [ ! -f ./tg/bin/telegram-cli ]; then
        echo "tg binary not found"
        echo "Run $0 install"
        exit 1
    fi
    if [ ! -f env/bin/activate ]; then
        echo "You need virtualenv in env directory"
        echo "Run virtualenv-3.4 env"
        exit 1
    fi
    source env/bin/activate
    ./tg/bin/telegram-cli -k ./tg/tg-server.pub -Z bot/bot.py -l 1 -E
fi
