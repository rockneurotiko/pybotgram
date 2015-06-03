from gl import settings
from gl import utils
import collections


def gen_help():
    text = "Plugin list:\n\n"
    for pname, p in settings.PLUGINS.items():
        info = p.__info__ if hasattr(p, '__info__') else {}
        text += "{}: {}\n".format(pname, info.get('description') or 'No description')
    text += "\nWrite \"!help [plugin name]\" for more info.\nOr \"!help all\" to show all info."
    return text


def help_plugin(name):
    if not utils.plugin_enabled(name):
        return "Plugin {} is not enabled, try execute \"!help\"".format(name)
    plg = settings.PLUGINS[name]
    if not hasattr(plg, '__info__'):
        return 'The plugin {} don\'t have information'.format(name)
    if not plg.__info__.get('usage'):
        return 'The plugin {} don\'t have usage info'.format(name)
    usage = plg.__info__['usage']
    if type(usage) is str:
        return usage
    elif isinstance(usage, collections.Iterable):
        return '\n'.join(usage)
    return ''


def help_all():
    return '\n\n'.join(map(help_plugin, settings.ENABLED_PLUGINS))


def run(msg, matches):
    if len(matches) != 1:
        return
    if matches[0] == "!help":
        return gen_help()
    if matches[0] == "all":
        return help_all()
    return help_plugin(matches[0])


__info__ = {
    "description": ["Help plugin.", "Get info from other plugins."],
    "usage": ["!help: Show list of plugins.",
              "!help all: Show all commands for every plugin.",
              "!help [plugin name]: Commands for that plugin."],
    "patterns": [
        "^!help$",
        "^!help ([\w_\.\-]+)$",
    ],
    "run": run
    # "cron": lambda: print(),
    # "pre_process": lambda x: print(x)
}
