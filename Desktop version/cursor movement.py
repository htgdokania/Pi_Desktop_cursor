import numpy as np
import cv2
import pyautogui

speed=5

#set your pointers HSV range
low=np.array([101,105,84])
high=np.array([120,255,255])

#initializing
prev_x=0
prev_y=0
prev_area=0
pyautogui.FAILSAFE = False

#Capture device
cap=cv2.VideoCapture(0)

while True:
    ret,image=cap.read()
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,low,high)
##    cv2.imshow('mask',mask)
    blur=cv2.GaussianBlur(mask,(15,15),0)
    _,contours,_=cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    for contour in contours:                       
        area=cv2.contourArea(contour)
        if area>1000:                            
            x,y,w,h = cv2.boundingRect(contour)
            d_x=x-prev_x
            d_y=y-prev_y
            if(abs(d_x)<10):
                d_x=0
            if(abs(d_y)<10):
                d_y=0
            prev_x=x
            prev_y=y
            if(area<=3000 and prev_area>=3000):
                print("leftclick")
##                pyautogui.click()
            else:    
                pyautogui.moveRel(speed*d_x,speed*d_y)
            prev_area=area                            
            cv2.drawContours(image,contour,-1,(255,0,0),3)
    cv2.imshow('frame',image) #display image

    if cv2.waitKey(25) & 0xFF==ord('q'):
        break
cv2.destroyAllWindows()
