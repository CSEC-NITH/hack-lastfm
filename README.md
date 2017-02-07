# hack-lastfm

hack-lastfm is a flask website that generates statistics and collages for last.fm users. We use
requests to send API requests to last.fm and generate collages of top albums, graphs for top artists
albums and tracks and compare two different users.

## Authors

* Param Singh
* Rashi Sah
* Prakriti Gupta
* Kuldip Kumar
* Udit Gulati

# How to build

    git clone https://github.com/paramsingh/hack-lastfm

    sudo pip install virtualenv

    cd hack-lastfm

    virtualenv env

    pip install -r requirements.txt

    python app.py

Contributions are welcome! We plan to use d3.js to make better visualizations in the future.
