import cv2
import numpy as np
import pickle
 
def mouseRGB(event,x,y,flags,param):
    global hsv_1
    global hsv_2
    global hsv_3
    global dict_hsv
    if (event == cv2.EVENT_LBUTTONDOWN) and (cv2.waitKey(0) & 0xFF == ord('r')):
        print("Red Color Captured!!")
        hsv_1.append(image[y,x,0])
        hsv_1.append(image[y,x,1])
        hsv_1.append(image[y,x,2])
        colors = image[y,x]
        dict_hsv['hsv_1'] = {"lower_bound":[abs(i-10) for i in hsv_1],"upper_bound":[i+10 for i in hsv_1]} 
        hsv_value= np.uint8([[[i for i in hsv_1]]])
        hsv = cv2.cvtColor(hsv_value,cv2.COLOR_BGR2HSV)
        print ("HSV : " ,hsv)
        print("Red: ",hsv_1[2])
        print("Green: ",hsv_1[1])
        print("Blue: ",hsv_1[0])
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)
    elif (event == cv2.EVENT_LBUTTONDOWN) and (cv2.waitKey(0) & 0xFF == ord('g')):
        print("green Color Captured!!")
        hsv_2.append(image[y,x,0])
        hsv_2.append(image[y,x,1])
        hsv_2.append(image[y,x,2])
        colors = image[y,x]
        dict_hsv['hsv_2'] = {"lower_bound":[abs(i-10) for i in hsv_2],"upper_bound":[i+10 for i in hsv_2]} 
        hsv_value= np.uint8([[[i for i in hsv_2]]])
        hsv = cv2.cvtColor(hsv_value,cv2.COLOR_BGR2HSV)
        print ("HSV : " ,hsv)
        print("Red: ",hsv_2[2])
        print("Green: ",hsv_2[1])
        print("Blue: ",hsv_2[0])
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)
    elif (event == cv2.EVENT_LBUTTONDOWN) and (cv2.waitKey(0) & 0xFF == ord('y')):
        print("yellow Color Captured!!")
        hsv_3.append(image[y,x,0])
        hsv_3.append(image[y,x,1])
        hsv_3.append(image[y,x,2])
        colors = image[y,x]
        dict_hsv['hsv_3'] = {"lower_bound":[abs(i-10) for i in hsv_3],"upper_bound":[i+10 for i in hsv_3]} 
        hsv_value= np.uint8([[[i for i in hsv_3]]])
        hsv = cv2.cvtColor(hsv_value,cv2.COLOR_BGR2HSV)
        print ("HSV : " ,hsv)
        print("Red: ",hsv_3[2])
        print("Green: ",hsv_3[1])
        print("Blue: ",hsv_3[0])
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)
        
        
hsv_1 = list()
hsv_2 = list()
hsv_3 = list()
dict_hsv = dict()
cap = cv2.VideoCapture(1)
if cap.read()[0]==False:
    cap = cv2.VideoCapture(0)
while(1):
    _, image = cap.read()
    cv2.namedWindow('mouseRGB')
    cv2.setMouseCallback('mouseRGB',mouseRGB)    
    cv2.imshow('mouseRGB',image)
    if cv2.waitKey(1) & 0xFF == 27:
        with open("range.pickle","wb") as file:
            pickle.dump(dict_hsv,file)
        break
    else:
        pass
cv2.destroyAllWindows()
cap.release()
