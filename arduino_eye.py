import serial
import serial.tools.list_ports
import time

class ArduinoController:
    def __init__(self):

        # List available serial ports
        available_ports = list(serial.tools.list_ports.comports())

        if not available_ports:
            print("No available serial ports found. Arduino not connected.")
            self.arduino_connected = False
        else:
            serial_port = available_ports[0].device
            baud_rate = 9600
            self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
            time.sleep(2)
            self.arduino_connected = True

    def send_command_on(self):
        if self.arduino_connected == True:
            self.ser.write(b'1')

    def send_command_off(self):
        if self.arduino_connected == True:
            self.ser.write(b'0')

    def send_command_idle(self):
        if self.arduino_connected == True:
            self.ser.write(b'2')
    
    def close_connection(self):
        if self.arduino_connected == True:
            self.ser.close()