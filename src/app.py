from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import request
import config
from utils import get_token,get_album_art
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/collage', methods= ['GET','POST'])
def collage():
    print("HI")
    if request.method=='GET':
        return render_template('collage.html')
    elif request.method == 'POST':
        print("HELLO")
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
        get_album_art(r.text)
        return render_template('collage.html')

if __name__ == "__main__":
    app.run()

