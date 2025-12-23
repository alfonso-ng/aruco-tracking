import cv2 as cv

detector_params = cv.aruco.DetectorParameters()
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
detector = cv.aruco.ArucoDetector(dictionary, detector_params)

input_video = cv.VideoCapture(2)
if not input_video.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = input_video.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow("frame", gray)
    if cv.waitKey(1) == ord("q"):
        break

input_video.release()
cv.destroyAllWindows()
