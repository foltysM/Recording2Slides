import cv2 as cv
import numpy as np

import sys
import random

THRESHOLD = 95


cap = cv.VideoCapture('test2.mp4')
i, last_i = 0, 0
frame_list = []

lower_black = np.array([0, 0, 0])  # HSV
upper_black = np.array([180, 255, 30])

ret, last_frame = cap.read()
j = 0
blacks = []
greens = []

cv.namedWindow("Preview", cv.WINDOW_KEEPRATIO)

while True:
    ret, frame30 = cap.read()
    if not ret:
        print("A problem")
        break

    imr = cv.resize(frame30, (480, 270))
    cv.imshow("Preview", imr)

    diff = cv.absdiff(frame30, last_frame)

    last_frame = frame30

    diff_hsv = cv.cvtColor(diff, cv.COLOR_BGR2HSV)

    mask_black = cv.inRange(diff_hsv, lower_black, upper_black)
    res = cv.bitwise_and(frame30, frame30, mask=mask_black)

    black_percent = (mask_black > 0).mean()
    print(black_percent)
    if black_percent < THRESHOLD/100 and j > 80:
        cv.imwrite('slide' + str(j) + '.jpg', frame30)
    j += 1
    blacks.append(black_percent)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
