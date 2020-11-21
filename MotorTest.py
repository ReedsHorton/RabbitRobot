from adafruit_motorkit import MotorKit
import time
#import board


kit = MotorKit()

kit.motor1.throttle = 1.0
#time.sleep(1)
kit.motor1.throttle = None
#time.sleep(2)
#kit.motor1.throttle = -1
#time.sleep(1)
#kit.motor1.throttle = 0

