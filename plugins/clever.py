import cleverbot


def run(msg, matches):
    text = matches[0].strip().lstrip('!')
    # cb = cleverbot.Session()
    cb = cleverbot.Cleverbot()
    response = cb.ask(text)  # Ask
    return response


__info__ = {
    "description": "Cleverbot plugin.",
    "usage": ["!clever (text): Say the text to cleverbot and receive the answer"],
    "patterns": [
        "^!clever +(.+)$",
    ],
    "run": run
}
