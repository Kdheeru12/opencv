import cv2
import numpy as np

cap  = cv2.VideoCapture(0)
whT = 320
nmsThreshold = 0.3
names = 'coco.names'
classNames = []
with open(names,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
#print(classNames)
# print(len(classNames))
modelConfiguration = 'yolo3.cfg'
modelWeights = 'yolov3.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
def findObjects(outputs,img):
    hT,wT,cT = img.shape
    bbox = []
    classIds = []
    confidence = []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidences = scores[classId]
            if confidences  > 0.5:
                w,h = int(detection[2]*wT),int(detection[3]*hT)
                x,y = int((detection[0]*wT)-(w/2)),int((detection[1]*hT)-(h/2))
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confidence.append(float(confidences))
    print(len(bbox))
    indices = cv2.dnn.NMSBoxes(bbox,confidence,0.5,nmsThreshold)
    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
        cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confidence[i]*100)}',(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,255),2)

while True:
    success,img = cap.read()
    blob = cv2.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)
    net.setInput(blob)
    layerNames = net.getLayerNames()
    
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    findObjects(outputs,img)
    cv2.imshow('Image',img)
    cv2.waitKey(1)