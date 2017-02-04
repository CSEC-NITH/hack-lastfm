from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import request
import config
from utils import get_token
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
        print(username)
        payload = {'user': username, 'api_key': config.LASTFM_API_KEY, 'method': 'user.gettopalbums'}
        r = requests.get(config.url, params = payload)
        print(r.text)
        return "DONE"

if __name__ == "__main__":
    app.run()

