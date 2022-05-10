import math
import random

import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGameAI:

    def __init__(self, pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # Distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # Total allowed length
        self.previousHead = 0, 0  # previous head point

        self.imageFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imageFood.shape
        self.foodPoints = 0, 0
        self.randomFoodLocation()

        self.score = 0

    def randomFoodLocation(self):
        self.foodPoints = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):

        px, py = self.previousHead
        cx, cy = currentHead

        self.points.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lengths.append(distance)
        self.currentLength += distance
        self.previousHead = cx, cy

        # Length Reduction
        if self.currentLength > self.allowedLength:
            for i, length in enumerate(self.lengths):
                self.currentLength -= length
                self.lengths.pop(i)
                self.points.pop(i)

                if self.currentLength < self.allowedLength:
                    break

        # check if the snake ate the food
        rx, ry = self.foodPoints
        if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                ry - self.hFood // 2 < cy < ry + self.hFood // 2:
            self.randomFoodLocation()
            self.allowedLength += 50
            self.score += 1
            print(self.score)

        # check if win
        if self.score == 10:
            cvzone.putTextRect(imgMain, "Congrat.", [300, 400],
                               scale=7, thickness=5, offset=20)

        # Draw snake
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:
                    cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 255, 0), 20)
            cv2.circle(img, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

        # Draw Food
        imgMain = cvzone.overlayPNG(imgMain, self.imageFood,
                                    (rx - self.wFood // 2, ry - self.hFood // 2))

        cvzone.putTextRect(imgMain, f'Your score: {self.score}', [50, 80],
                           scale=3, thickness=3, offset=10)

        return imgMain


testGame = SnakeGameAI("apple.png")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = testGame.update(img, pointIndex)

    cv2.imshow("AI Snake Game", img)
    key = cv2.waitKey(1)

    if key == ord('r' or 'R'):
        testGame.points = []  # all points of the snake
        testGame.lengths = []  # Distance between each point
        testGame.currentLength = 0  # total length of the snake
        testGame.allowedLength = 150  # Total allowed length
        testGame.previousHead = 0, 0  # previous head point
        testGame.randomFoodLocation()
        testGame.score = 0
    elif key == ord('c' or 'C'):
        exit()
