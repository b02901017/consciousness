from statistics import mode
import cv2
from keras.models import load_model
import numpy as np
import dlib
from constants import *
from inference import *
from draw import *
from utils import *
from message import *
from time import sleep


def main(face_dtr, shape_dtr, emotion_clf, gender_clf):
    # starting video streaming
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('window_frame')
    emotions = []
    genders = []
    i = 0           
    counter = 0                  
    while True:
        try :
            ret, bgr_img = cap.read()
            gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
            rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
            faces = detect_faces(face_dtr, gray_img)
        except:
            print('capture dead')
        # number of people
        number = detect_peoples(faces)
        draw_text([20,100], rgb_img, str(number), (0,255,0), 0, -45, 1, 1)
        for face in faces:
            try :
                # eye sight
                hor, ver = detect_eyesight(shape_dtr, face, gray_img)
                # trnsform
                face = box2coordinate(face)
                draw_text(face, rgb_img, 'h:{} v:{}'.format(hor, ver), (224,224,224), 0, -60, 0.5, 1)
                # distance
                dis = detect_distance(face, gray_img)
                draw_text(face, rgb_img, str(dis), (224,224,224), 0, -45, 0.5, 1)
                # gender
                gender, genders, color, g_idx = detect_gender(gender_clf, face, rgb_img, genders)
                draw_text(face, rgb_img, gender, color, 0, -15, 0.5, 1)
                # emotion
                emotion, emotions, color, e_idx = detect_emotion(emotion_clf, face, gray_img, emotions)
                draw_text(face, rgb_img, emotion, color, 0, -30, 0.5, 1)
                draw_bounding_box(face, rgb_img, color)
            except:
                print('model dead')
            # try :
            data = encode(i, number, dis, hor, ver, g_idx, e_idx)
            post_data(data)
                # # subimit data to rpi
                # if(counter % SUBMIT_FREQ == 0) :
                #     data = encode(i, number, dis, hor, ver, g_idx, e_idx)
                #     post_data(data)
                #     i += 1
                #     i %= DATA_SIZE
                #     counter %= SUBMIT_FREQ
            # except:
                # print('streaming dead')

        bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_img)
        counter += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    # loading models
    ## cascad
    # face_dtr = cv2.Cascadeclf(detection_model_path)
    ## dlib
    face_dtr = dlib.get_frontal_face_detector()
    shape_dtr = dlib.shape_predictor(shape_model_path)
    emotion_clf = load_model(emotion_model_path, compile=False)
    gender_clf = load_model(gender_model_path, compile=False)

    main(face_dtr, shape_dtr, emotion_clf, gender_clf)