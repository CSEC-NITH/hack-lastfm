from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html')

if __name__ == "__main__":
    app.run()
