from adafruit_motorkit import MotorKit
import time

import pigpio
import rotary_encoder



pos = 0

def callback(way):

	global pos

	pos += way

	print("pos={}".format(pos))

pi = pigpio.pi()

decoder = rotary_encoder.decoder(pi, 22, 23, callback)

#kit = MotorKit()

#kit.motor1.throttle = 1.0
#time.sleep(1)
#kit.motor1.throttle = None
#time.sleep(2)
#kit.motor1.throttle = -1
#time.sleep(1)
#kit.motor1.throttle = 0

time.sleep(300)

decoder.cancel()

pi.stop()