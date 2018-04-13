import requests
from constants import *

# the main mechanism
def encode(i, number = 0, dis = 0.0, hor = 0, ver = 0, g_idx = 0, e_idx = 0):
    data = [0] * DATA_SIZE
    data[i] = 1
    return data

# sned to rpi
def post_data(data):
    # 
    r = requests.post('http://{}:{}/{}'.format(IP, PORT, API), json={"data": data})