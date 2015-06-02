#!/usr/bin/env bash
THIS_DIR=$(cd $(dirname $0); pwd)
RAM=`grep MemTotal /proc/meminfo | awk '{print $2}'`
VBIN=virtualenv-3.4
PYBIN=python


if ! hash $VBIN 2>/dev/null; then
    VBIN=virtualenv3
fi
if ! hash $VBIN 2>/dev/null; then
    VBIN=virtualenv
fi
if ! hash $VBIN 2>/dev/null; then
    echo "You have to install virtualenv"
    exit 1
fi

cd $THIS_DIR

update() {
    git pull
    git submodule update --init --recursive
    if [ ! -f ./env/bin/activate ]; then
        echo "You need virtualenv in env directory"
        echo "Run virtualenv -p python3 env"
        exit 1
    fi
    source env/bin/activate
    pip install -r requirements.txt
}

opt_install() {
    if [ ! -f ./env/bin/activate ]; then
        echo "You need virtualenv in env directory"
        echo "Run ./launch.sh install first"
        exit 1
    fi
    source env/bin/activate
    pip install -r opt_requirements.txt
}


install_no_lua() {
    if [ $RAM -lt 307200 ]; then
        ./configure --disable-extf --disable-liblua && make
    else
        ./configure --disable-liblua && make
    fi
    RET=$?
    if [ $RET -ne 0 ];then
        echo "Error installing tg"; exit $RET;
    fi
}


check_python3dev() {
    local res=1
    for python in python3.4 python3 python; do
        local path=`$python -c "from distutils.sysconfig import *; print(get_config_var('CONFINCLUDEPY'))"`
        if [[ $path == *"python3.4m"* ]]; then
            PYBIN=$python
            res=0
        fi
    done
    if [ $res -ne 0 ]; then
        echo "You need to install the python 3 libs, in ubuntu: 'sudo apt-get install python3-dev'"
        exit 1
    fi
}


install() {
    check_python3dev
    $VBIN -p python3 env
    RET=$?
    if [ $RET -ne 0 ]; then
        echo "Error creating the virtualenv with python 3, check the install instructions"; exit $RET
    fi
    update
    check_python3dev
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
elif [ "$1" = "optdeps" ]; then
    opt_install
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
    if [ ! -f ./env/bin/activate ]; then
        echo "You need virtualenv in env directory"
        echo "Run virtualenv -p python3 env"
        exit 1
    fi
    source env/bin/activate
    ./tg/bin/telegram-cli -k ./tg/tg-server.pub -Z bot/bot.py -l 1 -E
fi
