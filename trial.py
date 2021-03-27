import numpy as np
import cv2
from ffpyplayer.player import *
from tkinter import *
import os

window = Tk()

width = window.winfo_screenwidth() - 25
height = window.winfo_screenheight() - 25

files = os.listdir('/home/pi/Desktop/videoLibrary/video/')


for i in files:
    print(i)
    print(type(i))
    b = '/home/pi/Desktop/videoLibrary/video/' + i
    cap = cv2.VideoCapture(b)
    print(cap.isOpened())
    player = MediaPlayer(b)
    if (cap.isOpened()==False):
        print("Error opening video file")
    else:
        while(cap.isOpened()):
            ret, frame = cap.read()
            audio_frame, val = player.get_frame()
                
            if ret == True:
                #a = GPIO.input(signal)
                scale_width = width/frame.shape[1]
                scale_height = height/frame.shape[0]
                window_width = int(frame.shape[1]*scale_width)
                window_height = int(frame.shape[0]*scale_height)
                dim = (window_width, window_height)
                cv2.resizeWindow('Frame',window_width, window_height)
                cv2.imshow('Frame', cv2.resize(frame, dim, interpolation=cv2.INTER_AREA))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# cap = cv2.VideoCapture('video1.mp4')
# player = MediaPlayer('video1.mp4')

# while(True):
# 	ret, frame = cap.read()
# 	# cv2.imshow('frame')
# 	audio_frame, val = player.get_frame()
# 	scale_width = width/frame.shape[1]
#     scale_height = height/frame.shape[0]
#     window_width = int(frame.shape[1]*scale_width)
#     window_height = int(frame.shape[0]*scale_height)
#     dim = (window_width, window_height)
#     cv2.resizeWindow('Frame',window_width, window_height)
#     cv2.imshow('Frame', cv2.resize(frame, dim, interpolation=cv2.INTER_AREA))
