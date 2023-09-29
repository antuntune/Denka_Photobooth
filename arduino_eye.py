import serial
import serial.tools.list_ports
import time
import json

class ArduinoController:
    def __init__(self):

        pass

    def establishConnection(self):

        # List available serial ports
        available_ports = list(serial.tools.list_ports.comports())

        if not available_ports:
            print("No available serial ports found. Arduino not connected.")
            self.arduino_connected = False
            #self.arduinoStatus = False
        else:
            serial_port = available_ports[0].device
            baud_rate = 9600
            try:
                self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
                time.sleep(2)
                self.arduino_connected = True
            except serial.SerialException as e:
                print(f"Failed to establish connection to {serial_port}: {e}")
        return self.arduino_connected


    def send_command_on(self):
        print("saljem on")
        if self.arduino_connected == True:
            print("povezan je i ne pali")
            self.ser.write(b'1')
        else:
            print("nije povezan")

    def send_command_off(self):
        print("saljem off")
        if self.arduino_connected == True:
            self.ser.write(b'0')

    def send_command_idle(self):
        if self.arduino_connected == True:
            self.ser.write(b'2')
    
    def close_connection(self):
        if self.arduino_connected == True:
            self.ser.close()


    def initJsonVar(self):
        # ucitavanje config.jsona i metanje u varijable da se lakse koristi
        with open('config.json', 'r') as f:
            # Load the contents of the file into a dictionary
            config = json.load(f)
            self.eventId_ = config['eventId_']
            self.tema_ = config['tema_']

        self.eventId = self.eventId_[0]
        self.tema = self.tema_[0]
        self.EventAlbumPath = config['eventAlbumPath']
        self.albumPath = config['albumPath']
        self.cardPath = config['cardPath']
        self.cardBright = config['cardBright']
        self.arduinoStatus = config['Arduino']
        self.whatsapp = config['WhatsApp']


    def loadJson(self):
        self.eventAlbumPath = self.albumPath + self.eventId + "/"
        #self.cardPath = self.eventAlbumPath + "/" + self.eventId + ".jpg"
        # Create a dictionary with the specific key-value pair
        data = {
            "eventId_": self.eventId_,
            "tema_": self.tema_,
            "eventId": self.eventId,
            "tema": self.tema,
            "albumPath": self.albumPath,
            "eventAlbumPath": self.eventAlbumPath,
            "cardPath": self.cardPath,
            "cardBright": self.cardBright,
            "Arduino": self.arduinoStatus,
            "WhatsApp": self.whatsapp
        }

        # Write data to the JSON file
        with open("config.json", "w") as file:
            json.dump(data, file)

