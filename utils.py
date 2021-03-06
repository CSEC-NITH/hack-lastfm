import config
import requests
import json
import hashlib
from PIL import Image
import shutil
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

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

def get_album_data(response):
    artist_names=[]
    album_names=[]
    playcounts=[]
    data=json.loads(response)
    print(json.dumps(data,indent=4))
    albums=data['topalbums']['album']
    for album in albums:
        artist_names.append(album['artist']['name'])
        album_names.append(album['name'])
        playcounts.append(int(album["playcount"]))
    artist_names.reverse()
    album_names.reverse()
    playcounts.reverse()
    return artist_names,album_names,playcounts    

def gen_graph(title,labels,frequency,filename,colour):
    x_pos=np.arange(len(labels))
    plt.figure(figsize=(25,10))
    plt.barh(x_pos, frequency, align='center', alpha=0.5, height=0.5, color=colour)
    plt.yticks(x_pos, labels)
    plt.xlabel('Playcounts')
    plt.title(title)
    plt.savefig('static/' + filename)


def comparison_graph(N,freq1,freq2,new_list,user1,user2):
    ind = np.arange(N)  # the x locations for the groups
    width = 0.25       # the width of the bars

    fig, ax = plt.subplots(figsize=(25, 10))
    rects1 = ax.barh(ind, freq1, width, color='#9DB9AE')
    rects2 = ax.barh(ind + width, freq2, width, color='#645D56')
    t = ()
    for i in new_list:
        t = t+(i,)
    # add some text for labels, title and axes ticks
    ax.set_xlabel('Play Count')
    ax.set_title('Top common artists')
    ax.set_yticks(ind + width / 2)
    ax.set_yticklabels(t)

    ax.legend((rects1[0], rects2[0]), (user1, user2))

    plt.savefig('static/'+ user1+user2+'.jpg')
    
def get_artists_data(response): 
    artist_names=[]
    playcounts=[]
    data=json.loads(response)
    print(json.dumps(data,indent=4))
    artists=data['topartists']['artist']
    for artist in artists:
        artist_names.append(artist['name'])
        playcounts.append(int(artist["playcount"]))
    artist_names.reverse()
    playcounts.reverse()
    return artist_names,playcounts      


def get_tracks_data(response): 
    track_names=[]
    playcounts=[]
    data=json.loads(response)
    print(json.dumps(data,indent=4))
    tracks=data['toptracks']['track']
    for track in tracks:
        track_names.append(track['name'])
        playcounts.append(int(track["playcount"]))
    track_names.reverse()
    playcounts.reverse()
    return track_names,playcounts      

def gen_artistlinks(response):
    links=[]
    data = json.loads(response)
    print(json.dumps(data,indent = 4))
    artists = data['artists']['artist']
    for i in artists:
        links.append(i['image'][3]['#text'])
    print(links)
    return links
