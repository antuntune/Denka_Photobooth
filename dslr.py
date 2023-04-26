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
from PIL import ImageOps, Image


# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)
    eventId = config['eventId']
    tema = config['tema']
    mode = config['mode']

capturetarget = ["--set-config", "capturetarget=1"]
clearCommand = ["--folder", "/store_00010001/DCIM/100EOS5D", "-R", "--delete-all-files"]
#triggerCommand = ["--debug", "--capture-image-and-download"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]
autoFocusCommand = ["--set-config", "manualfocusdrive=1"]
SDcard = ["--set-config", "capturetarget=1"]

def renameImage(name):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith("jpg"):
                os.rename(filename, (name + ".jpg"))


def captureImage():
    killStream()
    killGphoto2Process()
    sleep(1.5)
    cmd = "gphoto2 --capture-image-and-download "
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # Wait for the command to finish and get the return code
    return_code = process.wait()
    while return_code != 0:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return_code = process.wait()
        if return_code == 0:
            print("Command executed successfully.")
        else:
           killGphoto2Process()
           print(f"Command failed with return code {return_code}")


def killGphoto2Process():
    p = subprocess.Popen([ 'ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():     
        if b'gphoto2' in line:
                # Kill the process!
            pid = int (line.split(None,1) [0] )
            os.kill (pid, signal.SIGKILL)

    p = subprocess.Popen([ 'ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():     
        if b'gvfsd-gphoto2' in line:
                # Kill tte process!
            pid = int (line.split(None,1) [0] )
            os.kill (pid, signal.SIGKILL)

def killStream():
    p = subprocess.Popen([ 'ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():     
        if b'ffmpeg' in line:
                # Kill the process!
            pid = int (line.split(None,1) [0] )
            os.kill (pid, signal.SIGKILL)


def resizeImage(name):
    # read an image from file
    img = Image.open(name)
    # define the desired output size
    new_size = (1500, 800)
    resized_img = ImageOps.fit(img, new_size, method=Image.BILINEAR)
    resized_img.save(name)

