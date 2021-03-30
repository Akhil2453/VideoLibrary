# importing libraries 
import cv2 
import numpy as np
from tkinter import *
import tkinter.font as tkFont
from pytube import YouTube
import os
import RPi.GPIO as GPIO
import time
from ffpyplayer.player import *
import requests
from datetime import datetime, timedelta
import threading
#----------------------------container window----------------------------
window = Tk()
window.title("Bottle Crusher")
window.geometry('1920x1040')
window.attributes('-fullscreen', True)
width = window.winfo_screenwidth() - 25
height = window.winfo_screenheight() - 25
#---------------------------------utils----------------------------------
videos=[]
files=[]
c = 0
a = True
cnt = 1
count = StringVar()
phone = StringVar()
phone.set("")
ret = False
dfont = tkFont.Font(size=-6)
myfont = tkFont.Font(size=32)
mfont = tkFont.Font(size=20)
nfont = tkFont.Font(size=20)
count.set(cnt)


#GPIO pins
signal = 18


def raise_frame(frame):
    frame.tkraise()

#Api
parameters = {'action':'viewsvideos','MCID':'002000312'}
response = requests.get("http://clickcash.in/videoApi/videoApi.php", params=parameters)

#---------------------------------methods-----------------------------------
def number_e():
    global phone
    global count
    global cnt
    global ret
    global timer
    timer.cancel()
    num = phone.get()
    phone.set(num)
    pushCnt = str(cnt)
    print(num)
    print(pushCnt)
    para = {'action': 'saveUserData', 'MOB': num, 'MCID': '002000312', 'BTNO': pushCnt}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r)
    num=""
    phone.set(num)
    cnt = 1
    count.set(cnt)
    screen2.grid_forget()
    PageTwo.grid(row=8, column=3, sticky='news')
    window.update()
    time.sleep(5)
    PageTwo.grid_forget()
    loop()
    window.update()

def exita():
    global phone
    global count
    global cnt
    global a
    global timer
    a = True
    timer.cancel()
    pushCnt = str(cnt)
    print(pushCnt)
    para = {'action': 'saveUserData', 'MOB': '9999999999', 'MCID': '002000312', 'BTNO': pushCnt}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r)
    num=""
    phone.set(num)
    cnt = 1
    count.set(cnt)
    screen2.grid_forget()
    PageTwo.grid(row=8, column=3, sticky='news')
    window.update()
    time.sleep(5)
    PageTwo.grid_forget()
    loop()
    window.update()

timer=threading.Timer(30, exita)

def enterNum(digit):
    phone.set(phone.get()+str(digit))
    e.icursor("end")

def delete():
    phone.set(phone.get()[:-1])

def clear():
    phone.set("")

def cancel():
    global cnt
    global count
    #exita()
    cnt = 1
    count.set(cnt)
    e.delete(0, END)
    loop()   

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(signal, GPIO.IN) #, pull_up_down=GPIO.PUD_UP)

def endprogram():
    GPIO.cleanup()

def loop():
    window.update()
    window.withdraw()
    global width
    global height
    global a
    global count
    global cnt
    global timer
    a = True
    files = os.listdir("/home/pi/Desktop/videoLibrary/video")
    for i in files:
        b = '/home/pi/Desktop/videoLibrary/video/' + i
        cap = cv2.VideoCapture(b)
        player = MediaPlayer(b)
        if (cap.isOpened()==False):
            print("Error opening video file")
        else:
            while(cap.isOpened()):
                a = GPIO.input(signal)
                ret, frame = cap.read()
                audio_frame, val = player.get_frame()
                cv2.namedWindow ('Frame', cv2.WINDOW_NORMAL)
                cv2.setWindowProperty ('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                #print(b)
                #frame1 = cv2.resize(frame, (1920, 1040), interpolation=cv2.INTER_AREA)
                if ret == True:
                    a = GPIO.input(signal)
                    scale_width = width/frame.shape[1]
                    scale_height = height/frame.shape[0]
                    window_width = int(frame.shape[1]*scale_width)
                    window_height = int(frame.shape[0]*scale_height)
                    dim = (window_width, window_height)
                    cv2.imshow ('Frame', cv2.resize(frame, dim, interpolation=cv2.INTER_AREA))
                    timer=threading.Timer(30, exita)
                    main=threading.main_thread()

                    while(a == False) :
                        time.sleep(0.7)
                        player = None
                        cap.release()
                        cv2.destroyAllWindows()
                        audio_frame = None
                        val = None
                        window.update()
                        window.deiconify()
                        screen2.grid(row=8, column=3, sticky='news')
                        a = GPIO.input(signal)
                        if a==False:
                            if(timer.is_alive()):
                                #timer._stop()
                                print("Button Pressed")
                                cnt = cnt + 1
                                count.set(cnt)
                                print("Count: ", cnt)
                                print("inside timer.stop")
                                continue
                            else:
                                print("inside else")
                                #continue
                                print("Button Pressed")
                                cnt = cnt + 1
                                count.set(cnt)
                                print("Count: ", cnt)
                                timer.start()
                                print("after the thread has started")
                                a = True
                        else:
                            time.sleep(0.3)
                        a=False
                        
                    if cv2.waitKey(1) & 0xFF == ord('q'):
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
    videoList = []
    videosApi = response.json()['schemes']
    for video in videosApi:
        link = video['video']
        videoList.append(link)
    files = os.listdir("/home/pi/Desktop/videoLibrary/video")
    print(len(files))
    for x in videoList:
        num=num+1
    print(num)
    print(len(videos))
    if(len(files))==num:
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
            videoStream.download("/home/pi/Desktop/videoLibrary/video","video"+str(c))

#----------------------------Creating screens(Frames)-------------------------


screen2 = Frame(window)

PageTwo = Frame(window)

Label(screen2, text="Enter your Mobile Number to get Rewarded\n", font=myfont).grid(columnspan=3, row=0, column=0, padx=(425,1), pady=(75,15))
Label(screen2, text="Bottle Count: ", font=myfont).grid(row=1, column = 0, padx=(500,1), pady=5, columnspan=2)
Label(screen2, textvariable=count, font=myfont).place(x=1015, y=215) #grid(row=1, column=2, padx=(0,0), pady=5)
Label(screen2, text="\n", font=myfont).grid(row=1, column = 3, padx=(0,0), pady=0)
e = Entry(screen2, textvariable=phone, width=30, font=myfont)
e.grid(columnspan=3, row=2, column=0, padx=(375,1), pady=45)
Button(screen2, text='1', command=lambda:enterNum(1), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=3, column=0, padx=(350,10), pady=(15,0))
Button(screen2, text='2', command=lambda:enterNum(2), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=3, column=1, padx=(0,10), pady=(15,0))
Button(screen2, text='3', command=lambda:enterNum(3), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=3, column=2, padx=(0,10), pady=(15,0))
Button(screen2, text='4', command=lambda:enterNum(4), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=4, column=0, padx=(350,10), pady=(10,0))
Button(screen2, text='5', command=lambda:enterNum(5), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=4, column=1, padx=(0,10), pady=(10,0))
Button(screen2, text='6', command=lambda:enterNum(6), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=4, column=2, padx=(0,10), pady=(10,0))
Button(screen2, text='7', command=lambda:enterNum(7), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=5, column=0, padx=(350,10), pady=(10,0))
Button(screen2, text='8', command=lambda:enterNum(8), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=5, column=1, padx=(0,10), pady=(10,0))
Button(screen2, text='9', command=lambda:enterNum(9), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=5, column=2, padx=(0,10), pady=(10,0))
Button(screen2, text='0', command=lambda:enterNum(0), borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=6, column=1, padx=(0,10), pady=(10,0))
Button(screen2, text='Delete', command=delete, borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=6, column=2, padx=(0,10), pady=(10,0))
Button(screen2, text='Clear', command=clear, borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=6, column=0, padx=(350,10), pady=(10,0))
Button(screen2, text='Enter', bg='#0052cc', fg='#ffffff', command=number_e, borderwidth=5, relief=RAISED, height=2, width=44, font=nfont).grid(row=7, column=0, columnspan=2,padx=(350,10), pady=(10,0))
Button(screen2, text='Cancel', command=cancel, borderwidth=5, relief=RAISED, height=2, width=20, font=nfont).grid(row=7, column=2, padx=(0,10), pady=(10,0))

Label(PageTwo, text="Thank You\n\nfor your contribution\n\nin making our environment clean.\n\n\n\nBe Clean. Go Green.", font=myfont).grid(row=1, column=1, padx=650, pady=300)



lists()
setup()
window.after(500, loop)

#toggle_fullscreen()
window.mainloop()
