# importing libraries 
import cv2 
import numpy as np
from tkinter import *
from pytube import YouTube
import os
import RPi.GPIO as GPIO
import time
from ffpyplayer.player import *
import requests

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
phone.set("")

#GPIO pins
signal = 18


#Api
parameters = {'action':'viewsvideos','MCID':'002000311'}
response = requests.get("http://clickcash.in/videoApi/videoApi.php", params=parameters)

#---------------------------------methods-----------------------------------
def number_e():
    global number
    global count
    global cnt
    num = number.get()
    number.set(num)
    pushCnt = str(cnt)
    print(num)
    print(pushCnt)
    para = {'action': 'saveUserData', 'MOB': num, 'MCID': '002000311', 'BTNO': pushCnt}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r.text)
    num=""
    number.set(num)
    cnt = 0
    count.set(num)
    raise_frame(PageTwo)
    root.update()
    time.sleep(5)
    raise_frame(welcome)
    root.update()

def exit():
    global number
    global count
    global cnt
    pushCnt = str(cnt)
    print(pushCnt)
    para = {'action': 'saveUserData', 'MOB': '9999999999', 'MCID': '002000311', 'BTNO': pushCnt}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r.text)
    num=""
    number.set(num)
    cnt = 0
    count.set(num)
    raise_frame(PageTwo)
    root.update()
    time.sleep(5)
    raise_frame(welcome)
    root.update()


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
                    a = GPIO.input(signal)
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
                        root.after(30000, exit)
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

        #window.after(500, loop)
    
def lists():
    global c
    global collection
    global files
    num=0
    videoList = []
    videosApi = response.json()['schemes']
    for video in videosApi:
        link = video['video']
        videoList.append(link)
    files = os.listdir("/home/pi/Desktop/video")
    print(len(files))
    for x in videoList:
        num=num+1
    print(num)
    print(len(videos))
    if(len(files)-5)==num:
        print('No downloading...')
        c=num
    else:
        for item in videoList:
            if item in videos:
                print ('Already exists')
                videos.remove(item)
            else:
                videos.insert(0,item)
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

PageTwo = Frame(window)

for frame in (screen2, PageTwo):
    frame.grid(row=8, column=3, sticky='news')

# screen2.config(padx=20, pady=20)
# screen2.place(relwidth=1, relheight=1)

# screen2.columnconfigure(0,weight=1)
# screen2.columnconfigure(1,weight=1)
# screen2.columnconfigure(2,weight=1)
# screen2.rowconfigure(0,weight=1)
# screen2.rowconfigure(8,weight=1)

Label(screen2, text="Enter your Mobile Number to get Rewarded\n", font=myfont).grid(columnspan=3, row=0, column=0, padx=(185,1), pady=15)
Label(screen2, text="Bottle Count: ", font=myfont).grid(row=1, column = 0, padx=(250,1), pady=5, columnspan=2)
Label(screen2, textvariable=count, font=myfont).place(x=585, y=125) #grid(row=1, column=2, padx=(0,0), pady=5)
Label(screen2, text="\n", font=myfont).grid(row=1, column = 3, padx=(0,0), pady=0)
e = Entry(PageOne, textvariable=number, width=20, font=myfont)
e.grid(columnspan=3, row=2, column=0, padx=(200,1), pady=15)
Button(screen2, text='1', command=lambda:num_get(1), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=3, column=0, padx=(200,10), pady=(15,0))
Button(screen2, text='2', command=lambda:num_get(2), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=3, column=1, padx=(0,10), pady=(15,0))
Button(screen2, text='3', command=lambda:num_get(3), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=3, column=2, padx=(0,10), pady=(15,0))
Button(screen2, text='4', command=lambda:num_get(4), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=4, column=0, padx=(200,10), pady=(10,0))
Button(screen2, text='5', command=lambda:num_get(5), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=4, column=1, padx=(0,10), pady=(10,0))
Button(screen2, text='6', command=lambda:num_get(6), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=4, column=2, padx=(0,10), pady=(10,0))
Button(screen2, text='7', command=lambda:num_get(7), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=5, column=0, padx=(200,10), pady=(10,0))
Button(screen2, text='8', command=lambda:num_get(8), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=5, column=1, padx=(0,10), pady=(10,0))
Button(screen2, text='9', command=lambda:num_get(9), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=5, column=2, padx=(0,10), pady=(10,0))
Button(screen2, text='0', command=lambda:num_get(0), borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=6, column=1, padx=(0,10), pady=(10,0))
Button(screen2, text='Delete', command=delt, borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=6, column=2, padx=(0,10), pady=(10,0))
Button(screen2, text='Clear', command=clr, borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=6, column=0, padx=(200,10), pady=(10,0))
Button(screen2, text='Enter', bg='#0052cc', fg='#ffffff', command=number_e, borderwidth=5, relief=RAISED, height=1, width=22, font=nfont).grid(row=7, column=0, columnspan=2,padx=(200,10), pady=(10,0))
Button(screen2, text='Cancel', command=cancel, borderwidth=5, relief=RAISED, height=1, width=10, font=nfont).grid(row=7, column=2, padx=(0,10), pady=(10,0))

Label(PageTwo, text="Thank You\n\nfor your contribution\n\nin making our environment clean.\n\n\n\nBe Clean. Go Green.", font=myfont).grid(row=1, column=1, padx=250, pady=150)

setup()
#enterScreen1()
#window.after(500, loop)
loop()
window.mainloop()
