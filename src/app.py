from __future__ import print_function
from flask import Flask
from flask import request, render_template, send_file
import config
from utils import get_token,get_album_art, generate_collage, gen_graph, get_album_data, get_artists_data, get_tracks_data ,\
    gen_artistlinks, download_images
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

if __name__ == "__main__":
    app.run()

