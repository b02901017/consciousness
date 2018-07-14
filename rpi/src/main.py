from multiprocessing import Process, Value, Array
import time
from flask import Flask, request, jsonify
import requests
import sys
import json
from i2c import *
import json

HOST = '0.0.0.0'
PORT = 3000

app = Flask(__name__)

data = Array('i', [0]*24)
flag = Value('i', 0)

@app.route('/api/rpi/data/', methods=['POST'])
def get_data():
    req = json.loads(request.data.decode('utf-8'))['data']
    print(req)
    data[:] = req
    return jsonify(req)

@app.route("/")
def hello():
    return "Hello"

def loop(flag, data):
    while True:
        transmit(data[:])
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=loop, args=(flag, data))
    p.start()
    app.run(debug=False, use_reloader=False, port=PORT, host=HOST)
    p.join()
