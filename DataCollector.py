import pygame
import csv
import cv2
import time
import numpy as np
import mss
import os
import pandas as pd
from PIL import Image


# Writes a new line to the csv with given inputs
def add_line(img, joystick_x):
    with open('Lane_Data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([img, joystick_x])


np.set_printoptions(threshold=306001)
# This defines the area on the screen.
monitor = {"top": 203, "left": 496, "width": 1008, "height": 595, "mon": 1}
# Used to calculate FPS
previous_time = 0
# Set up the Xbox Controller input
pygame.init()
pygame.joystick.Joystick(0).init()
# Arrays to store frames and controller inputs before adding them to csv
frames = []
joystickInputs = []
while True:
    # Takes screenshot
    frame = mss.mss().grab(monitor)
    # Converts the frame into something that can be read by opencv
    frame = np.array(frame)
    frame = cv2.resize(frame, (720, 425))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display frame
    cv2.imshow('frame', frame)
    # FPS
    print("fps: {}".format(1 / (time.time() - previous_time)) + " - " + str(len(frames)))
    previous_time = time.time()
    # Store frame and controller input to array
    frames.append(frame)
    pygame.event.pump()
    joystickInputs.append(pygame.joystick.Joystick(0).get_axis(0))
    # Quits showing the frames when q is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

# Code to ask user which frames to save to the csv
startIndex = None
endIndex = None
while True:
    print("Enter start Index")
    line = input()
    if line.startswith("show"):
        showIndex = int(line.split(" ")[1])
        cv2.imshow("frame", frames[showIndex])
        if cv2.waitKey(0) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
    else:
        startIndex = int(line)
        break
while True:
    print("Enter end Index")
    line = input()
    if line.startswith("show"):
        showIndex = int(line.split(" ")[1])
        cv2.imshow("frame", frames[showIndex])
        if cv2.waitKey(0) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
    else:
        endIndex = int(line)
        break


# Trim arrays based on user input
frames = frames[startIndex:endIndex + 1]
joystickInputs = joystickInputs[startIndex:endIndex + 1]


# The urls of the images created below
img_urls = []
# Creates an image file and saves it to below directory
directory = "images/" + time.strftime('%m-%d-%Y-%H:%M:%S')
os.mkdir(directory)
for frame in frames:
    url = directory + "/" + str(time.time()) + ".jpg"
    cv2.imwrite(url, frame)
    img_urls.append(url)

# Format csv file
data_dict = {
    "img_url": img_urls,
    "JoystickX": joystickInputs
}

# Save the dictionary to csv
df = pd.DataFrame(data_dict)
df.to_csv("Lane_Data.csv", index=False,  header=False, mode='a')

print("Done")
