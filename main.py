import math
import cvzone
import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGameClass:
    def __init__(self):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each points
        self.currentLength = 0  # total length of snake
        self.allowedLength = 150  # total allowed length
        self.previousHead = 0, 0

    def update(self, imgMain, currentHead):
        px, py = self.previousHead  # px = previous x
        cx, cy = currentHead  # cx = current x

        self.points.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lengths.append(distance)
        self.currentLength += distance
        self.previousHead = cx, cy

        # Length Reduction of Snake
        if self.currentLength > self.allowedLength:
            for i, length in enumerate(self.lengths):
                self.currentLength -= length
                self.lengths.pop(i)
                self.points.pop(i)

                if self.currentLength < self.allowedLength:
                    break

        # Draw snake
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:
                    cv.line(imgMain, self.points[i-1],
                            self.points[i], (180, 60, 255), 20)
            cv.circle(imgMain, self.points[-1], 10, (200, 0, 200), cv.FILLED)
        return imgMain

game = SnakeGameClass()

while True:
    success, img = cap.read()
    # To flip image
    img = cv.flip(img, 1)
    hand, img = detector.findHands(img, flipType=False)

    if hand:
        lmList = hand[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)

    cv.imshow("Image", img)
    cv.waitKey(1)
