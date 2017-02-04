import config
import requests
import json
import hashlib
from PIL import Image
import shutil

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

def generate_collage(images,username):
    image = map(Image.open,images)
    new_im = Image.new('RGB', (900, 900))
    x_offset = 0
    y_offset = 0
    for i in image:
        new_im.paste(i, (x_offset,y_offset))
        x_offset+=300
        if x_offset == 900:
            x_offset = 0
            y_offset+=300
    new_im.save('static/'+username+ '.jpg')
    

def get_album_art(response, username):
    links=[]
    data = json.loads(response)
    print(json.dumps(data,indent = 4))
    albums = data['topalbums']['album']
    for i in albums:
        q= (i['image'][-1]['#text']) 
        links.append(q)
    return download_images(links, username)

def download_images(links, username):
    cnt = 0
    filenames = []
    for i in links:
        r = requests.get(i,stream = True)
        fn = username + str(cnt) + '.png'
        with open(fn ,'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        filenames.append(fn)
        cnt += 1
    return filenames  






