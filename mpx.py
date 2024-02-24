from threading import Lock, Thread
from time import sleep
import adafruit_vl53l0x
from adafruit_mcp230xx.mcp23017 import MCP23017
import digitalio
import board
import busio
import time

# TODO:
# - Exceptions management
# - Attribute a placement to sensors (front, back, sides)

# Default adress of Vl53L0X
DEFAULT_ADDRESS = 0x29
MAX_DIST = 3000


# MDB Class

# __init__(nb_sensors, sensor_address, expander_address, refresh):
#   - nb_sensors        : Number of VL53L0X
#   - sensor_address    : Address of the first sensors
#   - expander_address  : Address of the Gpio Expander
#   - refresh           : Refresh of the loop
# Sensors wil be between sensor_address and sensor_address + nb_sensors - 1
# Will init the gpio expanders and sensors
# Will launch a thread for the loop

# loop():
# Loop to get scan with a certain refresh
# Must run in a thread
# Will use a lock to update the data of the class

# get_scan:
#   Will return a scan (a list of measurement)

# __str__():
# Return a string of the status of the MDB

class Mpx:

    def __init__(self, nb_sensors, sensor_address=0x29, expander_address=0x20, refresh=0.1, debug=False):
        self.coef = 255 / (MAX_DIST / 2)

        # Init I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensors = []
        self.scan = []

        # Init MCP
        self.mcp = MCP23017(self.i2c, address=expander_address)

        self.nb_sensors = nb_sensors
        self.refresh = refresh
        self.debug = debug

        # Init all sensors
        self.init_sensors(sensor_address)

        self.lock = Lock()
        Thread(target=self.loop).start()

    def init_sensors(self, sensors_address):

        # Put all XSHUT pins to LOW
        print("in init_sensor")
        for i in range(0, self.nb_sensors):
            self.mcp.get_pin(i).switch_to_output()
            self.mcp.get_pin(i).value = False

        # Init sensor one by one and change addresses
        for i in range(0, self.nb_sensors):
            self.mcp.get_pin(i).value = True
            self.sensors.append(adafruit_vl53l0x.VL53L0X(self.i2c))  # , address=DEFAULT_ADDRESS))
            self.sensors[i].set_address(sensors_address + i + 1)

    def loop(self):
        while True:

            tmp = []

            for i in range(0, self.nb_sensors):
                dist = self.sensors[i].range
                tmp.append(dist)
            # Update scan
            with self.lock:
                self.scan = tmp

            time.sleep(self.refresh)

    def get_scan(self):
        tmp = []
        with self.lock:
            tmp = self.scan
        return tmp

    def __str__(self):
        return ""