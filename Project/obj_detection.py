import numpy as np
import cv2 
from matplotlib import pyplot as plt
import imutils


def blackball(frame, hsv, lower, upper):
    ret = []
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    conts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    ##found blue
    x=-1
    y=-1
    #if (len(conts) > 0):
    #c = max(conts, key=cv2.contourArea)
    for c in conts:
        
        if cv2.contourArea(c) > 250 and cv2.contourArea(c) < 1500:
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
            cv2.circle(frame, center, 5, (0,0,255), -1)
            ret = ret + [(x,y)]

    return ret, frame
def ball(frame, hsv, lower, upper):
    ret = []
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    conts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    ##found blue
    x=-1
    y=-1
    #if (len(conts) > 0):
    #c = max(conts, key=cv2.contourArea)
    for c in conts:
        print(cv2.contourArea(c))
        if cv2.contourArea(c) > 30:
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
            cv2.circle(frame, center, 5, (0,0,255), -1)
            ret = ret + [(x,y)]

    return ret, frame


def detector():
    cap = cv2.VideoCapture(2)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
    while(True):
        #frame capture
        ret, frame = cap.read()
        
        frame = imutils.resize(frame, width=600)
        #image operations
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        objects = []
        ret, frame = blackball(frame, hsv, np.array([0,0,0]), np.array([179,255,75])) ##black (robot)
        objects = objects +ret
        
        ret, frame = ball(frame, hsv, np.array([100,50,50]), np.array([130,255,255])) ##blue ball (target)
        objects = objects +ret
        ret, frame = ball(frame, hsv, np.array([130,50,50]), np.array([179,255,255])) ##red balls (obstacles)
        objects = objects +ret
        ret, frame = ball(frame, hsv, np.array([0,100,100]), np.array([55,255,255])) ##red balls (obstacles)
        objects = objects +ret
        
        cv2.imshow('frame', frame)
        if len(objects) >= 3:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    #print(objects)
    objects = [(obj[0]//60, obj[1]//60) for obj in objects]
    print(objects)
    cap.release()
    return objects
    #cv2.destroyAllWindows()



