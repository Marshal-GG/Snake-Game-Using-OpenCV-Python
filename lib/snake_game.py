import math
import os
import random
import cvzone
import numpy as np
import cv2 as cv


class SnakeGameClass:
    def __init__(self):
        self.points = []  # All points of the snake
        self.lengths = []  # Distance between each points
        self.currentLength = 0  # Total length of snake
        self.allowedLength = 150  # Total allowed length
        self.previousHead = 0, 0  # Previous head point
        self.direction = "RIGHT"  # Initial direction

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
            cvzone.putTextRect(imgMain, 'Game Over', [
                               300, 400], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [
                               300, 550], scale=7, thickness=5, offset=20)

        else:
            px, py = self.previousHead  # px = previous x
            cx, cy = currentHead  # cx = current x

            # Update direction based on current and previous head positions
            if cx > px:
                self.direction = "RIGHT"
            elif cx < px:
                self.direction = "LEFT"
            elif cy > py:
                self.direction = "DOWN"
            elif cy < py:
                self.direction = "UP"

            # Move snake in the current direction
            if self.direction == "RIGHT":
                cx += 1
            elif self.direction == "LEFT":
                cx -= 1
            elif self.direction == "DOWN":
                cy += 1
            elif self.direction == "UP":
                cy -= 1

            # Check if snake is outside the screen
            if cx < 0 or cy < 0 or cx > 1280 or cy > 720:
                self.gameOver = True

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
                        # Draw a line between the current and previous point
                        prev_point = self.points[i-1]
                        cv.line(imgMain, (int(prev_point[0]), int(prev_point[1])), (int(
                            point[0]), int(point[1])), (180, 60, 255), 15)
                # Draw the head of the snake as a circle
                cv.circle(imgMain, (int(
                    self.points[-1][0]), int(self.points[-1][1])), 15, (200, 0, 200), cv.FILLED)

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

            if self.points:
                # Check if snake is moving
                if self.points[-1] != self.previousHead:
                    self.previousHead = self.points[-1]
                    self.gameOverCounter = 0
                else:
                    self.gameOverCounter += 1

                # Check if snake hits the boundary
                if cx < 50 or cx > 1100 or cy < 50 or cy > 650:
                    self.gameOverCounter = 0
                    self.gameOver = True

                # Check for collision with body of snake
                if -1 <= minDist <= 1 and self.gameOverCounter > 10:
                    print('Hit')
                    self.gameOver = True
                    self.points = []  # All points of the snake
                    self.lengths = []  # Distance between each points
                    self.currentLength = 0  # Total length of snake
                    self.allowedLength = 150  # Total allowed length
                    self.previousHead = 0, 0  # Previous head point
                    self.randomFoodAndLocation()
                    self.score = 0

        return imgMain
