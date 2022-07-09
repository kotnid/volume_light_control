import cv2
import time 
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math 
import screen_brightness_control as sbc

from ctypes import cast , POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam , hCam = 1920 , 1080

cap = cv2.VideoCapture(0)
cap.set(3 , wCam)
cap.set(4 , hCam)
pTime = 0 
pTime_2 = 0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_ , CLSCTX_ALL , None)
volume = cast(interface , POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

detector = HandDetector( detectionCon=0.8 , minTrackCon=0.6,  maxHands=2)

print("=== starting the device pls wait ===")

while True:
    ret , img = cap.read()
    hands , img = detector.findHands(img)

    for hand in hands:
        
        handType = hand["type"]
        lmList = hand["lmList"]

        if len(lmList) > 5:
            x1 , y1 = lmList[4][0] ,lmList[4][1]
            x2 , y2 = lmList[8][0] ,lmList[8][1]

            cv2.circle(img , (x1 , y1) , 15 , (255,0,255) , cv2.FILLED)
            cv2.circle(img , (x2 , y2) , 15 , (255,0,255) , cv2.FILLED)
            cv2.line(img , (x1,y1) , (x2,y2) , (255,0,255) , 3) 

            length = math.hypot(x2-x1 , y2-y1)

            if handType == "Left":
                cTime = time.time()
        

                Time_diff = cTime - pTime

                if Time_diff > 0.1:

                    volume.SetMasterVolumeLevel(0,None)
                    minVol = volRange[0]
                    maxVol = volRange[1]

                    vol = np.interp(length , [50 , 300] , [minVol , maxVol])
                    volume.SetMasterVolumeLevel(vol , None)       

                    print(f"volume now : {vol}") 

                    pTime = cTime

            elif handType == "Right":
                    cTime_2 = time.time()
        

                    Time_diff = cTime_2 - pTime_2

                    if Time_diff > 0.1:

                        Bright = np.interp(length , [50 , 300] , [0 , 100])
                        sbc.set_brightness(Bright)     

                        print(f"bright now : {Bright}") 

                        pTime_2 = cTime_2


    

    cv2.imshow("Img" , img)
    
    cv2.waitKey(1)