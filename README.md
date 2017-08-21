# Vision
Vision Projects

At the moment, this is a clone of my working directory for Pineal Eye. "pineal1.py" and "thermalimg2file.py" are the current works in progress:

thermalimg2file.py captures an frame from a thermal webcam and stores the image in /dev/shm/pineal/thermal.bmp, and sets a flag value in thermal_image_status.txt to "new".

pineal1.py displays the feed from an attached rpicam; overlays the scaled & centered thermal feed on the visible feed; overlays the detected edges of the covered visible feed on the thermal feed.

both thermalimg2file.py and pineal1.py must be running to access live video from both cameras. pineal1.py must be running to access live video from any camera.

Next steps: add serial transmission to thermalimg2file.py in order to transfer thermal camera image data from one stereo channel to the other, and create a corresponding version able to receive thermal camera image data and store in /dev/shm/pineal/thermal.bmp for use by the other stereo channel.
