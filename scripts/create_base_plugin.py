#!/usr/bin/env python
import re
import os
import sys
BOTPATH = os.path.realpath(os.path.abspath('.'))
sys.path.append(BOTPATH)


capabilities = {'sett': 'from gl import settings',
                'utils': 'from gl import utils',
                'int': 'import requests',
                're': 'import re',
                'image': 'from PIL import Image',
                'clever': 'import cleverbot'}


def test_caps(caps):
    return caps == '' or all([x.lower().strip() in capabilities.keys() for x in caps.split(',')])


def check_plugin_valid(p):
    pnamer = "[\w_\.\-]+"
    match = re.match(pnamer, p)
    valid = match and match.group(0) == p
    valid = valid and p != ""
    return valid and p not in [f[:-3] for f in os.listdir('plugins')
                               if os.path.isfile(os.path.join('plugins', f)) and
                               not f.startswith('.') and
                               not f.startswith('__') and
                               f.endswith('.py')]


def ask_for_n(message, end=''):
    res = []
    goout = False
    print(message)
    while not goout:
        tmp = input()
        res.append(tmp)
        goout = tmp == end
    return res


def ask_until(message, errormessage, check):
    goout = False
    while not goout:
        tmp = input("{}: ".format(message))
        goout = True
        if not check(tmp):
            goout = False
            print(errormessage.format(tmp))
    print('')  # blank space ^^
    return tmp

full_file_base = """{imports}

{content}

{info}
"""


base_class = """
class _Plugin_{name}:

    def __init__(self):
        # Initialization
        pass

{func}


_Plugin_{name}_ins = _Plugin_{name}()
"""


class_base_func = """    def {name}(self, {params}):
        # Implement your {name} function here
        return {rtn}"""

base_func = """
def {name}({params}):
    # Implement your {name} function here
    return {rtn}"""

run_c_f = class_base_func.format(name="run", params="msg, matches", rtn="\"Some text to send\"")
cron_c_f = class_base_func.format(name="cron", params="", rtn="")
prep_c_f = class_base_func.format(name="pre_process", params="msg", rtn="msg")

run_f = base_func.format(name="run", params="msg, matches", rtn="\"\"")
cron_f = base_func.format(name="cron", params="", rtn="")
prep_f = base_func.format(name="pre_process", params="msg", rtn="msg")


base_info = """__info__ = {{
    "description": {description},
    "usage": {usage},
    "patterns": {patterns},
{extra}
}}"""

extra_base = '    "{}": {}'

priv_base = extra_base.format('privileged', '{}')
run_base = extra_base.format('run', '{}')
cron_base = extra_base.format('cron', '{}')
prep_base = extra_base.format('pre_process', '{}')


input("""Hi!
Welcome to the base plugin creator.
I'm gonna ask you some questions to build your plugin.
Hit enter when you want to start rock!
""")

sp8 = ' ' * 8

name = ask_until("What will be your plugin name?", "Sorry, plugin name \"{}\" is already taken or is not valid", check_plugin_valid)

description = ask_for_n("Write the description for your the plugin \"{}\":".format(name))[:-1]

longd = len(description) > 1
description = '"{}"'.format(description[0]) if not longd else '",\n{}"'.format(sp8).join(description)
if longd:
    description = "[\n{}\"{}\"]".format(sp8, description)


usages = ask_for_n('Put the usage list, one by one, and leave it blank when you want to finish:')[:-1]

usages = "[\n{}\"{}\"]".format(sp8, '",\n{}"'.format(sp8).join(usages))


patterns = ask_for_n('Put the patterns list, one by one, and leave it blank when you want to finish:')[:-1]

patterns = "[\n{}\"{}\"]".format(sp8, '",\n{}"'.format(sp8).join(patterns))


stateful = ask_until("Will the plugin \"{}\" be statefull or stateless? (full/less)".format(name), 'Write "full" or "less"', lambda x: x.lower() in ['full', 'less', 'f', 'l']).lower()
stateful = stateful[0] == 'f'

base_name_inf = "_Plugin_{}_ins.".format(name) if stateful else ''

priv = ask_until("Will the plugin \"{}\" be only for privileged users? (y/n)".format(name), 'Write "y" or "n"', lambda x: x.lower() in ['y', 'n', 'yes', 'no']).lower()
priv = priv[0] == 'y'
priv_e = priv_base.format("True" if priv else "False")

typ = ask_until('Of what type will be your plugin? (run/cron/preprocess)', 'Write "run", "cron" or "preprocess"', lambda x: x.lower() in ['run', 'cron', 'preprocess', 'r', 'c', 'p']).lower()

content = ''
if stateful:
    if typ[0] == 'r':
        func = run_c_f
    elif typ[0] == 'c':
        func = cron_c_f
    else:
        func = prep_c_f
    content = base_class.format(name=name, func=func)

if typ[0] == 'r':
    content = run_f if content == '' else content
    typ_e = run_base.format('{}run'.format(base_name_inf))
if typ[0] == 'c':
    content = cron_f if content == '' else content
    typ_e = cron_base.format('{}cron'.format(base_name_inf))
if typ[0] == 'p':
    content = prep_f if content == '' else content
    typ_e = prep_base.format('{}pre_process'.format(base_name_inf))


extra_f = "{},\n{}".format(typ_e, priv_e)

info_f = base_info.format(description=description, usage=usages, patterns=patterns, extra=extra_f)

caps = ask_until("""What capabilities will have the plugin? (cap1, cap2, ...)

The capabilities are:
[Name]: [capability]
-----------------
Settings: sett
Utils: utils
Internet: int
Regular expressions: re
Image: image
Cleverbot: clever

Write yours""", "Write a the capabilities separated by commas", test_caps)

imports = '' if caps == '' else '\n'.join(sorted([capabilities[x] for x in {y.lower().strip() for y in caps.split(',')}]))


final_path = './plugins/{}.py'.format(name)
end_file = full_file_base.format(imports=imports, content=content, info=info_f)

input("Hit enter to see how your file will look, then hit enter again to ask you if save it.\n")
print("------------------ Start Plugin {} ------------------".format(name))
print(end_file)
print("------------------ End Plugin {} ------------------".format(name))
input()

save = ask_until("Do you want to save the plugin file in {}? (yes/no)".format(final_path), 'Type "yes" or "no"', lambda x: x.lower() in ['y', 'n', 'yes', 'no']).lower()
if save[0] == 'y':
    with open(final_path, 'w') as f:
        f.write(end_file)
    print("File saved in {}".format(final_path))
else:
    print("Ok, I won't save it, see you!")
