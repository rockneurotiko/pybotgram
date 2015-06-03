import requests


def run(msg, matches):
    returnText = "Oops, an error occurred."
    exp = matches[0]
    payload = {'expr': exp}
    r = requests.get("http://api.mathjs.org/v1/", params = payload)
    
    if r.text:
	    returnText = r.text
	
    return returnText

__info__ = {
    "description": "A calculator to evaluate expressions",
    "usage": ["!calc (expression)"],
    "patterns": ["^!calc ([\s\S]+)$"],
    "run": run
}
