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


def shutterCounter():
    killStream()
    # Run the gphoto2 command
    command = ["gphoto2", "--get-config", "/main/status/shuttercounter"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print(f"Error: {stderr}")
        return stderr
    else:
        # Parse the "Current" value from the output
        lines = stdout.split('\n')
        for line in lines:
            if line.startswith("Current:"):
                current_value = line.split(":")[1].strip()
                print(f"Current Shutter Count: {current_value}")
        return current_value

def get_camera_info():
    try:
        result = subprocess.run(['gphoto2', '--auto-detect'], capture_output=True, text=True, check=True)
        output = result.stdout
        lines = output.split('\n')
        
        model_name = None
        port = None
        
        # Find the line with the camera model and port information
        for line in lines:
            if "Canon EOS" in line:  # You can adjust this condition for different camera brands
                info = line.split()
                model_name = " ".join(info[1:])
                if len(info) > 2:
                    port = info[-1]

        if model_name is None:
            model_name = "No camera detected"
        if port is None:
            port = "Port information not found"

        #return model_name.strip(), port.strip()
        return model_name.strip()

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return "Error", e