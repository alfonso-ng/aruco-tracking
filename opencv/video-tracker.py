import cv2 as cv

detector_params = cv.aruco.DetectorParameters()
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
detector = cv.aruco.ArucoDetector(dictionary, detector_params)

input_video = cv.VideoCapture(0)
if not input_video.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = input_video.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    detector_params = cv.aruco.DetectorParameters()
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
    detector = cv.aruco.ArucoDetector(dictionary, detector_params)

    (markerCorners, markerIds, rejectedCandidates) = detector.detectMarkers(gray)

    output_img = gray.copy()
    cv.aruco.drawDetectedMarkers(output_img, markerCorners, markerIds)
    cv.imshow("Output", output_img)

    cv.imshow("frame", gray)
    if cv.waitKey(1) == ord("q"):
        break

input_video.release()
cv.destroyAllWindows()
