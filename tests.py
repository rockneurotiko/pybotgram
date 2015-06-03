import importlib
import shutil
import os
# Copy the mock and import it
if os.path.isfile('tgl.pyc'):
    shutil.os.remove('tgl.pyc')
shutil.copy('mock/tgl.py', '.')
import tgl
from gl import settings
from gl import utils


def print_error(msg, plugin):
    print('\033[31mError in plugin \033[93m"{}"\033[39m'.format(plugin))
    print('\033[31mMessage: {}\033[39m'.format(msg))


def check_plugins():
    # Check the plugins
    res = 0
    for p in utils.clean_plugins(utils.get_all_plugins()):
        try:
            m = importlib.import_module('plugins.{}'.format(p))
            if not hasattr(m, '__info__'):
                print_error("Don't have __info__", p)
                res = 1
            if type(m.__info__) is not dict:
                print_error("__info__ is not a dictionary.", p)
                res = 1
            info = m.__info__
            haverun = hasattr(info.get("run"), '__call__')
            havecron = hasattr(info.get("cron"), '__call__')
            haveprec = hasattr(info.get("pre_process"), '__call__')
            if not (haverun or havecron or haveprec):
                print_error("Every plugin need a run, cron or pre_process function, and this does't have any of that.", p)
                res = 1
        except Exception as e:
            print('\033[31mError loading plugin {}\033[39m'.format(p))
            print('\033[31m{}\033[39m'.format(e))
            res = 1
    return res

res = check_plugins()
if os.path.isfile('tgl.pyc'):
    shutil.os.remove('tgl.pyc')
shutil.os.remove('./tgl.py')

exit(res)
