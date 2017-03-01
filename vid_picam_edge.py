### Imports ###################################################################

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
import numpy as np

### Setup #####################################################################

# Center coordinates
px = 480
py = 320

# Setup the camera
camera = PiCamera()
camera.resolution = (px, py )
camera.framerate = 60
rawCapture = PiRGBArray( camera, size=( px, py ) )

# Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier( '/home/pi/opencv-2.4.9/data/lbpcascades/lbpcascade_frontalface.xml' ) 

t_start = time.time()
fps = 0


### Main ######################################################################

# Capture frames from the camera
for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):
    
    image = frame.array
    #resized_image = cv2.resize(image, (2*px, 2*py))

    # Show the frame
    cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)          
    cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #thrs1 = cv2.getTrackbarPos('thrs1', 'edge')
    #thrs2 = cv2.getTrackbarPos('thrs2', 'edge')
    edge = cv2.Canny(gray, 3000, 4000, apertureSize=5)
    vis = image.copy()
    vis = np.uint8(vis/2.)
    vis[edge != 0] = (0, 255, 0)
    cv2.imshow("Frame", vis)
    key = cv2.waitKey( 1 ) & 0xFF

    # Clear the stream in preparation for the next frame
    rawCapture.truncate( 0 )

    if key == ord("q"):
	break

