from gl import utils


def user_id(msg):
    text = "{} (user#id{})".format(msg.src.name, msg.src.id)
    if utils.is_chat_msg(msg):
        text = "{}\nYou are in group {} (chat#id{})".format(text, msg.dest.name, msg.dest.id)
    return text


def callback(succ, peer):
    text = "IDs for chat {} (chat#id{}) [for now only the id]\nThere are {} members\n--------".format(peer.name, peer.id, len(peer.user_list))
    for p in peer.user_list:
        text = "{}\n{}".format(text, p)
    peer.send_msg(text)


def run(msg, matches):
    receiver = utils.get_receiver(msg)
    print()
    if len(matches) == 1:
        if matches[0] == "!id":
            return user_id(msg)
        elif matches[0] == 'chat':
            if not utils.is_chat_msg(msg):
                return 'You are not in a chat'
            else:
                receiver.info(callback)
    elif len(matches) == 2:
        return "Not implemented yet the function necesary in tgl :'('"
    # Implement your run function here
    return ""

__info__ = {
    "description": [
        "This plugin will return your id or the ids of the people in a chat"],
    "usage": [
        "!id: Return your ID and the chat id if you are in one.",
        "!ids chat: Return the IDs of the current chat members.",
        "!ids chat (id): Return the IDs of the chat (id) members."],
    "patterns": [
        "^!id$",
        # "^!ids? (chat) (\d+)$",
        "^!ids? (chat)$"],
    "run": run,
    "privileged": False
}
