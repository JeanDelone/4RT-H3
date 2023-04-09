import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import random

# reading image
img = cv.imread('Images/skull.png')

# converting image into grayscale image
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# setting threshold of gray image
_, threshold = cv.threshold(gray, 233, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

for contour in contours:
    cv.drawContours(img, [contour], 0, (255,0,255), 2)

cv.imshow('shapes', threshold)

cv.waitKey(0)
cv.destroyAllWindows()
