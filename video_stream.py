import subprocess, os, signal
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import time
import dslr

class VideoThread(QThread):
    frameCaptured = pyqtSignal(QPixmap)


    def __init__(self):
        super().__init__()
        self.stopped = False
        self.threadId = self.currentThreadId()

    def stop(self):
        self.stopped = True
        dslr.killStream()

    def start(self):
        cmd = "gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -s 1024x680 -threads 1 -f v4l2 /dev/video0"
        #cmd = "gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv422p -threads 1 -f v4l2 /dev/video0"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(3)
        self.stopped = False
        super().start()

    def run(self):
        cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        while not self.stopped:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.frameCaptured.emit(pixmap)
            self.msleep(1)


