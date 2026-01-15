import cv2 as cv

input_img = cv.imread("models/marker.jpg")

if input_img is None:
    exit()

# vector<int> markerIds
# vector<cv::Point2f> markerCorners, rejectedCandidates

detector_params = cv.aruco.DetectorParameters()
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
detector = cv.aruco.ArucoDetector(dictionary, detector_params)

(markerCorners, markerIds, rejectedCandidates) = detector.detectMarkers(input_img)

output_img = input_img.copy()
cv.aruco.drawDetectedMarkers(output_img, markerCorners, markerIds)


cv.imshow("Input", input_img)
cv.imshow("Output", output_img)
k = cv.waitKey(0)
