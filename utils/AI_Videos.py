import cv2
from threading import Timer

loop = None

def initializeAiVideo():
    global loop
    cap = cv2.VideoCapture("assets/AISilentVideo.mp4")
    if not cap.isOpened():
        print("Cannot initialize cap.")
        exit()
    windowName = 'Yahkart-AI'
    # Get length of the video.
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Initialize count.
    count = 0
    # cv2.namedWindow(windowName)



    # Frames loop.
    while True:
        if(loop == False):
            cap = cv2.VideoCapture("assets/AISilentVideo.mp4")
            count = 0
            video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            loop = None
        if(loop == True ):
            cap = cv2.VideoCapture("assets/AISpeakingVideo.mp4")
            loop = None
            count = 0
            video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Check length of the video.
        if count == video_length:
            # Reset to the first frame. Returns bool.
            _ = cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            count = 0
        
        # Get the frame.
        success, image = cap.read()
        if not success:
            print("Cannot read frame.")
            break


        cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        # do something with the image.
        cv2.imshow(windowName, image)



        # Quit by pressing 'q'.
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        count += 1

    # Post loop.
    cap.release()
    cv2.destroyAllWindows()

def endSpeakingVideo():
    global loop
    loop = False

def startSpeakingVoice():
    global loop
    loop = True

if __name__ == "__main__":
    initializeAiVideo()
    t = Timer(1.0, startSpeakingVoice)
    t.start() 
    startSpeakingVoice()