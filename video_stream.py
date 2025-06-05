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
        self.last_frame = None
        self.ffmpeg_proc = None

    def stop(self):
        self.stopped = True
        dslr.killStream()
        if self.ffmpeg_proc:
            self.ffmpeg_proc.terminate()
            try:
                self.ffmpeg_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.ffmpeg_proc.kill()
        self.quit()
        self.wait()

    def start(self):
        # Pokreni gphoto2 | ffmpeg proces samo jednom
        cmd = (
            "gphoto2 --stdout --capture-movie | "
            "ffmpeg -hide_banner -loglevel error -fflags nobuffer -i - "
            "-c:v mjpeg -q:v 5 "
            "-vf \"scale=1280:720:flags=bicubic,format=yuvj422p\" "
            "-f v4l2 /dev/video2"
        )
        self.ffmpeg_proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
        #time.sleep(1.0)  # Pusti da proces pokrene stream
        self.stopped = False
        super().start()

    def run(self):

        cap = cv2.VideoCapture('/dev/video2', cv2.CAP_V4L2)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 24)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimal buffer
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 1.0)
        cap.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY)  # Enable hardware acceleration

        while not self.stopped:
            try:
                ret, frame = cap.read()

                # Skip processing if frame is empty
                if not ret or frame is None or frame.size == 0:
                    self.msleep(2)
                    continue

                # Validate frame dimensions
                if frame.shape[0] != 720 or frame.shape[1] != 1280 or frame.shape[2] != 3:
                    print(f"Skipping invalid frame: {frame.shape}")
                    self.msleep(2)
                    continue

                # Process valid frame
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qimg = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

                if not qimg.isNull():
                    pixmap = QPixmap.fromImage(qimg)
                    self.frameCaptured.emit(pixmap)

            except Exception as e:
                # Handle specific JPEG corruption errors
                if "Corrupt JPEG" in str(e) or "bad Huffman code" in str(e):
                    print("Skipped corrupt JPEG frame")
                else:
                    print(f"Frame processing error: {e}")

            # Add slight delay to prevent buffer overrun
            self.msleep(2)

        cap.release()
