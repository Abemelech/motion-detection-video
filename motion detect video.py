import cv2, time
from datetime import datetime

time = str(int(datetime.now().timestamp()))

first_frame = None

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter(time+'.mp4', fourcc, 60.0, (640,480), cv2.CAP_DSHOW)

fps = 0
reset = 0

while True:
    fps += 1

    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0) 


    #if first_frame is None:
    if first_frame is None or reset > 3000:
        first_frame = gray
        reset = 0   
        continue
    
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame= cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  

    for countour in cnts:
        if cv2.contourArea(countour) < 5000:
            reset += 1
            print(reset)
            continue
        (x,y,w,h) = cv2.boundingRect(countour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
        #cv2.imwrite(str(fps)+".jpg", frame)
        out.write(frame)

    cv2.imshow("Capturing", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold", thresh_frame)
    cv2.imshow("Color Frame", frame)


    
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
out.release()
cv2.destroyAllWindows()