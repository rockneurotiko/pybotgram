import tgl
import pprint
from functools import partial
import sys
import os
import datetime
BOTPATH = os.path.realpath(os.path.abspath('.'))
sys.path.append(BOTPATH)
from gl import settings
from gl import utils


our_id = 0
now = datetime.datetime.now()
pp = pprint.PrettyPrinter(indent=4)
default_delay = 5 * 60

started = False

__version__ = '0.0.1'

print("Python version: {}".format(sys.version))


def on_msg_receive(msg):
    global started
    if not started:
        return
    talkoneself = settings.TALK_ONESELF if hasattr(settings, 'TALK_ONESELF') else False
    receiver = utils.get_receiver(msg)
    # pp.pprint(msg)
    # pp.pprint(receiver)
    if msg_valid(msg):
        msg = _internal_preproc(msg)
        msg = pre_process_msg(msg)
        if msg:
            match_plugins(msg)
            if not talkoneself:  # Only mark as read if we don't let us talk to ourself (means that we are the bot)
                receiver.mark_read(utils.ok_gen)


def _internal_preproc(msg):
    if not msg.text and msg.media:
        msg = utils.props(msg)
        msg.text = "[{}]".format(msg.media.get('type'))
    return msg


def pre_process_msg(msg):
    for name in settings.PLUGINS:
        if utils.plugin_have(name, 'pre_process'):
            msg = utils.execute_plugin_function(name, 'pre_process', msg)
            if not msg:
                return None  # stop process :)
    return msg


def match_plugins(msg):
    for name, plugin in settings.PLUGINS.items():
        match_plugin(plugin, name, msg)


def match_plugin(plugin, name, msg):
    if not hasattr(msg, 'text') or not msg.text or msg.text == '':
        return
    receiver = utils.get_receiver(msg)
    text = msg.text
    patterns = utils.get_infov(plugin, 'patterns', ())
    for pattern in patterns:
        # print("Trying to match", pattern, "with", text)
        matches = utils.match_pattern(pattern, text)
        if not matches:
            continue
        print("Message matches: {}".format(pattern))

        if utils.is_plugin_disabled_on_chat(name, receiver):
            return None

        if not utils.plugin_have_obj(plugin, 'run'):
            print("The plugin {} don't have run function".format(name))
            continue
        if utils.warns_user_not_allowed(plugin, msg):
            continue
        result = utils.execute_plugin_function_obj(plugin, 'run', msg, matches)
        if result and type(result) == str:
            utils.send_large_msg(receiver, result)
        return  # Only one pattern per plugin!


def msg_valid(msg):
    talkoneself = settings.TALK_ONESELF if hasattr(settings, 'TALK_ONESELF') else False
    if not talkoneself and msg.out:
        print('\033[36mNot valid: msg from us\033[39m')
        return False

    if msg.date < now:
        print('\033[36mNot valid: old msg\033[39m')
        return False

    if not talkoneself and not msg.unread:
        print('\033[36mNot valid: readed\033[39m')
        return False

    if msg.service:
        print('\033[36mNot valid: service\033[39m')
        return False

    if not msg.dest.id:
        print('\033[36mNot valid: To id not provided\033[39m')
        return False

    if not msg.src.id:
        print('\033[36mNot valid: From id not provided\033[39m')
        return False

    if not talkoneself and msg.src.id == settings.OUR_ID:
        print('\033[36mNot valid: Msg from our id\033[39m')
        return False

    if msg.dest.type == 'encr_chat':
        print('\033[36mNot valid: Encrypted chat\033[39m')
        return False

    if msg.src.id == 777000:
        print('\033[36mNot valid: Telegram message\033[39m')
        return False

    return True


def load_config():
    if not os.path.isfile('data/config.json'):
        create_initial_cfg()
    return utils.load_cfg('data/config.json')


def create_initial_cfg():
    print("Creating new config file: data/config.json")
    global our_id
    oid = settings.OUR_ID if hasattr(settings, 'OUR_ID') else our_id
    cfg = {
        'enabled_plugins': ['plugins',
                            'help',
                            'media'],
        'sudo_users': [oid],
        'disabled_channels': [],
        'talk_oneself': False,
    }
    if not os.path.isdir('data'):
        os.mkdir('data')
    utils.dump_cfg('data/config.json', cfg)
    print("Data created :)")


def on_binlog_replay_end():
    global started
    started = True
    config = load_config()
    utils.save_cfg_settings(config)
    handle_sudoers(config)
    utils.load_enabled_plugins()
    cron_plugins()


def handle_sudoers(cfg):
    suds = cfg.get('sudo_users') or (0,)
    for s in suds:
        print("Allowed sudo user: {}".format(s))


def on_get_difference_end():
    pass


def on_our_id(id):
    global our_id
    our_id = id
    settings.OUR_ID = id
    return "Set ID: " + str(our_id)


def msg_cb(success, msg):
    pass
    # pp.pprint(success)
    # pp.pprint(msg)

HISTORY_QUERY_SIZE = 100


def history_cb(msg_list, peer, success, msgs):
    print(len(msgs))
    msg_list.extend(msgs)
    print(len(msg_list))
    if len(msgs) == HISTORY_QUERY_SIZE:
        tgl.get_history(
            peer, len(msg_list), HISTORY_QUERY_SIZE, partial(history_cb, msg_list, peer))
    else:
        text = '\n'.join([str(i + 1) + ") " + x.text for (i, x) in enumerate(msgs[::-1]) if x.text is not None and not x.out])
        peer.send_msg(text, msg_cb)


def cb(success):
    pass
    # print(success)


def on_secret_chat_update(peer, types):
    return "on_secret_chat_update"


def on_user_update(user, what):
    # pp.pprint(user)
    # pp.pprint(what)
    pass


def on_chat_update(chat, what):
    # pp.pprint(chat)
    # pp.pprint(what)
    pass


@utils.delayed(default_delay)
def cron_plugins():
    print('yay!')


def noop():
    pass


# Set callbacks
tgl.set_on_binlog_replay_end(on_binlog_replay_end)
tgl.set_on_get_difference_end(on_get_difference_end)
tgl.set_on_our_id(on_our_id)
tgl.set_on_msg_receive(on_msg_receive)
tgl.set_on_secret_chat_update(on_secret_chat_update)
tgl.set_on_user_update(on_user_update)
tgl.set_on_chat_update(on_chat_update)
tgl.set_on_loop(noop)  # Make work the delayed functions :)

# utils.import_plugins(utils.get_all_plugins(['test']))
# utils.execute_plugin_function('test', 'run', '', [])
# utils.execute_plugin_function('test', 'run', '', [])
# utils.execute_plugin_function('test', 'run', '', [])
# utils.execute_plugin_function('test', 'run', '', [])
# utils.execute_plugin_function('test', 'run', '', [])
