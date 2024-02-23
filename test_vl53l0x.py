import time
import board
import busio
import adafruit_vl53l0x
from mpx import Mpx
from time import sleep

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

while True:
    try:
        # Read the distance
        distance_mm = vl53.range
        print("Distance:", distance_mm, "mm")
        time.sleep(0.1)
    except RuntimeError as e:
        print("Error:", e)

# mpx = Mpx(5)
#
# while True:
#     scan = mpx.get_scan()
#     print("---- New scan -----")
#     for i in range(len(scan)):
#         print("%d: %f" % (i + 1, scan[i]))
#     sleep(1)
