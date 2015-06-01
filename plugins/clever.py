import cleverbot


def run(msg, matches):
    text = matches[0].strip().lstrip('!')
    # cb = cleverbot.Session()
    cb = cleverbot.Cleverbot()
    response = cb.ask(text)  # Ask
    return response


__info__ = {
    "description": "cleverbot",
    "usage": ["!clever (text)"],
    "patterns": [
        "^!clever +(.+)$",
    ],
    "run": run
}
