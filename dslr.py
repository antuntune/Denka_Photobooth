from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
from multiprocessing import Process
import threading
import json
import os
from sh import gphoto2 as gp
import subprocess
from PIL import Image


# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)
    eventId = config['eventId']
    tema = config['tema']

def renameImage(name):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith("jpg"):
                os.rename(filename, (name + ".jpg"))


def captureImage():
    sleep(0.5)
    cmd = "gphoto2 --capture-image-and-download"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # Wait for the command to finish and get the return code
    return_code = process.wait()


def killStream():
    p = subprocess.Popen([ 'ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():     
        if b'ffmpeg' in line:
                # Kill the process!
            pid = int (line.split(None,1) [0] )
            os.kill (pid, signal.SIGKILL)

    p = subprocess.Popen([ 'ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():     
        if b'gvfs-gphoto2-volume-monitor' in line:
                # Kill the process!
            pid = int (line.split(None,1) [0] )
            os.kill (pid, signal.SIGKILL)

    p = subprocess.Popen([ 'ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():     
        if b'gvfsd-gphoto2' in line:
                # Kill the process!
            pid = int (line.split(None,1) [0] )
            os.kill (pid, signal.SIGKILL)


def resizeImage(name):
    # New image size
    new_size = (1500, 1000)
    # Open image
    image = Image.open(name)
    # Get image info
    exif = image.info['exif']
    # resize with Lanczos method
    resized_image = image.resize(new_size, resample = Image.LANCZOS)
    resized_image.save(name, quality=96, exif=exif)
