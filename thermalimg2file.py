import sys
import pygame
import pygame.camera
import cv2
from imutils.video import VideoStream
import imutils
import os

imageSwapFolder = "/dev/shm/pineal"
newImageFlagFile = "/dev/shm/pineal/thermal_image_status.txt"

if not os.path.exists(imageSwapFolder):
    os.makedirs(imageSwapFolder)
if not os.path.exists(newImageFlagFile):
    os.system("sudo touch /dev/shm/pineal/thermal_image_status.txt")
    os.chown('/dev/shm/pineal/thermal_image_status.txt', 0, 0)

pygame.init()
pygame.camera.init()

#find, open and start low-res camera
cam_list = pygame.camera.list_cameras()
webcam = pygame.camera.Camera(cam_list[0],(32,24))
webcam.start()


while True:
	    #grab image, scale and blit to screen
    img = webcam.get_image()
    pygame.image.save(img, '/dev/shm/pineal/thermal.bmp')
    f = open(newImageFlagFile, 'w+')
    f.write('new')
    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
	        webcam.stop()
        	pygame.quit()
        	sys.exit()
