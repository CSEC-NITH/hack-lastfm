from __future__ import print_function
from flask import Flask
from flask import request, render_template, send_file
import config
from utils import get_token,get_album_art, generate_collage
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/collage', methods= ['GET','POST'])
def collage():
    print("HI")
    if request.method=='GET':
        return render_template('collage.html',input=True)
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
        filenames = get_album_art(r.text, username)
        generate_collage(filenames,username)
        return send_file('static/' + username+'.jpg', mimetype='image/jpg')

if __name__ == "__main__":
    app.run()

