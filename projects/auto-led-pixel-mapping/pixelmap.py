from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import cv2
import imutils

import serial
import time

BLUE = [0, 0, 255]
BLACK = [0, 0, 0]


def draw_calibration_pixel(led_number, retries=3):
    with serial.Serial("COM3", baudrate=2152000, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE) as ser:
        for _ in range(retries):
            ser.write(bytearray(BLACK * led_number + BLUE + BLACK * (299 - led_number)))
            time.sleep(.3)


LED_NUM = 300
output = Path.cwd() / "led_pos.4.csv"


def locate_led_coord(cap, frames=80):
    accum_frame = None
    for _ in range(frames):
        # Capture frame-by-frame
        _, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([110, 40, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        res = cv2.cvtColor(res, cv2.COLOR_HSV2RGB)
        res = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)

        ret, res = cv2.threshold(res, 60, 255, cv2.THRESH_BINARY)
        # cv2.imshow("res", res)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     pass
        if accum_frame is None:
            accum_frame = res
        else:
            accum_frame += res

    blurred = cv2.GaussianBlur(accum_frame, (29, 29), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("res", thresh)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     pass
    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)




if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    with output.open("w") as f:
        for led_index in range(LED_NUM):
            draw_calibration_pixel(led_index)
            x, y = locate_led_coord(cap)
            f.write("{},{},{}\n".format(led_index, x, y))
            print(led_index, x, y)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
