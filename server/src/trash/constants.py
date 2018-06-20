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
REALEASE_HOLDTIME = 30 # for super release
REALEASE_OPEN = 3  # how long do we open relaese motor
REALEASE_CLOSE = 3  # how long do close relaese motor
REALEASE_TICK = REALEASE_CLOSE + REALEASE_OPEN
HOLD_TIME = 0 # the near mode hold up time
FULL = [
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3
]
HALF = [
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3
]
# sample num
GROUP_NUM = 3 # how many group to trigger
MOTOR_NUM = 1 # how many motor to trigger per group
# distance
NEAR = (0.075, 0.388)
MID =  (0.3, 0.3) # for eyesight, ex close (0.3,0.3)
FAR =  (0.08, 0.08) # for position, ex close (0.0, 0.0)

POSX_THRESHOLD = 0.04
POSY_THRESHOLD = 0.12
EYEX_THRESHOLD = 0.1
EYEY_THRESHOLD = 0.1
# specific motor
REALEASE_MOTOR = 3 # the idx of release specific motor
GROUPS = {
	'LU': [0, 1, 4],
	'MU': [19, 4, 8, 12],
	'RU': [16, 12, 17],
	'LM': [1, 5],
	'MM': [10, 5, 13],
	'RM': [17, 13],
	'LD': [2, 1, 5],
	'MD': [2, 1, 5, 18, 13, 17],	
	'RD': [18, 13, 17],
}
DIRECTION2GROUP = [
	['LU', 'MU', 'RU'],
	['LM', 'MM', 'RM'],
	['LD', 'MD', 'RD'],
]
PRIORITY = [
	[10],
	[5, 13],
	[0, 16],
	[9],
	[4, 12, 1, 17],
	[2, 8, 18],	
]
# size
DATA_SIZE = 24 # output size 
MEMORY_SIZE = 10 # how long do we open
# count for saturate
MEMORY_THRESHOLD = 5