import requests
import numpy as np
from constants import *
from random import sample, choice
import cv2

# the main mechanism
class Controller(object):
    def __init__(self):
        self.memory = np.zeros((MEMORY_SIZE, DATA_SIZE))
        self.groups = list(GROUPS.keys())
        self.near_tick = 0
        self.release_tick = 0
        self.super_release = 0

    def run(self, datas):
        level, datas = self.get_level(datas)
        data = np.zeros(DATA_SIZE)
        if (self.super_release):
            data[REALEASE_MOTOR] = 1
            self.super_release -= 1
            self.near_tick = 0
        else :
            if level == 'near':
                if self.near_tick <= len(PRIORITY) + HOLD_TIME:
                    self.near_tick += 1
                data  = self.output_near(datas)
            else :
                if self.near_tick > 0 :
                    self.near_tick -= 1
            if level == 'mid':
                data = self.output_mid(datas)            
            elif level == 'far':
                data = self.output_far(datas)
            elif level == 'none':
                data = self.output_random(datas)
            data = self.release(data)
        self.refresh_memory(data)
        data = data.astype('int8').tolist()
        print(data)
        self.post_data(data)
        return data

    def detect_click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            if x < 620 and x > 580 and y < 340 and y > 300 :
                self.super_release = REALEASE_HOLDTIME

    def get_level(self, datas):
        filter_dist = lambda x, rule :  rule[0] < x['distance'] and rule[1] >= x['distance']
        near = list(filter(lambda x: filter_dist(x, NEAR), datas))
        mid = list(filter(lambda x: filter_dist(x, MID), datas))
        far = list(filter(lambda x: filter_dist(x, FAR), datas))   
        if len(near):
            return 'near', near
        elif len(mid):
            return 'mid', mid
        elif len(far):
            return 'far', far
        else:
            return 'none', None

    def output_near(self, datas):
        data = np.zeros(DATA_SIZE)
        for i in range(min(self.near_tick, len(PRIORITY))):
            for m in PRIORITY[i]:
                data[m] = 1
        return data

    def output_mid(self, datas):
        group = self.condition2group(datas, 'eyesight')
        group = sample(group, GROUP_NUM)
        data = self.output(group, FULL)
        return data

    def output_far(self, datas):
        group = self.condition2group(datas, 'position')
        group = sample(group, GROUP_NUM)
        data = self.output(group, FULL)
        return data

    def output_random(self, datas):
        group = sample(self.groups, GROUP_NUM)
        data = self.output(group, HALF)
        return data

    def output(self, group, capcity):
        data = np.zeros(DATA_SIZE)
        for k in group:
            for i in range(MOTOR_NUM):
                motors = GROUPS[k]
                m = motors[0]
                if(self.check_capcity(m, capcity)):
                    m = choice(motors)  
                if(self.check_capcity(m, capcity)):
                    m = choice(motors)
                data[m] = 1
        return data

    def refresh_memory(self, data):
        self.memory = np.delete(self.memory, 0, 0)
        self.memory = np.concatenate([self.memory, [data]], 0)

    def check_capcity(self, idx, capcity):
        row = self.memory[:,idx]
        cap = capcity[idx]
        return np.sum(row[-cap:]) == cap or np.sum(row) >= MEMORY_THRESHOLD

    def condition2group(self, datas, key):
        parse = lambda x, k : DIRECTION2GROUP[x[k][0] + 1][x[k][1] + 1]
        group = list(map(lambda x: parse(x, key), datas))
        return group

    def condition2score(self, datas, key):
        group = list(map(lambda x: parse(x), datas))
        return group

    def release(self, data):
        if self.release_tick < REALEASE_OPEN :
            data[REALEASE_MOTOR] = 1
        else :
            data[REALEASE_MOTOR] = 0
        self.release_tick += 1
        self.release_tick %= REALEASE_TICK
        return data

    def post_data(self, data):
        r = requests.post('http://{}:{}/{}'.format(IP, PORT, API), json={"data": data})