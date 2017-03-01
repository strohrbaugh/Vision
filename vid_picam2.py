###############################################################################
#                                                                             #
# file:    1_single_core.py                                                   #
#                                                                             #
# authors: Andre Heil  - avh34                                                #
#          Jingyao Ren - jr386                                                #
#                                                                             #
# date:    December 1st 2015                                                  #
#                                                                             #
# brief:   This is the simple face-tracking program. It uses a single core to #
#          process the images taken by the Pi Camera and processes them using #
#          OpenCV. It then uses ServoBlaster to move the servos so that your  #
#          face is centered.                                                  #
#                                                                             #
###############################################################################


### Imports ###################################################################

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os


### Setup #####################################################################

# Center coordinates
cx = 160
cy = 120

os.system( "echo 0=150 > /dev/servoblaster" )
os.system( "echo 1=150 > /dev/servoblaster" )

xdeg = 150
ydeg = 150

# Setup the camera
camera = PiCamera()
camera.resolution = ( 320, 240 )
camera.framerate = 60
rawCapture = PiRGBArray( camera, size=( 320, 240 ) )

# Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier( '/home/pi/opencv-2.4.9/data/lbpcascades/lbpcascade_frontalface.xml' ) 

t_start = time.time()
fps = 0


### Main ######################################################################

# Capture frames from the camera
for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):
    
    image = frame.array
    resized_image = cv2.resize(image, (1280, 960))

    # Show the frame
    cv2.imshow( "Frame", resized_image )
    key = cv2.waitKey( 1 ) & 0xFF

    # Clear the stream in preparation for the next frame
    rawCapture.truncate( 0 )

    if key == ord("q"):
	break
