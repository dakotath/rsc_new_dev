from flask import Flask, render_template, request, redirect, Response
from flask_babel import Babel, gettext
from werkzeug.serving import WSGIRequestHandler
from werkzeug.urls import url_encode
from urllib.request import Request, urlopen

import time
import random
import json
import ssl
import hashlib
import sqlite3
import socket
import shopCardPoints

conn = sqlite3.connect('riishop.db', check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)
babel = Babel(app)

@app.route('/')
def mainLoader():
    return render_template("mainPage.html")#'Hello, World!'

@app.route('/welcome')
def welcome():
    return render_template("welcome.html", userInfos=shopCardPoints.getUserInfos(conn, cursor))

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    # Hint that we are about to use very brittle ciphers.
    context.set_ciphers('ALL:@SECLEVEL=0')
    context.load_cert_chain('ssl/cert.pem', 'ssl/key.pem')

    app.run(host="192.168.2.51", port=443, debug=True, ssl_context=context) #, socket.gethostbyname(socket.gethostname()))
