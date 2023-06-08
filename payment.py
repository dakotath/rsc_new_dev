from flask import Flask, render_template, request, redirect, Response
from flask_babel import Babel, gettext
from werkzeug.serving import WSGIRequestHandler
from werkzeug.urls import url_encode
from urllib.request import Request, urlopen

import time
import random
import json
import ssl
import sqlite3
import socket
import shopCardPoints

conn = sqlite3.connect('riishop.db', check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)
babel = Babel(app)

@app.route("/payment_interface/info/<string:serial>/<string:token>")
def paymentInterface(serial, token):
    shopCardPoints.getUserInfos(conn, cursor)
    paymentInfo = shopCardPoints.getUserInfo(conn, cursor, serial, token)

    return render_template('paymentInterface.html', serial=serial, token=token, userName=paymentInfo[0], points=paymentInfo[1], purchaseAmount=paymentInfo[2], purchaseAmountDivided=paymentInfo[2]/100, purchaseStatus=paymentInfo[3])

@app.route("/payment_interface/buy/<string:serial>/<string:amt>")
def paymentPoints(serial, amt):
    token = shopCardPoints.genPaymentToken(conn, cursor, serial, str(amt))

    return {"Serial": serial,"Token": token}

@app.route("/points/payment/ok/<string:serial>/<string:token>")
def paymentVerify2(serial, token):
    shopCardPoints.makePayment(conn, cursor, serial, token, "paid")
    paymentInfo = shopCardPoints.getUserInfo(conn, cursor, serial, token)

    return {"status":paymentInfo[3]}

@app.route("/payment_interface/confirm/<string:serial>/<string:token>")
def paymentVerify(serial, token):
    shopCardPoints.makePayment(conn, cursor, serial, token, "paid")
    paymentInfo = shopCardPoints.getUserInfo(conn, cursor, serial, token)

    return {"status":paymentInfo[3]}

@app.route("/eula/<int:code>/en.html")
def random_app(code):
    return render_template('str2hax.html')

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    # Hint that we are about to use very brittle ciphers.
    #context.set_ciphers('ALL:@SECLEVEL=0')
    #context.load_cert_chain('cert.pem', 'key.pem')

    app.run(host="192.168.2.51", port=8081, debug=True) #, ssl_context=context) # socket.gethostbyname(socket.gethostname())
