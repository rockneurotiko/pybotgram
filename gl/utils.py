# -*- coding: utf-8 -*-

from threading import Timer
import re
import importlib
import collections
import os
try:
    import tgl
except Exception as e:
    print(e)
    print("You are not injected in telegram. Maybe some actions won't work :S")
from gl import settings
import pickle
import six
import json
import math

USER = 1
CHAT = 2


emojis = {
    'smile': '😄' if six.PY3 else ':)',
    'wut': '😐' if six.PY3 else ':|',
    'nope': '❌' if six.PY3 else 'X',
    'ok': '✔' if six.PY3 else 'V'
}


def get_receiver(msg):
    if msg.dest.type == USER:
        return msg.src
    if msg.dest.type == CHAT:
        return msg.dest
    if msg.dest.type == "encr_chat":
        print("Private chat!")
        return None


def get_receiver_id(msg):
    rcv = get_receiver(msg)
    base = 'user#id' if rcv.type == 'user' else 'chat#id'
    return "{}{}".format(base, rcv.id)


def ok_cb(success, msg):
    pass


def ok_gen(*args):
    pass


def get_all_plugins(pluginsloaded=(), ignore=True):
    return [f for f in os.listdir('plugins')
            if os.path.isfile(os.path.join('plugins', f)) and
            not f.startswith(".") and
            f.endswith(".py") and
            (ignore or f[:-3] in pluginsloaded)]


def clean_plugins(plugins):
    return [x[:-3] for x in plugins if not x.startswith("__init__")]


def reload_cfg_plugins():
    cfg = load_cfg('data/config.json')
    nplugs = cfg.get('enabled_plugins') or ()
    oplugs = settings.ENABLED_PLUGINS
    diff1 = all(map(lambda x: x in oplugs, nplugs))
    diff2 = all(map(lambda x: x in nplugs, oplugs))
    if not diff1 or not diff2:
        save_cfg_settings(cfg)
        load_enabled_plugins()


def plugin_enabled(name):
    return name in settings.PLUGINS.keys()


def plugin_exists(name):
    if hasattr(settings, 'ALL_PLUGINS'):
        return name in settings.ALL_PLUGINS
    return name in clean_plugins(get_all_plugins())


def save_cfg_settings(cfg):
    if type(cfg) is not dict:
        return
    defaults = ('enabled_plugins', "sudo_users", "disabled_channels", "all_plugins")
    settings.ALL_PLUGINS = clean_plugins(get_all_plugins())
    settings.ENABLED_PLUGINS = cfg.get('enabled_plugins') or ()
    settings.SUDO_USERS = cfg.get('sudo_users') or ()
    settings.DISABLED_CHANNELS = cfg.get('disabled_channels') or ()
    for k, v in cfg.items():
        if k.lower() in defaults: continue
        setattr(settings, k.upper(), v)


def get_enabled_paths(pluginsloaded=()):
    if hasattr(settings, 'ALL_PLUGINS'):
        return filter(lambda x: x in pluginsloaded, settings.ALL_PLUGINS)
    return get_all_plugins(pluginsloaded, False)


def load_enabled_plugins():
    eplugins = settings.ENABLED_PLUGINS if hasattr(settings, 'ENABLED_PLUGINS') else set()
    epaths = get_enabled_paths(eplugins)
    import_plugins(epaths, eplugins)


def import_plugins(paths, eplugins=set()):
    # Some magic to dynamic import and reload ^^
    plugins = settings.PLUGINS or {}
    errored = {}
    for p in paths:
        try:
            p = p[:-3] if p.endswith('.py') else p
            print("Loading plugin: {}".format(p))
            if plugins.get(p):
                m = importlib.reload(plugins[p])
            else:
                m = importlib.import_module('plugins.{}'.format(p))
            plugins[p] = m
        except Exception as e:
            errored[p] = None
            print('\033[31mError loading plugin {}\033[39m'.format(p))
            print('\033[31m{}\033[39m'.format(e))
    settings.PLUGINS = plugins
    allplug = errored.copy()
    allplug.update(plugins)
    for p in filter(lambda x: x not in allplug, eplugins):
        print("\033[93mWarning: Plugin \"{}\" not loaded, maybe it's not in plugins directory anymore?\033[39m".format(p))
    # Old way, can't reload in that way :S
    # plgs = __import__('plugins', globals(), locals(), paths, 0)
    # plugins = {}
    # for x in paths:
    #     try:
    #         print("Loading plugin: {}".format(x[:-3]))
    #         plugins.update({x[:-3]: getattr(plgs, x[:-3])})
    #     except Exception as e:
    #         print('\033[31mError loading plugin {}\033[39m'.format(x[:-3]))
    #         print('\033[31m{}\033[39m'.format(e))
    # settings.PLUGINS = plugins
    # settings.PLUGINS = {x[:-3]: getattr(plgs, x[:-3]) for x in paths}


def dump_cfg(path, data):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4)
    except:
        pass


def load_cfg(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}


def dump_pick_cfg(path, data):
    try:
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    except:
        pass


def load_pick_cfg(path):
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except:
        return {}


def plugin_have_obj(plugin, function):
    if not hasattr(plugin, '__info__'):
        return False
    return function in plugin.__info__.keys()


def plugin_have(plugin, function):
    plg  = settings.PLUGINS.get(plugin)
    if not plg:
        return False
    return plugin_have_obj(plg, function)
    # if not hasattr(plg, '__info__'):
    #     return False
    # f = plg.__info__.get(function)
    # if not f:
    #     return False
    # return True


def execute_plugin_function_obj(plugin, function, *args, **kargs):
    if not plugin_have_obj(plugin, function):
        return
    return plugin.__info__[function](*args, **kargs)


def execute_plugin_function(plugin, function, *args, **kargs):
    if not plugin_have(plugin, function):
        print("The plugin {} is not loaded or don't have {}".format(plugin, function))
        return
    f = settings.PLUGINS[plugin].__info__[function]
    return f(*args, **kargs)


def get_infov(plugin, val, default=None):
    if not hasattr(plugin, '__info__'):
        return default
    return plugin.__info__.get(val) or default


def match_pattern(pattern, text, lower_case=False):
    if lower_case:
        text = text.lower()
    match = re.search(pattern, text)
    if match:
        return match.groups() if match.groups() != () else (match.group(),)
    return None


def is_plugin_disabled_on_chat(name, receiver):
    if not hasattr(settings, 'DISABLED_PLUGINS_ON_CHAT'): return False
    disabl = settings.DISABLED_PLUGINS_ON_CHAT.get(receiver) or set()
    return name in disabl


def warns_user_not_allowed(plugin, msg):
    if not user_allowed(plugin, msg):
        get_receiver(msg).send_msg("This plugin requires privileged user")
        return True
    return False


def user_allowed(plugin, msg):
    if get_infov(plugin, 'privileged') and not is_sudo(msg):
        return False
    return True


def is_sudo(msg):
    return isinstance(settings.SUDO_USERS, collections.Iterable) and msg.src.id in settings.SUDO_USERS


def send_large_msg(receiver, text):
    _send_large_msg_callback_aux(receiver, text)(True, receiver)


# If text is longer than 4096 chars, send multiple msg.
# https://core.telegram.org/method/messages.sendMessage
def _send_large_msg_callback_aux(receiver, text):
    def aux(success, dest):
        text_max = 4096
        tlen = len(text)
        nmsg = math.ceil(tlen / text_max)
        if nmsg <= 1:
            receiver.send_msg(text, ok_cb)
        else:
            ntext = text[:text_max]
            rest = text[text_max:]
            f = _send_large_msg_callback_aux(receiver, rest)
            tgl.send_msg(receiver, ntext, f, True)
    return aux


# If text is longer than 4096 chars, send multiple msg.
# https://core.telegram.org/method/messages.sendMessage
# def send_large_msg_callback(success, cb_extra, result=None):
#     def aux(success, dest):
#         pass
#     text_max = 4096
#     destination = cb_extra.get('destination')
#     text = cb_extra.get('text')
#     if not destination or not text:
#         return
#     tlen = len(text)
#     nmsg = math.ceil(tlen / text_max)
#     if nmsg <= 1:
#         destination.send_msg(text, ok_cb)
#     else:
#         ntext = text[:text_max]
#         rest = text[text_max:]
#         cb_extra = {
#             'destination': destination,
#             'text': rest
#         }
#         tgl.send_msg(destination, ntext, send_large_msg_callback, cb_extra)
#         # destination.send_msg(ntext, send_large_msg_callback, cb_extra)


def delayed(seconds):
    def decorator(f):
        def wrapper(*args, **kargs):
            t = Timer(seconds, f, args, kargs)
            t.start()
        return wrapper
    return decorator
