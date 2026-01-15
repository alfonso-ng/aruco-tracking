import json
import socket

import cv2 as cv
import numpy as np
from scipy.spatial.transform import Rotation as R

cv_to_unity = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])

detector_params = cv.aruco.DetectorParameters()
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
detector = cv.aruco.ArucoDetector(dictionary, detector_params)

aruco_marker_side_length = 0.2
mtx = np.array([[752, 0, 305], [0, 756, 242], [0, 0, 1]])

dst = np.array([-0.23, 3.785, 0.001, 0.002, -20.937])

transform = {
    "position": {"x": 0, "y": 0, "z": 0},
    "rotation": {"x": 0, "y": 0, "z": 0, "w": 0},
}

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

    detector_params = cv.aruco.DetectorParameters()
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
    detector = cv.aruco.ArucoDetector(dictionary, detector_params)

    (markerCorners, markerIds, rejectedCandidates) = detector.detectMarkers(gray)

    output_img = gray.copy()
    # Set up coordinate system
    obj_points = np.array(
        [
            [-aruco_marker_side_length / 2, aruco_marker_side_length / 2, 0],
            [aruco_marker_side_length / 2, aruco_marker_side_length / 2, 0],
            [aruco_marker_side_length / 2, -aruco_marker_side_length / 2, 0],
            [-aruco_marker_side_length / 2, -aruco_marker_side_length / 2, 0],
        ],
        dtype=np.float32,
    )

    rvecs = []
    tvecs = []
    nMarkers = len(markerCorners)

    if markerIds is not None:
        cv.aruco.drawDetectedMarkers(output_img, markerCorners, markerIds)

        # SolvePnP
        for i in range(nMarkers):
            ret, rvec, tvec = cv.solvePnP(obj_points, markerCorners[i], mtx, dst)
            rvecs.append(rvec)
            tvecs.append(tvec)

            # DrawAxis
            cv.drawFrameAxes(
                output_img,
                mtx,
                dst,
                rvecs[i],
                tvecs[i],
                aruco_marker_side_length / 3,
                2,
            )

            T_unity = cv_to_unity @ tvec

            r, _ = cv.Rodrigues(rvec)
            R_unity = cv_to_unity @ r @ cv_to_unity
            q = R.from_matrix(R_unity).as_quat()

            transform["position"]["x"] = T_unity[0][0]
            transform["position"]["y"] = T_unity[1][0]
            transform["position"]["z"] = T_unity[2][0]

            transform["rotation"]["x"] = q[0]
            transform["rotation"]["y"] = q[1]
            transform["rotation"]["z"] = q[2]
            transform["rotation"]["w"] = q[3]

            message = json.dumps(transform).encode("utf-8")
            sock.sendto(message, (UDP_IP, UDP_PORT))

    cv.imshow("Output", output_img)
    cv.imshow("frame", gray)
    if cv.waitKey(1) == ord("q"):
        break

input_video.release()
cv.destroyAllWindows()
