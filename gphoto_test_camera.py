import subprocess

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

        return model_name.strip(), port.strip()

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return "Error", "Error"

if __name__ == "__main__":
    camera_model, camera_port = get_camera_info()
    camera_model = camera_model.split(" usb:")[0]  # Remove the " usb:" and everything after it
    print("Camera Model:", camera_model)
    print("Camera Port:", camera_port)
