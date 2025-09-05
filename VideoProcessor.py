import numpy as np
import cv2 


class VideoProcessor:
    def __init__(self, path):
        self.path = path

    # split the video into frames
    def process(self):
        frames = []
        video = cv2.VideoCapture(self.path)

        if not video.isOpened():
            print("Error. video didn't open.")
        else:
            totalFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            while video.get(cv2.CAP_PROP_POS_FRAMES) <  totalFrames:
                ret, frame = video.read()

                if ret == False:
                    print("frame ", video.get(cv2.CAP_PROP_FRAME_COUNT, " not read"))
                    return None
                
                # reduce rezolution to 100*100
                # h, w = frame.shape[:2]
                # temp = cv2.resize(frame, (100,100), interpolation= cv2.INTER_LINEAR)
                # frame = cv2.resize(temp, (w, h), interpolation= cv2.INTER_LINEAR)

                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to gray scale                    
                faces = face_cascade.detectMultiScale(grayFrame, scaleFactor=1.1, minNeighbors=5) # detact faces

                if len(faces) > 1:
                    print("There are more then one face in the frame. Try again.")
                    continue
                if len(faces) < 1:
                    print("There is no face in the frame. Try again.")
                    continue
                
                x, y, w, h = faces[0]
                frame = frame[y:y+h, x:x+w]
                if frame.size == 0:
                    continue
                frames.append(frame)
        return frames
    
    # returns number of frames in one second
    def framePerSec(self):
        video = cv2.VideoCapture(self.path)
        if not video.isOpened():
            print("Error. video didn't opened.")
        else:
            return video.get(cv2.CAP_PROP_FPS)
        
def main():
        path = r"C:\Users\naama\Documents\studing\stress-level-analyzer\videos\naama_hand.mp4"
        video_processor = VideoProcessor(path)
        frames = video_processor.process()
        if frames == None:
            return

        print("length of video is: " , len(frames) , " frames") # length of video
        print("number of frames per second: ", video_processor.framePerSec()) # rate

        # show the frames one by one
        if not len(frames) == 0:
            i = 1
            for frame in frames:
                cv2.imshow("frame "+str(i), frame)
                cv2.waitKey(0) 
                cv2.destroyAllWindows()
                i += 1

if __name__ == "__main__":
    main()