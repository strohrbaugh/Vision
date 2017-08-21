#Updates 8/20/2017 8:30pm

import sys
import os
import pygame
import pygame.camera
from pygame.locals import *
import cv2
import numpy as np
import time
import picamera
import picamera.array
from imutils.video import VideoStream
import imutils

screen_width = 640
screen_height = 330

x_therm_offset=80
y_therm_offset=220
thermal_width = 165

camera = picamera.PiCamera()
camera.resolution = (screen_width, screen_height)

pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode([screen_width, screen_height],pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

video = picamera.array.PiRGBArray(camera)
#find, open and start low-res camera
cam_list = pygame.camera.list_cameras()
#webcam = VideoStream(src=0).start()
#webcam = pygame.camera.Camera(cam_list[0],(32,24))
#webcam.start()

#os.system('sudo python thermalimg2file.py')

try:
    for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):
	frame = np.rot90(frameBuf.array,3)
	frame = np.fliplr(frame)
        video.truncate(0)

        f = open('/dev/shm/pineal/thermal_image_status.txt', 'r')
        status = f.read()
        if status == 'new':
            print "new image"
            thermal = cv2.imread('/dev/shm/pineal/thermal.bmp')
	    thermal = np.rot90(thermal,3)
	    thermal = np.fliplr(thermal)
	    thermal = imutils.resize(thermal,width = thermal_width)
	else:
	    thermal = thermal	    
#        thermal = pygame.transform.scale(thermal,(80,60))
        
#Trying to do edge detection here
        
#	visiblur = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	visiblur = frame[y_therm_offset:y_therm_offset+thermal.shape[0], x_therm_offset:x_therm_offset+thermal.shape[1],0]
#	visiblur = cv2.GaussianBlur(visiblur, (9, 9), 0)
	sigma = 0.33
	v = np.median(visiblur)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edgeimg = cv2.Canny(visiblur, lower, upper)
	thermal[edgeimg != 0] = [0,255,0]
#	edgeimg = visiblur

#done trying to do edge detection

#merging thermal & visible

	frame = np.array(frame).copy()
	frame[y_therm_offset:y_therm_offset+thermal.shape[0], x_therm_offset:x_therm_offset+thermal.shape[1],:] = thermal
	#thermal = cv2.copyMakeBorder(thermal, 135, 135, 280, 280, cv2.BORDER_CONSTANT)
	#frame[edgeimg != 0] = [0,255,0]

#done merging thermal & visible

        display = pygame.surfarray.make_surface(frame)
        screen.blit(display, (0,0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                    raise KeyboardInterrupt
except KeyboardInterrupt,SystemExit:
    pygame.quit()
    cv2.destroyAllWindows()


