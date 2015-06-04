from gl import utils
import re


def cb(r, receiver, amount, fromCur, toCur):
    returnText = 'An error occurred.'
    html = r.text or ''
    moneyMatches = re.search("<span class=bld>([\d.]+)", html)
    if moneyMatches:
        returnText = "{} {} is {} {}".format(
            amount, fromCur, moneyMatches.group(1), toCur)
    receiver.send_msg(returnText)


def run(msg, matches):
    currencies = ["AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTC", "BTN", "BWP", "BYR", "BZD", "CAD", "CDF", "CHF", "CLF", "CLP", "CNH", "CNY", "COP", "CRC", "CUP", "CVE", "CZK", "DEM", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FIM", "FJD", "FKP", "FRF", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "IEP", "ILS", "INR", "IQD", "IRR", "ISK", "ITL", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LTL", "LVL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKG", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SOS", "SRD", "STD", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VEF", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR", "ZMK", "ZMW", "ZWL"]

    fromCur = matches[0].upper()
    amount = matches[1]
    toCur = matches[2].upper()

    if fromCur.isdigit():
        fromCur, amount = amount.upper(), fromCur

    if fromCur not in currencies:
        return "ERROR: currency \"" + fromCur + "\" is not recognized"

    if toCur not in currencies:
        return "ERROR: currency \"" + toCur + "\" is not recognized"

    url = "https://www.google.com/finance/converter?a=" + \
          amount + "&from=" + fromCur + "&to=" + toCur

    receiver = utils.get_receiver(msg)

    gcb = utils.gac(cb, receiver, amount, fromCur, toCur)
    utils.mp_requests('GET', url, gcb)

__info__ = {
    "description": "Currency converter",
    "usage": ["!money (from currency) (amount) (to currency)"],
    "patterns": [
        "^!m(?:oney)? ([\d\.]+) (\w+)(?: in)? (\w+)$",
        "^!m(?:oney)? (\w+) ([\d\.]+)(?: in)? (\w+)$"],
    "run": run
}
