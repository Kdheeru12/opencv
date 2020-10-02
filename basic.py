import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import shutil
path = 'imagesbasic'
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer IP Address is:" + IPAddr)

filename = 'dhe1.avi'
filename1 = 'dhe1.mp4'
print(type(filename),type(filename1))
print(filename1,filename)
frames_per_seconds = 24.0
myres = '720p'
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}
def get_dims(cap,res='1080p'):
    width,height = STD_DIMENSIONS['480p']
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
        change_res(cap,width,height)
        return width,height
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}
def get_video_type(filename):
    path = '../imagesbasic'
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']
cap = cv2.VideoCapture(0) 
dims = get_dims(cap,res=myres)
VIDEO_TYPE_cv2 = get_video_type(filename)
out = cv2.VideoWriter(filename,VIDEO_TYPE_cv2,frames_per_seconds,dims)
path = 'imagesbasic'
images = []
classnames = []
mylist = os.listdir(path)
print(mylist)

for cl in mylist:
    curimg = cv2.imread(f'{path}/{cl}')
    images.append(curimg)
    classnames.append(os.path.splitext(cl)[0])
print(classnames)
def findEncodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist
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
while(True):
    ret, frame = cap.read()

    out.write(frame)
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
import moviepy.editor as moviepy
clip = moviepy.VideoFileClip(filename)
clip.write_videofile(filename1)


