import numpy as np
import cv2
from ffpyplayer.player import *
from tkinter import *

window = Tk()

width = window.winfo_screenwidth() - 25
height = window.winfo_screenheight() - 25

cap = cv2.VideoCapture('video1.mp4')
player = MediaPlayer('video1.mp4')
print(cap.isOpened())
while(True):
    ret, frame = cap.read()
    # cv2.imshow('frame')
    #print(ret)
    audio_frame, val = player.get_frame()
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
