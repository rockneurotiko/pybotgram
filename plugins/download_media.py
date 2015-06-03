def ppath(success, path):
    # Move to a user location?
    if success:
        print("File downloaded to: {}".format(path))


def run(msg, matches):
    if hasattr(msg, "load_{}".format(matches[0])):
        f = getattr(msg, "load_{}".format(matches[0]))
        f(ppath)


__info__ = {
    "description": "When bot receives a media msg, download the media to the file system.",
    "usage": ["This plugin is automatic when someone send a file."],
    "patterns": [
        "^\[(photo)\]$",
        "^\[(video)\]$",
        "^\[(video)_thumb\]$",
        "^\[(audio)\]$",
        "^\[(document)\]$",
        "^\[(document_thumb)\]$"],
    "run": run
}
