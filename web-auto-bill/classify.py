import cv2
import numpy as np
from cvzone.ClassificationModule import Classifier

item = []

with open('bill.csv', 'w') as creating_new_csv_file: 
   pass 

def runprg():
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    myClassifier = Classifier('MyModel/keras_model.h5', 'MyModel/labels.txt')
    price = [0,1000,1500,20,40]

    w = 1


    def bill(name, price):
        cnt = 0
        for i in range(0, len(item)):
            if item[i][0] == name:
                item[i][1] += 1
                item[i][2] += price
                cnt = 1
        if cnt == 0:
            item.append([name, 1, price])

    while True:
        _, frame= cap.read();
        blurred_frame = cv2.GaussianBlur(frame, (5,5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
        lowerblue=np.array([38, 86, 0])
        upperblue=np.array([121,255,255])
        mask=cv2.inRange(hsv, lowerblue, upperblue)
        predictions, index = myClassifier.getPrediction(frame, scale=1)
        print (myClassifier.getPrediction(frame,scale=1))
        contours, _=cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        roi = frame[340: 720,500: 800]
        for cnt in contours:
            area=cv2.contourArea(cnt)
            if area > 100:
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
        name = myClassifier.list_labels[index]
        if (index == 0):
            w = 1
        elif (index != 0):
            if (w == 1):
                bill(name, price[index])
                w = 0
        #print(contours)
        cv2.imshow('frame',frame)
        cv2.imshow("Mask",mask)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    sumprice = 0
    if(len(item)>0):
        for i in range(0, len(item)):
            sumprice += item[i][2]
    item.insert(0, ['Item', 'Quantity', 'Price'])
    item.append(['Total', '', sumprice])

    with open('bill.csv', 'r+') as f:
        myDataList = f.readline()
        for line in myDataList:
            entry = line.split(',')
        for i in range(0, len(item)):
            f.writelines(f'\n{item[i][0]},{item[i][1]},{item[i][2]}')

    
