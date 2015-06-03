#!/usr/bin/env python
import sys
import os
import shutil
import re
sys.path.append(os.path.realpath(os.path.abspath('.')))
if os.path.isdir('tgl.pyc'):
    shutil.os.remove('tgl.pyc')
shutil.copy('mock/tgl.py', '.')


def safe_exit(code=0):
    if os.path.isfile('tgl.pyc'):
        shutil.os.remove('tgl.pyc')
    if os.path.isfile('tgl.py'):
        shutil.os.remove('./tgl.py')
    exit(code)


def get_values(p):
    if not hasattr(p, '__info__'):
        return ('', '')
    info = p.__info__
    desc = info.get('description')
    desc = desc or 'No description'
    usage = info.get('usage')
    usage = usage or ''
    if type(desc) is list:
        desc = '<br>'.join(desc)
    if type(usage) is list:
        usage = '<br>'.join(usage)
    return desc, usage


activate_this_file = "./env/bin/activate_this.py"
if not os.path.isfile(activate_this_file):
    print("You need to install the virtualenv")
    safe_exit(1)

if not hasattr(sys, 'real_prefix'):
    print("You are not inside the virtualenv.")
    print("Do 'source env/bin/activate' before executing this")
    safe_exit(1)

import tgl
from gl import utils
from gl import settings


plugins = utils.clean_plugins(utils.get_all_plugins())

text = "| Name | Description | Usage |\n| ---- | ----------- | ----- |\n"
base = "| {} | {} | {} |\n"
utils.import_plugins(plugins, plugins)
for p in sorted(plugins):
    realname = "{}.py".format(p)
    if not settings.PLUGINS.get(p):
        continue
    plug = settings.PLUGINS.get(p)
    desc, usage = get_values(plug)
    text += base.format(realname, desc, usage)


with open("README.md", "r") as f:
    readmetext = f.read()

reg1 = "Plugins\n---------\n+"
reg2 = "\n\nInstallation\n---------"
reg3 = "\|.*\|"

m1 = re.search(reg1, readmetext)
m2 = re.search(reg2, readmetext)

if not (m1 and m2):
    print("There have some problem reading README.md, here have your plugins information to copy and paste manually:")
    print(text)
    safe_exit(1)

oldtext = readmetext[m1.end():m2.start()]

textcmp1 = re.search(reg3, oldtext, re.DOTALL)
textcmp2 = re.search(reg3, text, re.DOTALL)

if (textcmp1 and textcmp2) and textcmp1.group(0) == textcmp2.group(0):
    print("You already have the last plugins in README.md! ^^")
    safe_exit()

print("I'm going to replace this text:\n------\n{}\n------\nFor this\n-----\n{}\n-----\n".format(oldtext, text))
resinput = input("If you want to make this changes, answer (Y): ")
if resinput == "Y":
    prevp = readmetext[:m1.end()]
    nextp = readmetext[m2.start():]
    nextreadme = "{}{}{}".format(prevp, text, nextp)
    with open("README.md", "w") as f:
        f.write(nextreadme)
    print("The text had been replaced!")
else:
    print("The text won't be replaced!")

safe_exit()
