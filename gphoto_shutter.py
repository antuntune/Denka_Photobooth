import subprocess

# Run the gphoto2 command
command = ["gphoto2", "--get-config", "/main/status/shuttercounter"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = process.communicate()

# Check for errors
if process.returncode != 0:
    print(f"Error: {stderr}")
else:
    # Parse the "Current" value from the output
    lines = stdout.split('\n')
    for line in lines:
        if line.startswith("Current:"):
            current_value = line.split(":")[1].strip()
            print(f"Current Shutter Count: {current_value}")
