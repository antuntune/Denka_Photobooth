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

        dslr.killStream()
        #dslr.killGphoto2Process()
        self.stopped = True

    def start(self):
        dslr.killStream()
        print("ubio stream na pocetku threada")
        #dslr.killGphoto2Process()
        cmd = "gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video0"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(3.2)
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
