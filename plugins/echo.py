def run(msg, matches):
    text = matches[0].strip().lstrip('!')
    return text


__info__ = {
    "description": "Simplest plugin and example :)",
    "usage": ["!echo (text)"],
    "patterns": [
        "^!echo +(.+)$",
    ],
    "run": run
}
