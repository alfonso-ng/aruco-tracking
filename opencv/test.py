import cv2 as cv

img = cv.imread("models/example.jpg")

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
markerImage = cv.aruco.generateImageMarker(dictionary, 23, 200, None, 1)
cv.imwrite("./models/marker.jpg", markerImage)

if markerImage is not None:
    cv.imshow("Display window", markerImage)

k = cv.waitKey(0)
cv.aruco.ArucoDetector
