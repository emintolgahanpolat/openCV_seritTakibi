from __future__ import division

import cv2
import numpy as np
import track
import detect

font = cv2.FONT_HERSHEY_SIMPLEX

def main(video_path):
    cap = cv2.VideoCapture(video_path)

    ret, img = cap.read()
    height,width,layer=img.shape
    print height,width,layer

    screen_rate=0.4
    width=int(width*screen_rate)
    height=int(height*screen_rate)


    ticks = 0

    lt = track.LaneTracker(2, 0.1, 500)
    ld = detect.LaneDetector(180)
    while cap.isOpened():
        precTick = ticks
        ticks = cv2.getTickCount()
        dt = (ticks - precTick) / cv2.getTickFrequency()

        ret, frame = cap.read()
        frame = cv2.resize(frame,None,fx=screen_rate, fy=screen_rate, interpolation = cv2.INTER_CUBIC)


        predicted = lt.predict(dt)

        lanes = ld.detect(frame)

            #goruntu ortasi
        cv2.line(frame, (int(width/2),0), (int(width/2),height ), (255, 255, 255), 2)


        if predicted is not None:
            Ax=predicted[0][2]
            Ay=predicted[0][3]

            Bx=predicted[0][0]
            By=predicted[0][1]

            Cx=predicted[1][2]
            Cy=predicted[1][3]

            Dx=predicted[1][0]
            Dy=predicted[1][1]

            #koseler
            cv2.line(frame, (Ax, Ay), (Bx,By), (0, 255, 255), 5)
            cv2.line(frame, (Cx, Cy), (Dx,Dy), (0, 255, 255), 5)

            #alan
            ic = np.array(
                [
                [Ax,Ay],
                [Bx,By],
                [Cx,Cy],
                [Dx,Dy]
                ],
                np.int32)

            #alanin ortasi
            cv2.line(frame,((Ax+Dx)/2,(Ay+Dy)/2),((Bx+Cx)/2, (By+Cy)/2),(0, 0, 255), 5)

            cv2.circle (frame,((Ax+Dx)/2,(Ay+Dy)/2),5,(255,0,0),-1)

            cv2.line(frame,((Ax+Dx)/2,(Ay+Dy)/2),(int(width/2), (Ay+Dy)/2),(0, 255, 0), 3)
       
            veri="s"+str(((Ax+Dx)/2)-(width/2))
            cv2.putText(frame,veri, ((Ax+Dx)/2,(Ay+Dy)/2), font, 0.5, (255,255,255),1,cv2.LINE_AA)

            #kose isimleri
            cv2.putText(frame,'A', (Ax,Ay), font, 0.5, (255,255,255),1,cv2.LINE_AA)
            cv2.putText(frame,'B', (Bx,By), font, 0.5, (255,255,255),1,cv2.LINE_AA)
            cv2.putText(frame,'C', (Cx,Cy), font, 0.5, (255,255,255),1,cv2.LINE_AA)
            cv2.putText(frame,'D', (Dx,Dy), font, 0.5, (255,255,255),1,cv2.LINE_AA)




            overlay = frame.copy()
            cv2.fillPoly(overlay, [ic], (100, 50, 50, 50) )
            opacity = 0.4
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
 
        lt.update(lanes)


        cv2.imshow('output', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


main("yol.mp4")