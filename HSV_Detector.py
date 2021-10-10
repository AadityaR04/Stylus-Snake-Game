import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

hsv=[]

def hsv_Detector():
    '''For Detecting the HSV of the Stylus'''
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        frame = cv.flip(frame, 1)

        #Removing noise of the frame
        filtered_frame = cv.GaussianBlur(frame,(11,11),0)

        #Drawing region
        cv.rectangle(frame,(320-50,240-50),(320+50,240+50),(0,255,0),2)
        cv.circle(frame,(320,240),3,(0,0,255),-1)

        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(frame,'Align center of stylus to the dot',(50,50), font,1,(0,0,255),2,cv.LINE_AA)
        cv.putText(frame,'Press Q to capture stylus',(100,430), font,1,(255,255,0),2,cv.LINE_AA)

        box=filtered_frame[240-5:240+5,320-5:320+5]
        hsv_box=cv.cvtColor(box, cv.COLOR_BGR2HSV)

        # Display the resulting frame
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            h=[]
            s=[]
            v=[]

        #Taking the HSV values of each pixel
            for i in range(10):
                for j in range(10):
                    h.append(hsv_box[i,j,0])
                    s.append(hsv_box[i,j,1])
                    v.append(hsv_box[i,j,2])

            #Finding average of all the HSV values
            hsv.append(int(sum(h)/100))
            hsv.append(int(sum(s)/100))
            hsv.append(int(sum(v)/100))
            break
    # When everything done, release the capture

    cap.release()
    cv.destroyAllWindows()

    return(hsv)