import cv2
from constants import *

def get_colors(num_classes):
    colors = plt.cm.hsv(np.linspace(0, 1, num_classes)).tolist()
    colors = np.asarray(colors) * 255
    return colors

def draw_bounding_box(coordinate, image_array, color):
    x, y, w, h = coordinate
    cv2.rectangle(image_array, (x, y), (x + w, y + h), color, 2)

def draw_shape_dot(coordinate, image_array, color, index, size):
    i, j = FACIAL_LANDMARKS_IDXS[index]
    for (x, y) in shape[i:j]:
        cv2.circle(image_array, (x, y), size, color, -1)

def draw_text(coordinate, image_array, text, color, x_offset=0, y_offset=0,
                                                font_scale=2, thickness=2):
    x, y = coordinate[:2]
    cv2.putText(image_array, text, (x + x_offset, y + y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness, cv2.LINE_AA)
