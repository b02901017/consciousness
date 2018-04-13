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


IP = '192.168.1.10'
PORT = 3000
API = 'api/rpi/data/'
DATA_SIZE = 16