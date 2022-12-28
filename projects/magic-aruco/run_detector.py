from functools import partial
from pathlib import Path
from typing import NamedTuple

import cv2
import cv2.aruco as aruco
import numpy as np


dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
detect_markers = partial(
    aruco.detectMarkers, dictionary=dictionary, parameters=parameters
)


def generate_aruco_markers(size=300):
    """Generates the whole dictionary of ArUco tags"""
    output_directory = Path.cwd() / "markers"

    if not output_directory.exists():
        output_directory.mkdir()

    for id in range(0, 50):

        tag = np.zeros((size, size, 1), dtype="uint8")
        marker = aruco.drawMarker(dictionary, id, size, tag, 1)

        filepath = output_directory / f"{id}.png"
        cv2.imwrite(str(filepath), marker)


class Face(NamedTuple):
    id: int
    corner: int


def register_aruco_cube() -> None:
    data = {}
    face = 0

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bboxs, ids, _ = detect_markers(img)

        print(aruco.estimatePoseSingleMarkers(bboxs, 0.03))

        if ids is not None and len(ids) > 0:
            id, *_ = ids[0].tolist()

            if id not in data:
                data[id] = face
                face += 1

        aruco.drawDetectedMarkers(img, bboxs)
        img = cv2.flip(img, 1)
        cv2.imshow("Cube Registration", img)
        k = cv2.waitKey(30) & 0xFF

        if k == 27:
            break

        if len(data.keys()) == 6:
            break

    cap.release()
    cv2.destroyAllWindows()

    print(data)


def run_event_loop() -> None:
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bboxs, ids, _ = detect_markers(img)
        aruco.drawDetectedMarkers(img, bboxs)
        img = cv2.flip(img, 1)
        cv2.imshow("Magic Pen", img)
        k = cv2.waitKey(30) & 0xFF

        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    register_aruco_cube()
