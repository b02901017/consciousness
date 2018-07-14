import cv2
import matplotlib.pyplot as plt
import numpy as np
from imutils import face_utils
from imutils.object_detection import non_max_suppression
from utils import *
from constants import *
import math


def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x

# get each eye sight
def process_eye(shape, gray_img, offsets, index):
    i, j = FACIAL_LANDMARKS_IDXS[index]
    eye = shape[i:j]
    eye = cv2.boundingRect(np.array([eye]))
    x1, x2, y1, y2 = apply_offsets(eye, offsets)
    eye = gray_img[y1:y2,x1:x2]
    eye = cv2.equalizeHist(eye)
    eye = cv2.threshold(eye, THRESH, 255, cv2.THRESH_BINARY)[1]
    zero = np.where(eye == 0)
    eye = np.asarray([eye.shape[1], eye.shape[0]]) / 2
    ball = np.asarray([np.mean(zero[1]), np.mean(zero[0])])
    shift = (eye - ball) / eye
    return shift

# def detect_faces(detection_model, gray_img):
#     return detection_model.detectMultiScale(gray_img, 1.3, 5)

# peoplr
def detect_people(detector, bgr_img):
	(rects, weights) = detector.detectMultiScale(
        bgr_img, winStride=(8, 8), padding=(16, 16), scale=1.06)
	rects = non_max_suppression(rects, probs=None, overlapThresh=0.65)
	return rects


# faces
def detect_faces(detector, gray_img):
    return detector(gray_img, 1)

# set of features
def detect_shape(detector, face, gray_img):
    shape = detector(gray_img, face)
    shape = face_utils.shape_to_np(shape)
    return shape

# number of peoples
def detect_peoples(faces):
    return len(faces)

# distance
def detect_distance(face, gray_img):
    _, _, face_w, face_h = face
    h, w = gray_img.shape
    return np.round(np.sqrt((face_w * face_h) / (w * h)), 3)

# eyesight
def detect_eyesight(detector, face, gray_img):
    shape = detect_shape(detector, face, gray_img)
    left_shift = process_eye(shape, gray_img, EYE_OFFSETS, 'left_eye') - LEFT_CENTER
    right_shift = process_eye(shape, gray_img, EYE_OFFSETS, 'right_eye') - RIGHT_CENTER
    shift =  left_shift + right_shift
    hor, ver  = shift
    if (np.abs(hor) < EYEX_THRESHOLD):
        hor = 0
    if (np.abs(ver) < EYEY_THRESHOLD):
        ver = 0
    return (-int(np.sign(hor)), int(np.sign(ver)))

# position
def detect_position(face, gray_img):
    x, y, face_w, face_h = face
    h, w = gray_img.shape       
    x = x + face_w/2 - w/ 2
    y = y + face_h/2 - h /2
    x = 2 * face_w * x/ (w*w)
    y = 2 * face_h * y/ (h*h)
    # for the postion bias    
    if (np.abs(x) < POSX_THRESHOLD):
        x = 0
    if (np.abs(y) < POSY_THRESHOLD):
        y = 0
    return (-int(np.sign(x)), int(np.sign(y)))
    # return np.round(face_w * x/ w, 3), np.round(face_h * y/ face_h, 3) 
    

# emotion
def detect_emotion(classifier, face, gray_img, emotions):
    x1, x2, y1, y2 = apply_offsets(face, EMOTION_OFFSETS)
    gray_face = gray_img[y1:y2, x1:x2]
    try:
        gray_face = cv2.resize(gray_face, (EMOTION_SIZE))
    except:
        pass
    gray_face = preprocess_input(gray_face, True)
    gray_face = np.expand_dims(gray_face, 0)
    gray_face = np.expand_dims(gray_face, -1)
    pred = classifier.predict(gray_face)
    emotion, emotions = pred2emotion(pred, emotions)
    color = pred2lcolor(pred)
    return emotion, emotions, color, np.argmax(pred)

# gender
def detect_gender(classifier, face, rgb_img, genders):
    x1, x2, y1, y2 = apply_offsets(face, GENDER_OFFSETS)
    rgb_face = rgb_img[y1:y2, x1:x2]
    try:
        rgb_face = cv2.resize(rgb_face, (GENDER_SIZE))
    except:
        pass
    rgb_face = np.expand_dims(rgb_face, 0)
    rgb_face = preprocess_input(rgb_face, False)
    pred = classifier.predict(rgb_face)
    gender, genders = pred2gender(pred, genders)
    color ={
        'man': (0, 0, 255),
        'woman': (255,0,0)
    }[gender]
    return gender, genders, color, np.argmax(pred)
