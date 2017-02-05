from __future__ import print_function
from flask import Flask
import json
from flask import request, render_template, send_file
import config
from utils import get_token,get_album_art, generate_collage, gen_graph, get_album_data, get_artists_data, get_tracks_data ,\
    gen_artistlinks, download_images, comparison_graph
import requests
import json


app = Flask(__name__)

@app.route('/')
def index():
    payload={
            'api_key' : config.LASTFM_API_KEY,
            'method' : 'chart.getTopArtists',
            'limit' : 9,
            'format' : 'json'
    }
    r=requests.get(config.url, params=payload)
    links = gen_artistlinks(r.text)
    filenames = download_images(links, 'index')
    generate_collage(filenames, 'index_image')
    return render_template('index.html')

@app.route('/collage', methods= ['GET','POST'])
def collage():
    if request.method=='GET':
        return render_template('collage.html',input=True)
    elif request.method == 'POST':
        username = request.form['lastfm_username']
        duration = request.form['duration']
        print(username)
        payload = {
            'user': username,
            'api_key': config.LASTFM_API_KEY,
            'method': 'user.gettopalbums',
            'period':duration,
            'limit':9,
            'format':'json'
        }
        r = requests.get(config.url, params = payload)
        filenames = get_album_art(r.text, username)
        generate_collage(filenames,username)
        return send_file('static/' + username+'.jpg', mimetype='image/jpg')


@app.route('/stats', methods=['GET','POST'])
def stats():
    if request.method=='GET':
        return render_template('stats.html',input=True)
    elif request.method == 'POST':
        username = request.form['lastfm_username']
        duration = request.form['duration']
        print(username)
        payload = {
            'user': username,
            'api_key': config.LASTFM_API_KEY,
            'method': 'user.gettopalbums',
            'period':duration,
            'limit':10,
            'format':'json'
        }
        r = requests.get(config.url, params = payload)
        artists_names,album_names,playcounts=get_album_data(r.text)
        gen_graph("Top Albums",album_names,playcounts,username + "_albums.png","RED")
        payload['method']='user.gettopartists'
        r = requests.get(config.url, params = payload)
        artists_names,playcounts=get_artists_data(r.text)
        gen_graph("Top Artists",artists_names,playcounts,username + "_artists.png", "BLUE")
        payload['method']='user.gettoptracks'
        r = requests.get(config.url, params = payload)
        track_names,playcounts=get_tracks_data(r.text)
        gen_graph("Top Tracks",track_names,playcounts,username + "_tracks.png","YELLOW")

        return render_template('stats.html',input=False,username=username)

@app.route('/comparison',methods= ['GET','POST'])
def comparison():
    if request.method=='GET':
        return render_template('compar.html',input=True)
    elif request.method=='POST':
        user1 = request.form['lastfm_username1']
        user2 = request.form['lastfm_username2']
        payload1 = {
            'user': user1,
            'api_key': config.LASTFM_API_KEY,
            'method': 'User.getTopArtists',
            'limit':100,
            'format':'json'
        }
        payload2 = {
            'user': user2,
            'api_key': config.LASTFM_API_KEY,
            'method': 'User.getTopArtists',
            'limit':100,
            'format':'json'
        }
        r1 = requests.get(config.url, params = payload1)
        r2 = requests.get(config.url, params = payload2)
        if r1.status_code ==200 and r2.status_code==200:
            list1=[]
            list2=[]
            x1=json.loads(r1.text)
            print(json.dumps(x1,indent=4))
            x2=json.loads(r2.text)
            print(json.dumps(x2,indent=4))
            size1 = len(x1['topartists']['artist'])
            size2 = len(x2['topartists']['artist'])
            frequency1={}
            frequency2 = {}
            for i in range(size1):
                list1.append(x1['topartists']['artist'][i]['name'])
                frequency1[list1[i]]=x1['topartists']['artist'][i]['playcount']
            for j in range(size2):   
                list2.append(x2['topartists']['artist'][j]['name'])
                frequency2[list2[j]]=x2['topartists']['artist'][j]['playcount']
            new_list = []
            count=0
            for i in list1:
                if i in list2:
                    new_list.append(i)
                    count+=1
                    if count==10:
                        break
            freq1 = ()
            freq2 = ()
            for i in new_list:
                freq1= freq1+(frequency1[i],)
            for j in new_list:
                freq2 = freq2+(frequency2[j],)
            if not new_list:
                return render_template('compar.html', input = False, zero = True)
            comparison_graph(len(new_list),freq1,freq2,new_list,user1,user2)
            return render_template('compar.html', input = False, graph = user1+user2+'.jpg')

if __name__ == "__main__":
    app.run()