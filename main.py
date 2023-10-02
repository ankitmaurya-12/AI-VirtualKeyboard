import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
#import numpy as np
from pynput.keyboard import Controller



cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [["0","1","2","3","4","5","6","7","8","9"],
        ["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

finalText=''

keyboard = Controller()

def drawALL(img,buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 13, y + 56), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

class Button():
    def __init__(self, pos, text, size=[73, 73]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# myButton1  = Button([200,100],"W")
# myButton2= Button([300,100],"E")

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawALL(img, buttonList)


    if lmList:
        for button in buttonList:
            x,y= button.pos
            w,h=button.size

            if x< lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 13, y + 56), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l,_,_= detector.findDistance(8,12, img,draw=False)
                print(l)

                if l<30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 13, y + 56), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.22)

    cv2.rectangle(img, (62,450), (920, 500) , (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (65,490), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)







    # img = myButton.draw(img)
    # img = myButton1.draw(img)
    # img = myButton2.draw(img)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
