def ppath(success, path):
    # Move to a user location?
    if success:
        print("File downloaded to: {}".format(path))


def run(msg, matches):
    if hasattr(msg, "load_{}".format(matches[0])):
        f = getattr(msg, "load_{}".format(matches[0]))
        f(ppath)


__info__ = {
    "description": "Plugin to download all media files to a directory.",
    "usage": ["This plugin is automatic when someone send a file."],
    "patterns": [
        "^\[(document)\]",
        "^\[(photo)\]",
        "^\[(video)\]",
        "^\[(image)\]"],
    "run": run
}
