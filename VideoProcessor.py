import numpy as np
import cv2 as cv


class VideoProcessor:
    def __init__(self, path):
        self.face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml') 
        self.path = path
        self.frames = []

    # split the video into frames
    def process(self):
        video = cv.VideoCapture(self.path)

        if not video.isOpened():
            print("Error. video didn't open.")
        else:
            totalFrames = video.get(cv.CAP_PROP_FRAME_COUNT)
            while video.get(cv.CAP_PROP_POS_FRAMES) <  totalFrames:
                ret, frame = video.read()

                if ret == False:
                    print("frame ", video.get(cv.CAP_PROP_FRAME_COUNT), " not read")
                    return None
                
                faces = self.face_detector(frame)
                
                # reduce rezolution to 100*100
                # h, w = frame.shape[:2]
                # temp = cv.resize(frame, (100,100), interpolation= cv.INTER_LINEAR)
                # frame = cv.resize(temp, (w, h), interpolation= cv.INTER_LINEAR)

                # if len(faces) > 1:
                #     print("There are more then one face in the frame. Try again.")
                #     continue
                # if len(faces) < 1:
                #     print("There is no face in the frame. Try again.")
                #     continue
                
                for (x, y, w, h) in faces:
                    face = frame[y:y+h, x:x+w]
                    if face.size == 0:
                        continue
                    self.frames.append(face)
        return self.frames
    
    
    def face_detector(self, image):
        
        
        target_width = 1300
        scale = image.shape[1]/target_width #the scale is the sorce width devided by the desierd with
        target_hight = int(image.shape[0]/scale)
        image = cv.resize(image, (target_width, target_hight), interpolation=cv.INTER_AREA)
                
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)     # convert to gray scale for face haarcascade algoritem   

        image = cv.equalizeHist(image)
        
        faces = self.face_cascade.detectMultiScale(
            image, 
            scaleFactor=1.1,       # סולם הפחתת גודל התמונה בכל מעבר
            minNeighbors=5,        # מספר מינימלי של "שכנים" להכרזה על פנים
            minSize=(30, 30)       # גודל מינימלי לחלון שבו ינסו לגלות פנים
        )
       
        return faces
    
    
    # returns number of frames in one second
    def framePerSec(self):
        video = cv.VideoCapture(self.path)
        if not video.isOpened():
            print("Error. video didn't opened.")
        else:
            return video.get(cv.CAP_PROP_FPS)
    
        


