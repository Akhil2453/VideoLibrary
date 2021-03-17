# importing libraries 
import cv2 
import numpy as np
from tkinter import *
import pymongo
from pytube import YouTube
import os
import RPi.GPIO as GPIO
import time
from ffpyplayer.player import *

#----------------------------container window----------------------------
window = Tk()

#---------------------------------utils----------------------------------
videos=[]
files=[]
c = 0
a = True
cnt = 0
count = StringVar()
phone = StringVar()
width = window.winfo_screenwidth()-50
height = window.winfo_screenheight()-50
window.geometry(str(width)+"x"+str(height))
fontFamily="veranda"
bgPink="#fce4ec"
darkPink="#c2185b"
bgButton="#81d3f9"
phone.set("")

#GPIO pins
signal = 18

#Database
connection = pymongo.MongoClient('mongodb+srv://Dikshitha:Dikshitha29@cluster1.xya37.mongodb.net/CigaretteBud?retryWrites=true&w=majority')
db = connection['CigaretteBud']
collection = db['videoLinks']

#---------------------------------methods-----------------------------------
def enterNum(digit):
    phone.set(phone.get()+digit)
    entryPhone.icursor("end")

def delete():
    phone.set(phone.get()[:-1])

def clear():
    phone.set("")

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(signal, GPIO.IN) #, pull_up_down=GPIO.PUD_UP)

def endprogram():
    GPIO.cleanup()

def loop():
    window.update()
    window.withdraw()
    lists()
    global width
    global height
    global a
    global count
    global cnt
    global files
    a = GPIO.input(signal)
    for i in files:
        cap = cv2.VideoCapture(i)
        player = MediaPlayer(i)
        if (cap.isOpened()==False):
            print("Error opening video file")
        else:
            while(cap.isOpened()):
                ret, frame = cap.read()
                audio_frame, val = player.get_frame()
                
                if ret == True:
                    scale_width = width/frame.shape[1]
                    scale_height = height/frame.shape[0]
                    window_width = int(frame.shape[1]*scale_width)
                    window_height = int(frame.shape[0]*scale_height)
                    dim = (window_width, window_height)
                    cv2.resizeWindow('Frame',window_width, window_height)
                    cv2.imshow('Frame', cv2.resize(frame, dim, interpolation=cv2.INTER_AREA))
                    
                    if a == False:
                        a = True
                        cap.release()
                        cv2.destroyAllWindows()
                        window.update()
                        window.deiconify()
                        time.sleep(0.2)
                        print("Button Pressed")
                        cnt = cnt + 1
                        count.set(cnt)
                        print("Count: ", cnt)
                        audio_frame = None
                        val = None
                        enterScreen1()
                        return
                        
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        a = True
                        window.update()
                        window.deiconify()
                        cap.release()
                        cv2.destroyAllWindows()
                        time.sleep(0.2)
                        print("Button Pressed")
                        cnt = cnt + 1
                        count.set(cnt)
                        print("count", cnt)
                        audio_frame = None
                        val = None
                        enterScreen1()
                        return

                    if val != 'eof' and audio_frame is not None:
                        img, t = audio_frame
                        
                else:
                    break

            cap.release()
        cv2.destroyAllWindows()

        window.after(500, loop)
    
def lists():
    global c
    global collection
    global files
    num=0
    files = os.listdir("/home/pi/Desktop/video")
    print(len(files))
    for x in collection.find():
        num=num+1
    print(num)
    print(len(videos))
    if(len(files)-2)==num:
        print('No downloading...')
        c=num
    else:
        for item in collection.find():
            if item.get('link',"") in videos:
                print ('Already exists')
                videos.remove(item.get('link',''))
            else:
                videos.insert(0,item.get('link',""))
        print(videos)
        for link in videos:
            print (link)
            yt=YouTube(link)
            c=c+1
            print(c)
            videoStream=yt.streams.first()
            videoStream.download("/home/pi/Desktop/video","video"+str(c))
    
def enterScreen1():
    window.update()
    window.deiconify()
    #window.after(5000, loop)

#----------------------------Creating screens(Frames)-------------------------
screen2 = Frame(window)
screen2.config(padx=20, pady=20)
screen2.place(relwidth=1, relheight=1)

screen2.columnconfigure(0,weight=1)
screen2.columnconfigure(1,weight=1)
screen2.columnconfigure(2,weight=1)
screen2.rowconfigure(0,weight=1)
screen2.rowconfigure(8,weight=1)

Label(screen2,
      text="Phone Number : ",
      font=(fontFamily,14,"italic"),
      bg=bgPink).grid(row=1,column=0,sticky=NE,padx=5,pady=5)
entryPhone = Entry(screen2,
             textvariable=phone,
             font=(fontFamily,14,"normal"))
entryPhone.grid(row=1,column=1,columnspan=2,sticky=NW,padx=5,pady=5)
Button(screen2,
       text="1",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("1")).grid(row=2,column=0,sticky="nesw")
Button(screen2,
       text="2",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("2")).grid(row=2,column=1,sticky="nesw")
Button(screen2,
       text="3",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("3")).grid(row=2,column=2,sticky="nesw")
Button(screen2,
       text="4",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("4")).grid(row=3,column=0,sticky="nesw")
Button(screen2,
       text="5",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("5")).grid(row=3,column=1,sticky="nesw")
Button(screen2,
       text="6",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("6")).grid(row=3,column=2,sticky="nesw")
Button(screen2,
       text="7",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("7")).grid(row=4,column=0,sticky="nesw")
Button(screen2,
       text="8",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("8")).grid(row=4,column=1,sticky="nesw")
Button(screen2,
       text="9",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("9")).grid(row=4,column=2,sticky="nesw")
Button(screen2,
       text="Del",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=delete).grid(row=5,column=0,sticky="nesw")
Button(screen2,
       text="0",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=lambda: enterNum("0")).grid(row=5,column=1,sticky="nesw")
Button(screen2,
       text="Clear",
       font=(fontFamily,14,"italic"),
       bg=darkPink,
       command=clear).grid(row=5,column=2,sticky="nesw")
Button(screen2,
       text="Continue",
       font=(fontFamily,14,"normal"),
       justify=CENTER,
       fg="black",
       bg=bgButton,
       activeforeground="white",
       activebackground=bgButton,
       relief=RIDGE,
       command=loop).grid(row=7,column=0,columnspan=3,padx=20,pady=10)
lblError = Label(screen2,
                 text="*Enter A Valid Phone Number",
                 font=(fontFamily,14,"italic"),
                 fg="red",
                 bg=bgPink)
lblError.grid_forget()


setup()
#enterScreen1()
window.after(500, loop)
window.mainloop()
