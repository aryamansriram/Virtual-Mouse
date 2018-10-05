import cv2
import numpy as np
import pyautogui
import time

(sx,sy)=pyautogui.size()
(camx, camy) = (640, 480)

#lower and upper bound for hsv range.
lowerBound = np.array([150,100,100])
upperBound = np.array([179,255,255])


cam = cv2.VideoCapture(0)

kernelOpen = np.ones((5,5))
kernelClose = np.ones((20,20))
pinchFlag = 0

while True:
    ret, img = cam.read()
    img = cv2.resize(img, (camx,camy))
    img = cv2.flip(img,1)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    
    #Apply mask for red color
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    maskFinal = maskClose
#    cv2.imshow("HSV_Masked", maskFinal)
    
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
        cx = int(m['m10']/m['m00'])
        cy = int(m['m01']/m['m00'])
        cv2.circle(img, (cx, cy), 10, (0, 0, 255), -1)
        cv2.imshow("img", img)
        print("In one object mode")
        
        
    elif(len(contours)==2):
        #two object mode
        cnt1 = contours[0]
        m = cv2.moments(cnt1)
        cx1 = int(m['m10']/m['m00'])
        cy1 = int(m['m01']/m['m00'])
        cv2.circle(img, (cx1, cy1), 10, (0, 0, 255), -1)
        
        
        
        
        cnt2 = contours[1]
        m2 = cv2.moments(cnt2)
        cx2 = int(m2['m10']/m2['m00'])
        cy2 = int(m2['m01']/m2['m00'])
        cv2.circle(img, (cx2, cy2), 10, (0, 0, 255), -1)
        
        cv2.line(img, (cx1, cy1), (cx2, cy2), (0,0,255), 2)
        cv2.imshow("img", img)
        
        centerX = int((cx1+cx2)/2)
        centerY = int((cy1+cy2)/2)
        
        cv2.circle(img, (centerX, centerY), 3, (0, 0, 255), -1)
        
        xi = sx - (centerX*(sx/camx))
        yi = centerY*(sy/camy)
        pyautogui.moveTo(xi, yi) 
        
        
        
        print("In two object mode")
#        time.sleep(1)
        
    elif(len(contours)==3):
        #three object mode
        cnt1 = contours[0]
        m = cv2.moments(cnt1)
        cx1 = int(m['m10']/m['m00'])
        cy1 = int(m['m01']/m['m00'])
        cv2.circle(img, (cx1, cy1), 3, (0, 0, 255), -1)
        
        cnt2 = contours[1]
        m2 = cv2.moments(cnt2)
        cx2 = int(m2['m10']/m2['m00'])
        cy2 = int(m2['m01']/m2['m00'])
        cv2.circle(img, (cx2, cy2), 3, (0, 0, 255), -1)
        
        cnt3 = contours[2]
        m3 = cv2.moments(cnt3)
        cx3 = int(m3['m10']/m3['m00'])
        cy3 = int(m3['m01']/m3['m00'])
        cv2.circle(img, (cx3, cy3), 3, (0, 0, 255), -1)
        cv2.imshow("img", img)
        print("In three object mode")
        
    else:
        print("Neither in one, two or three object mode!!")
    
    
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.imshow("img", img)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()
