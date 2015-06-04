from gl import utils


def cb(r, receiver):
    text = r.text if r.text else 'An error occurred.'
    receiver.send_msg(text)


def run(msg, matches):
    receiver = utils.get_receiver(msg)
    exp = matches[0]
    path = "http://api.mathjs.org/v1/"
    payload = {'expr': exp}
    if len(matches) > 1:
        payload.update({'precision': matches[1]})
    gcb = utils.gac(cb, receiver)
    utils.mp_requests('GET', path, gcb, params=payload)

__info__ = {
    "description": "A calculator to evaluate expressions",
    "usage": ["!calc (expression)"],
    "patterns": [
        "^!calc ([\s\S]+) prec (\d+)?$",
        "^!calc ([\s\S]+)$"],
    "run": run
}
