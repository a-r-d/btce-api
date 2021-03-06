import httplib
import json
import decimal

decimal.getcontext().rounding = decimal.ROUND_DOWN
exps = [decimal.Decimal("1e-%d" % i) for i in range(16)]

btce_domain = "btc-e.com"

all_currencies = ("btc", "usd", "rur", "ltc", "nmc", "eur", "nvc", 
                  "trc", "ppc")  
all_pairs = ("btc_usd", "btc_rur", "btc_eur", "ltc_btc", "ltc_usd", 
             "ltc_rur", "nmc_btc", "usd_rur", "eur_usd", "nvc_btc", 
             "trc_btc", "ppc_btc")
max_digits = {"btc_usd":3,
              "btc_rur":4,
              "btc_eur":5,
              "ltc_btc":5, 
              "ltc_usd":6,
              "ltc_rur":5,
              "nmc_btc":5,
              "usd_rur":5,
              "eur_usd":5, 
              "nvc_btc":5,
              "trc_btc":5,
              "ppc_btc":5}
min_orders = {"btc_usd":0.1,
              "btc_rur":0.1,
              "btc_eur":0.1,
              "ltc_btc":0.1, 
              "ltc_usd":0.1,
              "ltc_rur":0.1,
              "nmc_btc":0.1,
              "usd_rur":0.1,
              "eur_usd":0.1, 
              "nvc_btc":0.1,
              "trc_btc":0.1,
              "ppc_btc":0.1}

def makeRequest(url, extra_headers = None, params = {}):
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    if extra_headers is not None:
        headers.update(extra_headers)
        
    conn = httplib.HTTPSConnection(btce_domain)
    conn.request("POST", url, params, headers)
    response = conn.getresponse().read()
    conn.close()    

    return response
              
def makeJSONRequest(url, extra_headers = None, params = {}):
    response = makeRequest(url, extra_headers, params)
    
    # Fix up bogus values returned by the API; sometimes floating-point
    # numbers with no fractional value are returned as 1. instead of 1.0, etc.
    response = response.replace(".,", ".0,")
    
    try:
        r = json.loads(response)
    except Exception as e:
        print "Error while attempting to parse JSON response: %s" % e
        print "Response: %r" % response
        raise e
    
    return r

def validatePair(pair):
    if pair not in all_pairs:
        if "_" in pair:
            a, b = pair.split("_")
            swapped_pair = "%s_%s" % (b, a)
            if swapped_pair in all_pairs:
                msg = "Unrecognized pair: %r -- did you mean %s?" % (pair, swapped_pair)
                raise Exception(msg)
        raise Exception("Unrecognized pair: %r" % pair)
        
def formatCurrency(value, maxdigits):
    s = str(decimal.Decimal(value).quantize(exps[maxdigits]))
    while s[-1] == "0":
        s = s[:-1]
        
    return s

