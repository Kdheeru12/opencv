# import the opencv library 
import shutil
import os
import numpy as np
import cv2

filename = 'video.avi'
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
    path = ''
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']
cap = cv2.VideoCapture(0) 
dims = get_dims(cap,res=myres)
VIDEO_TYPE_cv2 = get_video_type(filename)
out = cv2.VideoWriter(filename,VIDEO_TYPE_cv2,frames_per_seconds,dims)
while(True): 
	
	# Capture the video frame 
	# by frame 
    ret, frame = cap.read()

    out.write(frame)
    qui='q'
	# Display the resulting frame 
    cv2.imshow('frame', frame) 
	
	# the 'q' button is set as the 
	# quitting button you may use any 
	# desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord(qui): 
        break

# After the loop release the cap object 
cap.release() 
# Destroy all the windows 
out.release()
cv2.destroyAllWindows()
import moviepy.editor as moviepy
clip = moviepy.VideoFileClip("video.avi")
clip.write_videofile("video.mp4")
