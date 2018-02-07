from __future__ import division

import cv2
import numpy as np
import track
import detect


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
        cv2.line(frame, (int(width/2),height), (int(width/2),0 ), (255, 255, 255), 2)


        if predicted is not None:
            #koseler
            cv2.line(frame, (predicted[0][0], predicted[0][1]), (predicted[0][2], predicted[0][3]), (0, 255, 255), 5)
            cv2.line(frame, (predicted[1][0], predicted[1][1]), (predicted[1][2], predicted[1][3]), (0, 255, 255), 5)

            #alan
            ic = np.array(
                [
                [predicted[0][0],predicted[0][1]],
                [predicted[0][2],predicted[0][3]],
                [predicted[1][0],predicted[1][1]],
                [predicted[1][2],predicted[1][3]]
                ],
                np.int32)

            #alanin ortasi
            cv2.line(frame, 
            ((predicted[1][0]+predicted[0][2])/2,(predicted[1][1]+predicted[0][3])/2),
             ((predicted[0][0]+predicted[1][2])/2, (predicted[0][1]+predicted[1][3])/2), (0, 0, 255), 5)
           




            overlay = frame.copy()
            cv2.fillPoly(overlay, [ic], (100, 50, 50, 50) )
            opacity = 0.4
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
 
        lt.update(lanes)


        cv2.imshow('output', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


main("yol.mp4")