import cv2
import numpy as np
import pyautogui
import time
import pickle

objects = []
with (open("range.pickle", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break



(sx,sy)=pyautogui.size()
(camx, camy) = (640, 480)

def nothing(x):
    pass
image = np.zeros((300,512,3), np.uint8)

#lower and upper bound for hsv range.
lowerBound = objects[0]['hsv_1']['lower_bound']
upperBound = objects[0]['hsv_1']['upper_bound']
cv2.namedWindow('HSV_Masked')

#cv2.createTrackbar('H','HSV_Masked',lowerBound[0][0][0],upperBound[0][0][0],nothing)
#cv2.createTrackbar('S','HSV_Masked',lowerBound[0][0][1],upperBound[0][0][1],nothing)
#cv2.createTrackbar('V','HSV_Masked',lowerBound[0][0][2],upperBound[0][0][2],nothing)

cv2.createTrackbar('H','HSV_Masked',0,179,nothing)
cv2.createTrackbar('S','HSV_Masked',0,255,nothing)
cv2.createTrackbar('V','HSV_Masked',0,255,nothing)

switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'HSV_Masked',0,1,nothing)



cam = cv2.VideoCapture(0)

kernelOpen = np.ones((5,5))
kernelClose = np.ones((5,5))
pinchFlag = 0


while True:
    ret, img = cam.read()
    img = cv2.resize(img, (camx,camy))
    img = cv2.flip(img,1)
    #cv2.namedWindow('HSV_masked')
    #cv2.setTrackbarPos()

    
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #cv2.imshow('image',image)
    
    #Apply mask for red color
    r=-1
    if(r==-1):
        
        mask = cv2.inRange(imgHSV,np.array(lowerBound),np.array(upperBound))
    else:
        mask = cv2.inRange(imgHSV,np.array([b-40,g-40,r-40]),np.array([b+40,g+40,r+40]))
   
        
    #print(b,g,r)
    
    #maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelClose,iterations = 3)
    maskFinal = maskClose
    
    cv2.imshow("HSV_Masked", maskFinal)
    
    r = cv2.getTrackbarPos('H','HSV_Masked')
    g = cv2.getTrackbarPos('S','HSV_Masked')
    b = cv2.getTrackbarPos('V','HSV_Masked')
    s = cv2.getTrackbarPos(switch,'HSV_Masked')
   
    print("ccc",b,g,r,s)
    
    
    (version, _, _) = cv2.__version__.split('.')

    if version == '3':
        image, contours, hierarchy = cv2.findContours(maskFinal.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    elif version == '2':
        contours, hierarchy = cv2.findContours(maskFinal.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)
        
    
    if(len(contours)==1):
        #one object mode
        cnt = contours[0]
        m = cv2.moments(cnt)
        if(m['m00']!=0):
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
        else:
            cx = 0
            cy = 0
        cv2.circle(img, (cx, cy), 10, (0, 0, 255), -1)
        cv2.imshow("img", img)
        print("In one object mode")
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(cx, cy) 
        
        
        
    elif(len(contours)==2):
        #two object mode
        cnt1 = contours[0]
        m = cv2.moments(cnt1)
        if(m['m00']!=0):
        
            cx1 = int(m['m10']/m['m00'])
            cy1 = int(m['m01']/m['m00'])
        else:
            cx1 = 0
            cy1 = 0
         
        cv2.circle(img, (cx1, cy1), 10, (0, 0, 255), -1)
        
        
        
        
        cnt2 = contours[1]
        m2 = cv2.moments(cnt2)
        if(m2['m00']!=0):
        
            cx2 = int(m2['m10']/m2['m00'])
            cy2 = int(m2['m01']/m2['m00'])
        else:
            cx2 = 0
            cy2 = 0
        cv2.circle(img, (cx2, cy2), 10, (0, 0, 255), -1)
        
        cv2.line(img, (cx1, cy1), (cx2, cy2), (0,0,255), 2)
        cv2.imshow("img", img)
        
        centerX = int((cx1+cx2)/2)
        centerY = int((cy1+cy2)/2)
        
        cv2.circle(img, (centerX, centerY), 3, (0, 0, 255), -1)
        
        xi = sx - (centerX*(sx/camx))
        yi = centerY*(sy/camy)
        
        if(cx2==centerX and cx1==centerY):
            pyautogui.click()
        #pyautogui.moveTo(xi, yi) 
        
        
        
        print("In two object mode")
#        time.sleep(1)
        
    elif(len(contours)==3):
        #three object mode
        cnt1 = contours[0]
        m = cv2.moments(cnt1)
        if(m['m00']!=0):
        
            cx1 = int(m['m10']/m['m00'])
            cy1 = int(m['m01']/m['m00'])
        else:
            cx1 = 0
            cx2 = 0
        cv2.circle(img, (cx1, cy1), 3, (0, 0, 255), -1)
        
        cnt2 = contours[1]
        m2 = cv2.moments(cnt2)
        if(m2['m00']!=0):
        
            cx2 = int(m2['m10']/m2['m00'])
            cy2 = int(m2['m01']/m2['m00'])
        else:
            cx2 = 0
            cy2 = 0
        cv2.circle(img, (cx2, cy2), 3, (0, 0, 255), -1)
          
        cnt3 = contours[2]
        m3 = cv2.moments(cnt3)
        
        if(m3['m00']!=0):
        
            cx3 = int(m3['m10']/m3['m00'])
            cy3 = int(m3['m01']/m3['m00'])
        else:
            cx3 = 0
            cy3 = 0
        cv2.circle(img, (cx3, cy3), 3, (0, 0, 255), -1) 
        cv2.imshow("img", img)
        print("In three object mode")
        
    else:
        print("Neither in one, two or three object mode!!")
    
    
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.imshow("img", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()
