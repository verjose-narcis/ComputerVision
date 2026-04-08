# metrics.py

import math


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def calculate_ear(face_landmarks, eye_indices, w, h, get_point_float):
    p1 = get_point_float(face_landmarks, eye_indices[0], w, h)
    p2 = get_point_float(face_landmarks, eye_indices[1], w, h)
    p3 = get_point_float(face_landmarks, eye_indices[2], w, h)
    p4 = get_point_float(face_landmarks, eye_indices[3], w, h)
    p5 = get_point_float(face_landmarks, eye_indices[4], w, h)
    p6 = get_point_float(face_landmarks, eye_indices[5], w, h)

    vertical_1 = distance(p2, p5)
    vertical_2 = distance(p3, p6)
    horizontal = distance(p1, p4)

    if horizontal == 0:
        return 0.0

    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def calculate_mar(face_landmarks, mouth_indices, w, h, get_point_float):
    left_point = get_point_float(face_landmarks, mouth_indices[0], w, h)
    top_point = get_point_float(face_landmarks, mouth_indices[1], w, h)
    right_point = get_point_float(face_landmarks, mouth_indices[2], w, h)
    bottom_point = get_point_float(face_landmarks, mouth_indices[3], w, h)

    vertical = distance(top_point, bottom_point)
    horizontal = distance(left_point, right_point)

    if horizontal == 0:
        return 0.0

    return vertical / horizontal