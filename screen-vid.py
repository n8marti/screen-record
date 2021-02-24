#!/usr/bin/env python3
"""
Ref:
- https://pythonprogramming.org/screen-recording-using-python/
- https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
"""

import cv2 # OpenCV
import pyautogui
import numpy as np

from pathlib import Path

# Get full screen resolution.
screen_w, screen_h = pyautogui.size()

# Initialize the list of window reference points.
corners = []

def select_region(event, x, y, flags, param):
	# Reference the global variable.
    global corners

	# If the left mouse button was clicked, record the starting (x, y)
    #   coordinates and indicate that cropping is being performed.
    if event == cv2.EVENT_LBUTTONDOWN:
        corners = [(x, y)]

        # Draw a rectangle around the region of interest.
        #cv2.rectangle(image, corners[0], pyautogui.position(), (0, 255, 0), 8)
        #cv2.imshow("image", image)

    elif event == cv2.EVENT_LBUTTONUP:
        # Record the ending (x, y) coordinates.
        corners.append((x, y))

        # Draw a rectangle around the region of interest.
        cv2.rectangle(image, corners[0], corners[1], (0, 255, 0), 8)
        cv2.imshow("image", image)

def translate_corners(corners):
    """
    corners = (x0, y0), (x1, y1)
    f_left = x0
    f_top = y0
    width = x1 - x0
    height = y1 - y0
    """
    f_left = corners[0][0]
    f_top = corners[0][1]
    width = corners[1][0] - corners[0][0]
    height = corners[1][1] - corners[0][1]
    return f_left, f_top, width, height


# Load the image, clone it, and setup the mouse callback function.
image = pyautogui.screenshot()
image = np.array(image) # converting the image into numpy array representation
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # converting the BGR image into RGB image
clone = image.copy()
#cv2.namedWindow("image", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("image", 400, 225)
cv2.namedWindow("image")
cv2.setMouseCallback("image", select_region)

# Choose mp4 codec for outfile.
codec = cv2.VideoWriter_fourcc(*'mp4v')

# Show initial window looping until the 'q' key is pressed.
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # If the 'r' key is pressed, reset the cropping region.
    if key == ord("r"):
    	image = clone.copy()

    # If the 'q' key is pressed, break from the loop.
    if key == ord("q"):
        break

    # Select entire desktop if "a" or "d" is pressed.
    if key == ord("a") or key == ord("d"):
        corners = [(0,0),(screen_w, screen_h)]

    if len(corners) == 2:
        break

if len(corners) == 2:
    # Get window values.
    f_left, f_top, width, height = translate_corners(corners)

    # Resolution set by 'width' and 'height'.
    outdir = Path.home()
    outfile_name = "Recorded.mp4"
    outfile = outdir / outfile_name
    out = cv2.VideoWriter(str(outfile), codec , 20, (int(width), int(height)))

    while True:
        img = pyautogui.screenshot(region=(f_left, f_top, width, height))
        # Convert the image into numpy array representation.
        frame = np.array(img)
        # Convert the BGR image into RGB image.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Write the RBG image to the outfile.
        out.write(frame)
        # Display screen/frame being recorded.
        cv2.imshow('Recording', frame)
        # Enable the user to press 'q' key to stop the recording.
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.waitKey(0)
    out.release()

# Destroy the recording window.
cv2.destroyAllWindows()
