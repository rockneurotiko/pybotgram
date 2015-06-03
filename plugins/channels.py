from gl import utils


def enable_channel(receiver):
    conf = utils.get_safe_setting('disabled_channels', list)
    if receiver not in conf:
        return "Channel is not disabled!"
    utils.generic_cfg(receiver, 'remove', list, 'disabled_channels')
    utils.reload_cfg_plugins('disabled_channels')
    return "Channel enabled"


def disable_channel(receiver):
    conf = utils.get_safe_setting('disabled_channels', list)
    if receiver in conf:
        return "Channel already disabled!"
    utils.generic_cfg(receiver, 'append', list, 'disabled_channels')
    utils.reload_cfg_plugins('disabled_channels')
    return "Channel disabled"


def run(msg, matches):
    receiver = utils.get_receiver_id(msg)
    if matches[0] == "enable":
        return enable_channel(receiver)
    if matches[0] == "disable":
        return disable_channel(receiver)


def pre_process(msg):
    receiver = utils.get_receiver_id(msg)
    if utils.is_sudo(msg) and msg.text == "!channel enable":
        peer = utils.get_receiver(msg)
        enable_channel(receiver)
        peer.send_msg("Channel enabled")
        return None  # Already processed
    conf = utils.get_safe_setting('disabled_channels', list)
    if receiver in conf:
        return None  # Don't process the message
    return msg


__info__ = {
    "description": ["Plugin to manage channels.",
                    "Enable or disable channel."],
    "usage": ["!channel enable: enable current channel",
              "!channel disable: disable current channel"],
    "patterns": ["^!channel? (enable|disable)$"],
    "run": run,
    "privileged": True,
    "pre_process": pre_process
}
