import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import shutil

path = 'imagesbasic'
images = []
classnames = []
mylist = os.listdir(path)
print(mylist)

for cl in mylist:
    curimg = cv2.imread(f'{path}/{cl}')
    images.append(curimg)
    classnames.append(os.path.splitext(cl)[0])
def findEncodings(images):
    encodelist = []
    for img in images:
        print(img)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist
encodelistkmown = findEncodings(images)
def markAttendance(name):
    with open('attandance.csv','r+') as f:
        myDatalist = f.readlines()
        namelist = []
        for line in myDatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')

encodelistknown = findEncodings(images)
print(len(encodelistknown))
notfound = 0
cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    success,img = cap.read()
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgs)
    encodesCurFrame = face_recognition.face_encodings(imgs,facesCurFrame)
    for encodeface,faceloc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodelistknown,encodeface)
        facedis = face_recognition.face_distance(encodelistknown,encodeface)
        print(facedis)
        matchindex = np.argmin(facedis)
        if matches[matchindex]:
            name = classnames[matchindex].upper()
            print(name)
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
        else:
            notfound = notfound + 1
            ntfund = str(notfound)
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,'notfound'+ntfund,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.imshow('webcam',img)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
cap.release() 
# Destroy all the windows 
out.release()
cv2.destroyAllWindows()
