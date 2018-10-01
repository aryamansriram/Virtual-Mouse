import cv2 as cv
import numpy
import matplotlib.pyplot as plt
def printThreshold(thr):
    print(thr)
kernel = numpy.ones((5,5))

cap = cv.VideoCapture(0)
cap.set(10,200)
cv.namedWindow('thresh')
cv.createTrackbar('trh1', 'thresh', 60, 100, printThreshold)

while(True):
    ret,frame = cap.read()
    frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    threshold = cv.getTrackbarPos('trh1','thresh')
    ret, image = cv.threshold(frame,threshold,255,cv.THRESH_BINARY)
    cv.imshow('thresh',image)
    k = cv.waitKey(10)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()
    
