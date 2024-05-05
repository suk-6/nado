import cv2
import random
from gaze_tracking import GazeTracking


class GazeAnalysis:
    def __init__(self) -> None:
        self.id = random.randint(0, 1000000)
        self.videoPath = f"/tmp/{self.id}.mp4"
        self.statusList = []

    def analysis(self):
        video = cv2.VideoCapture(self.videoPath)
        gaze = GazeTracking()

        while video.isOpened():
            ret, frame = video.read()
            if ret:
                gaze.refresh(frame)
                if gaze.is_blinking():
                    self.statusList.append("Blinking")
                if gaze.is_right():
                    self.statusList.append("right")
                if gaze.is_left():
                    self.statusList.append("left")
                if gaze.is_center():
                    self.statusList.append("center")
            else:
                break

        video.release()

        return self.statusList
