import config
import requests
import json
import hashlib

def md5sum(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def signature(method):
    sig = 'api_key' + config.LASTFM_API_KEY + 'method'+method + 'token' + config.LASTFM_TOKEN + LASTFM_SECRET
    return md5sum(sig)

def get_token():
    payload={'method':'auth.getToken','api_key':config.LASTFM_API_KEY, 'format':'json'}
    r=requests.get(config.url,params=payload)
    if r.status_code==200:
        x=json.loads(r.text)
        return x['token']

