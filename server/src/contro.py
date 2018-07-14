import requests
import numpy as np
from constants import *
from random import sample, choice, shuffle
import cv2
from functools import reduce

# the main mechanism
class Controller(object):
    def __init__(self):
        self.groups = list(GROUPS.keys())
        self.queue = np.zeros([DATA_SIZE, 2], dtype = int)
        self.state = np.zeros([len(self.groups), 2])
        self.super_release = REALEASE_HOLDTIME
        self.super_halt = 0

    def empty(self):   
        self.queue = np.zeros([DATA_SIZE, 2], dtype = int)
        self.state = np.zeros([len(self.groups), 2])

    def run(self, datas):
        level, datas = self.get_level(datas)
        data = np.zeros(DATA_SIZE)
        if (self.super_halt):
            data = self.output_halt()
        elif (self.super_release):
            data = self.output_none()
        else :
            if level == 'far':
                score = self.calculate_score(datas)
                self.update_state(score)
                group = self.select_group()
                motors = self.select_motor(group)
                self.update_queue(motors)
                data = self.output_far()
            elif level == 'none':
                self.super_release = REALEASE_HOLDTIME
                data = self.output_none()
        data = data.astype('int8').tolist()
        print(data)
        self.post_data(data)
        return data

    def detect_click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            if x < 620 and x > 580 and y < 340 and y > 300 :
                self.super_release = REALEASE_HOLDTIME
                self.super_halt = 0
            if x < 60 and x > 20 and y < 340 and y > 300 :
                self.super_halt = HALT_HOLDTIME
                self.super_release = 0
                

    def get_level(self, datas):
        if len(datas):
            return 'far', datas
        else:
            return 'none', None
    
    def calculate_score(self, datas):
        parse = lambda x: (x['position'][0] + 1, x['number'])
        datas = list(map(lambda x: parse(x), datas))
        score = np.zeros(len(self.groups))
        for idx, n in datas:
            score[idx] += 1 /n
            # score[idx] += 1
        return score

    def update_state(self, score):
        self.state[:, 1] += score

    def select_group(self):
        group = []
        for i, st in enumerate(self.state):
            b, s = st
            if s >= BANCHNARK[min(int(b), len(BANCHNARK)-1)]:
                self.state[i][0] += 1
                group.append(self.groups[i])
        return group

    def select_motor(self, trigger):
        motors = []
        for g in trigger:
            m = GROUPS[g]
            shuffle(m)
            m = m[:MOTOR_NUM]
            motors += m
        return motors

    def update_queue(self, motors):
        for m in motors:
            if not self.queue[m][0]:
                self.queue[m][0] = 1
                self.queue[m][1] = HALF[m]
            if self.queue[m][0] == 2:
                self.queue[m][0] = 3
                self.queue[m][1] = FULL[m]

    def output_far(self):
        data = np.zeros(DATA_SIZE)
        for i, q in enumerate(self.queue):
            s, c = q
            if((s == 1 or s == 3) and c):
                self.queue[i][1] -= 1
                data[i] = 1
            if(s == 1 and not c):
                self.queue[i][0] = 2
            if(s == 3 and not c):
                self.queue[i][0] = 4
        return data
        
    def output_none(self):
        data = np.zeros(DATA_SIZE)
        data[RELEASE] = 1
        self.empty()
        self.super_halt = 0
        self.super_release -= 1
        return data
        
    def output_halt(self):
        data = np.zeros(DATA_SIZE)
        self.empty()
        self.super_release = 0
        self.super_halt -= 1
        return data

    def post_data(self, data):
        r = requests.post('http://{}:{}/{}'.format(IP, PORT, API), json={"data": data})
