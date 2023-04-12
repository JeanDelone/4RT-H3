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

# Find the contours of the shapes in the image
contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw the detected contours on a black image
shapes_img = np.zeros_like(img)
cv2.drawContours(shapes_img, contours, -1, (255, 255, 255), thickness=2)

# Display the original image and the simplified image with the detected shapes
cv2.imshow('Original Image', img)
cv2.imshow('Simplified Image with Shapes', shapes_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
