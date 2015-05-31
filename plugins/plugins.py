from gl import settings
from gl import utils


def generic_cfg(data, action, defaultt=list, field='enabled_plugins', fname="data/config.p", key=None):
    cfg = utils.load_cfg(fname)  # load cfg
    plugs = cfg.get(field) or defaultt()
    if key is not None:
        if not plugs.get(key):
            plugs[key] = type(data)()
        if not hasattr(plugs[key], action):
            return
        getattr(plugs[key], action)(data)
    else:
        if not hasattr(plugs, action):
            return
        getattr(plugs, action)(data)
    cfg[field] = plugs
    utils.dump_cfg(fname, cfg)


def getOrElse(field, defaultt=list, fname='data/config.p'):
    cfg = utils.load_cfg(fname)  # load cfg
    return (cfg, cfg.get(field) or defaultt())


def list_plugins(only_enabled=False, receiver='', in_chat=False):
    text = ""
    allp = settings.ALL_PLUGINS if hasattr(settings, 'ALL_PLUGINS') else utils.clean_plugins(utils.get_all_plugins())
    for plug in allp:
        status = utils.emojis.get('nope')
        if plug in settings.ENABLED_PLUGINS:
            status = utils.emojis.get('ok')
        if utils.is_plugin_disabled_on_chat(plug, receiver):
            status = '{} (in chat)'.format(utils.emojis.get('nope'))
        if not only_enabled or status == utils.emojis.get('ok'):
            text += "{} {}\n".format(plug, status)
        elif in_chat:
            text += "{} {}\n".format(plug, status)
    return text


def enable_plugin(name, receiver):
    print("")
    if utils.plugin_enabled(name):
        return 'Plugin {} is enabled'.format(name)
    if utils.plugin_exists(name):
        generic_cfg(name, 'append')
        print("Added plugin {} to config file".format(name))
        utils.reload_cfg_plugins()
        return list_plugins(True, receiver)
    else:
        return 'Plugin "{}" does not exists'.format(name)


def disable_plugin(name, receiver):
    if not utils.plugin_exists(name):
        return 'Plugin {} does not exists'.format(name)
    if not utils.plugin_enabled(name):
        return 'Plugin {} is not enabled'.format(name)
    generic_cfg(name, 'remove')
    print("Removed plugin {} to config file".format(name))
    utils.reload_cfg_plugins()
    return list_plugins(True, receiver)


def enable_plugin_chat(name, receiver):
    if not utils.plugin_exists(name):
        return 'Plugin {} does not exists'.format(name)
    if not utils.is_plugin_disabled_on_chat(name, receiver):
        return 'Plugin {} is not disabled in this chat'.format(name)
    cfg, data = getOrElse('disabled_plugins_on_chat', dict)
    plgs = data.get(receiver)
    plgs.remove(name)
    data[receiver] = plgs
    generic_cfg(data, 'update', dict, field='disabled_plugins_on_chat')
    print("Enabled plugin {} in chat {} and saved".format(name, receiver))
    cfg['disabled_plugins_on_chat'] = data
    utils.save_cfg_settings(cfg)
    return "Plugin {} enabled in the chat again! {}".format(name, utils.emojis['smile'])
    # return list_plugins(True, receiver, True)


def disable_plugin_chat(name, receiver):
    if not utils.plugin_exists(name):
        return 'Plugin {} does not exists'.format(name)
    cfg, data = getOrElse('disabled_plugins_on_chat', dict)
    plgs = data.get(receiver) or set()
    plgs.add(name)
    data[receiver] = plgs
    generic_cfg(data, 'update', dict, field='disabled_plugins_on_chat')
    print("Disabled plugin {} in chat {} and saved".format(name, receiver))
    cfg['disabled_plugins_on_chat'] = data
    utils.save_cfg_settings(cfg)
    return "Plugin {} disabled in the chat {}".format(name, utils.emojis['wut'])
    # return list_plugins(True, receiver, True)


def run(msg, matches):
    receiver = utils.get_receiver_id(msg)
    print(matches)
    if len(matches) == 1:
        if matches[0] == "!plugins":
            return list_plugins(receiver=receiver)
        elif matches[0] == "reload":
            utils.load_enabled_plugins()
            return list_plugins(True)
    elif len(matches) == 2:
        if matches[0] == 'enable':
            return enable_plugin(matches[1], receiver)
        else:
            print("Disable {} on this chat".format(matches[1]))
            return disable_plugin(matches[1], receiver)
    elif len(matches) == 3:
        if matches[0] == 'enable':
            return enable_plugin_chat(matches[1], receiver)
        else:
            return disable_plugin_chat(matches[1], receiver)


__info__ = {
    "description": "Plugin to manage other plugins. Enable, disable or reload.",
    "usage": ["!plugins: list all plugins.",
              "!plugins enable [plugin]: enable plugin.",
              "!plugins disable [plugin]: disable plugin.",
              "!plugins disable [plugin] chat: disable plugin only this chat.",
              "!plugins reload: reloads all plugins."],
    "patterns": [
        "^!plugins$",
        "^!plugins? (enable|disable) ([\w_\.\-]+)$",
        "^!plugins? (enable|disable) ([\w_\.\-]+) (chat)?$",
        "^!plugins (reload)$",
    ],
    "run": run,
    'privileged': True
    # "cron": lambda: print(),
    # "pre_process": lambda x: print(x)
}
