import numpy as np

detection_model_path = 'model/face.xml'
shape_model_path = 'model/shape.dat'
emotion_model_path = 'model/emtion.hdf5'
gender_model_path = 'model/gender.hdf5'

emotion2label = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
gender2label =  ['woman','man']

WINDOW_SIZE = 5
THRESH = 160

EMOTION_SIZE = (64, 64)
GENDER_SIZE = (48, 48)

EMOTION_OFFSETS = (20, 40)
GENDER_OFFSETS  = (30, 60)
EYE_OFFSETS = (1, 2)
EYEX_THRESHOLD = 0.1
EYEY_THRESHOLD = 0.1

FACIAL_LANDMARKS_IDXS = {
    'mouth' : (48, 68),
    'right_eyebrow': (17, 22),
	'left_eyebrow': (22, 27),
	'right_eye': (36, 42),
	'left_eye': (42, 48),
    'eyes' : (36, 48),
	'nose': (27, 35),
	'jaw': (0, 17),
    'all' : (0,68)
}

RED = np.asarray((255, 0, 0))
GREEN = np.asarray((255, 0, 0))
PURPLE = np.asarray((192, 0, 192))
YELLOW = np.asarray((255, 255, 0))
BLUE = np.asarray((0, 0, 255))
MAGENTA = np.asarray((0, 255, 255))
CYAN = np.asarray((0, 255, 255))

COLORS = [RED, GREEN, PURPLE, YELLOW, BLUE, MAGENTA, CYAN]

LEFT_CENTER = np.asarray((-0.2, 0.05))
RIGHT_CENTER = np.asarray((0.3, 0.05))

IP = '172.20.10.2'
PORT = 3000
API = 'api/rpi/data/'

# time
SUBMIT_TICK = 1 # how often do we submit to rpi
REALEASE_HOLDTIME = 20 # for super release
HALT_HOLDTIME = 10 # for super halt
FULL = [
	28, 14, 9, 0, 
	11, 11, 0, 0,
	20, 0, 10, 0,
	11, 11, 0, 0, 
	28, 14, 9, 5,
	0, 0, 0, 0,
]
HALF = [
	15, 7, 5, 0, 
	6, 6, 0, 0,
	10, 0, 6, 0,
	6, 6, 0, 0, 
	15, 7, 5, 3,
	0, 0, 0, 0,
]
# sample num
MOTOR_NUM = 2 # how many motor to trigger per group

POSX_THRESHOLD = 0.04
POSY_THRESHOLD = 0.12
# specific motor
REALEASE_MOTOR = 3 # the idx of release specific motor
GROUPS = {
	'L': [0, 1, 2, 4, 5],
	'M': [4, 5, 8, 19, 10, 12, 13],
	'R': [12, 13, 16, 17, 18],
}
RELEASE = [3, 6, 7, 11, 14]

DIRECTION2GROUP = ['L', 'M', 'R']
BANCHNARK = [5, 15, 30, 60, 100, 150]
# size
DATA_SIZE = 24 # output size 