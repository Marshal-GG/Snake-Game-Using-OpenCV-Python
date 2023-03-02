import math
import os
import random
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
        self.points = []  # All points of the snake
        self.lengths = []  # Distance between each points
        self.currentLength = 0  # Total length of snake
        self.allowedLength = 150  # Total allowed length
        self.previousHead = 0, 0  # Previous head point

        # Load food images from directory
        foodDir = "images/foods"
        self.foodImages = []
        for filename in os.listdir(foodDir):
            img = cv.imread(os.path.join(foodDir, filename),
                            cv.IMREAD_UNCHANGED)
            img = cv.resize(img, (50, 50))
            self.foodImages.append(img)
        self.numFoodImages = len(self.foodImages)

        # Select a random food image
        self.imgFood = self.foodImages[random.randint(0, self.numFoodImages-1)]
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoints = 0, 0
        self.randomFoodAndLocation()

        self.score = 0
        self.gameOver = False

    def randomFoodAndLocation(self):
        # Select a new random food location
        self.foodPoints = random.randint(100, 1000), random.randint(100, 600)

        # Select a new random food image
        self.imgFood = self.foodImages[random.randint(0, self.numFoodImages-1)]
        self.hFood, self.wFood, _ = self.imgFood.shape

    def update(self, imgMain, currentHead):

        if self.gameOver:
            cvzone.putTextRect(imgMain, 'Gmae Over', [
                               300, 400], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [
                               300, 550], scale=7, thickness=5, offset=20)

        else:
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

            # Check if snake eat the Food
            rx, ry = self.foodPoints  # rx = random x
            if rx - self.wFood//2 < cx < rx + self.wFood//2 and ry - self.hFood//2 < cy < ry + self.hFood//2:
                self.randomFoodAndLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv.line(imgMain, self.points[i-1],
                                self.points[i], (180, 60, 255), 5)
                cv.circle(imgMain, self.points[-1],
                          10, (200, 0, 200), cv.FILLED)

            # Draw Food
            rx, ry = self.foodPoints
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.wFood//2, ry - self.hFood//2))

            cvzone.putTextRect(imgMain, f'Score: {self.score}', [
                50, 80], scale=3, thickness=3, offset=10)

            # Check for collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv.polylines(imgMain, [pts], False, (100, 200, 50), 3)
            minDist = cv.pointPolygonTest(pts, (cx, cy), True)
            # print(minDist)

            if -1 <= minDist <= 1:
                print('Hit')
                self.gameOver = True  # Resets the Game
                self.points = []  # All points of the snake
                self.lengths = []  # Distance between each points
                self.currentLength = 0  # Total length of snake
                self.allowedLength = 150  # Total allowed length
                self.previousHead = 0, 0  # Previous head point
                self.randomFoodAndLocation()
                self.score = 0

        return imgMain


game = SnakeGameClass()

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)  # To flip image
    hand, img = detector.findHands(img, flipType=False)

    if hand:
        lmList = hand[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)

    cv.imshow("Image", img)
    key = cv.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
