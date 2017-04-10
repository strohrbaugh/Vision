# import the necessary packages
from __future__ import print_function
#from pyimagesearch.basicmotiondetector import BasicMotionDetector
from imutils.video import VideoStream
import numpy as np
import datetime
import imutils
import pygame
import time
import cv2

# initialize the video streams and allow them to warmup
print("[INFO] starting cameras...")
webcam = VideoStream(src=0).start()
picam = VideoStream(usePiCamera=True).start()
time.sleep(1.0)

#pygame.init()
#pygame.display.set_mode((640,480), pygame.FULLSCREEN)
#pygame.mouse.set_visible( False )

# initialize the two motion detectors, along with the total
# number of frames read
#camMotion = BasicMotionDetector()
#piMotion = BasicMotionDetector()
total = 0

# loop over frames from the video streams
while True:
	# initialize the list of frames that have been processed
	frames = []
	visibleFrames = []

	visible = picam.read()
	visible = imutils.resize(visible, width = 320)
	visible = cv2.cvtColor(visible, cv2.COLOR_BGR2GRAY)
	visible = cv2.GaussianBlur(visible, (21, 21), 0)
	visibleEdge = cv2.Canny(visible, 300, 400, apertureSize = 5)
#	cv2.imshow("visible", visibleEdge)

	thermal = webcam.read()
#	thermal = imutils.resize(thermal, width = 320)
	thermal = imutils.resize(thermal, width = 160)
	thermal = cv2.copyMakeBorder(thermal, 60, 60, 80, 80,cv2.BORDER_CONSTANT)

	thermal = np.uint8(thermal/2.)
#	visible[60:180, 80:240,:]=thermal
	thermal[visibleEdge != 0] = (0, 255, 0)

	cv2.imshow("composite image", thermal)

	# loop over the frames and their respective motion detectors

	# increment the total number of frames read and grab the 
	# current timestamp
	total += 1
	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")

	# loop over the frames a second time
	for (frame, name) in zip(frames, ("Webcam", "Picamera")):
		# draw the timestamp on the frame and display it
		cv2.putText(frame, ts, (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		cv2.imshow(name, frame)

	# check to see if a key was pressed
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
webcam.stop()
picam.stop()
