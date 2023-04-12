import cv2
import numpy as np

# Load the image
img = cv2.imread('../Images/skull.png')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply edge detection using the Canny algorithm
edges = cv2.Canny(gray, 100, 200)

# Apply dilation and erosion to remove any small gaps in the edges
kernel = np.ones((5,5), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=1)
eroded = cv2.erode(dilated, kernel, iterations=1)

# Detect circles using the Hough transform
circles = cv2.HoughCircles(eroded, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

# Detect lines using the Hough transform
lines = cv2.HoughLinesP(eroded, rho=1, theta=np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)

# Draw the detected circles and lines on a black image
shapes_img = np.zeros_like(img)

if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        cv2.circle(shapes_img, (x, y), r, (255, 255, 255), 2)

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(shapes_img, (x1, y1), (x2, y2), (255, 255, 255), 2)

# Display the original image and the simplified image with the detected shapes
cv2.imshow('Original Image', img)
cv2.imshow('Simplified Image with Shapes', shapes_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
