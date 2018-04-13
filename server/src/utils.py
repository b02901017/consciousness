import cv2
import matplotlib.pyplot as plt
import numpy as np
from constants import *
from keras.preprocessing import image
from scipy.misc import imread, imresize

def detect_faces(detector, gray_img):
    return detector(gray_img, 1)

def box2coordinate(box):
    left = box.left()
    top = box.top()
    right = box.right()
    bottom = box.bottom()
    return [left, top, right-left, bottom-top]

def coordinate2box(coordinate):
    x, y, w, h = coordinate
    return [x, x+w, y, y+h]

def apply_offsets(coordinate, offsets):
    x, y, w, h = coordinate
    x_off, y_off = offsets
    return (x - x_off, x + w + x_off, y - y_off, y + h + y_off)

def pred2emotion(pred, labels):
    label = np.argmax(pred)
    labels.append(label)
    if len(labels) > WINDOW_SIZE:
        labels.pop(0)
    try:
        label = mode(labels)
    except:
        pass
    return emotion2label[label], labels

def pred2gender(pred, labels):
    label = np.argmax(pred)
    labels.append(label)
    if len(labels) > WINDOW_SIZE:
        labels.pop(0)
    try:
        label = mode(labels)
    except:
        pass
    return gender2label[label], labels

def pred2lcolor(pred):
    prob = np.max(pred)
    label = np.argmax(pred)
    color = prob * COLORS[label]
    color = color.astype(int)
    color = color.tolist()
    return color

def load_image(image_path, grayscale=False, target_size=None):
    pil_image = image.load_img(image_path, grayscale, target_size)
    return image.img_to_array(pil_image)

def _imread(image_name):
    return imread(image_name)

def _imresize(image_array, size):
    return imresize(image_array, size)

def to_categorical(integer_classes, num_classes=2):
    integer_classes = np.asarray(integer_classes, dtype='int')
    num_samples = integer_classes.shape[0]
    categorical = np.zeros((num_samples, num_classes))
    categorical[np.arange(num_samples), integer_classes] = 1
    return categorical

