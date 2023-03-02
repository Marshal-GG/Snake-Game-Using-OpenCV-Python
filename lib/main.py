import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from snake_game import SnakeGameClass

cap = cv.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

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
    elif key == ord('q'):
        break
