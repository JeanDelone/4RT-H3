import matplotlib.pyplot as plt
import cv2 as cv

x = [x for x in range(0,256)]
y = []
print(x)

for i in x:
    img = cv.imread("Images/skull.png")
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, threshold = cv.threshold(gray, i, 255, cv.THRESH_BINARY)
    y.append(cv.countNonZero(threshold))
print(y)
plt.plot(x,y)
plt.show()