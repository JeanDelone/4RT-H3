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

# Find contours in the image
contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter the contours by area and shape approximation
shapes = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area < 1000:
        continue
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
    if len(approx) == 3:
        shapes.append("Triangle")
    elif len(approx) == 4:
        shapes.append("Rectangle")
    elif len(approx) == 5:
        shapes.append("Pentagon")
    elif len(approx) == 6:
        shapes.append("Hexagon")

# Draw the detected shapes on a black image
shapes_img = np.zeros_like(img)

for contour in contours:
    area = cv2.contourArea(contour)
    if area < 1000:
        continue
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
    if len(approx) <= 6:
        cv2.drawContours(shapes_img, [contour], 0, (255, 255, 255), 2)

# Display the original image and the simplified image with the detected shapes
cv2.imshow('Original Image', img)
cv2.imshow('Simplified Image with Shapes', shapes_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the detected shapes
print("Detected Shapes:")
for shape in shapes:
    print(shape)
