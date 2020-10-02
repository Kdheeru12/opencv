from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d.%m.%Y.%H.%M.%S")
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer IP Address is:" + IPAddr)

filename = str(IPAddr)+str(dt_string)+'.avi'
filename1 = str(IPAddr)+str(dt_string)+'.mp4'
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
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
    
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# After the loop release the cap object 
cap.release() 
# Destroy all the windows 
out.release()
cv2.destroyAllWindows()
import moviepy.editor as moviepy
clip = moviepy.VideoFileClip(filename)
clip.write_videofile(filename1)
os.remove(filename)
files = [filename1]
for f in files:
    shutil.move(f, 'media')
deo = Video(url=filename1)
deo.save()