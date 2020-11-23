#!/usr/bin/env python3
from adafruit_motorkit import MotorKit
import time
import math

import pigpio
import rotary_encoder

def callback(way):
	global pos

	pos += way

	print("pos={}".format(pos))



def main():
	pos = 0


	pi = pigpio.pi()

	decoder = rotary_encoder.decoder(pi, 22, 23, callback)

	kit = MotorKit()

	time_now = time.time()
	kit.motor1.throttle = 1.0
	time.sleep(1)

	time_before = time.time()
	pos_before = pos
	time.sleep(5)
	time_now = time.time()
	pos_now = pos

	speed = ((pos_before - pos_now)/48)/(time_now - time_before)*math.pi*.0635

	speed = 1/speed * 100
	print("100m = " + str(speed))




	time_now = time.time()
	kit.motor1.throttle = 1.0
	time.sleep(.5)

	time_before = time.time()
	pos_before = pos
	time.sleep(5)
	time_now = time.time()
	pos_now = pos

	speed = ((pos_before - pos_now)/48)/(time_now - time_before)*math.pi*.0635

	speed = 1/speed * 100
	print("100m = " + str(speed))



	time_now = time.time()
	kit.motor1.throttle = .99
	time.sleep(.5)

	time_before = time.time()
	pos_before = pos
	time.sleep(5)
	time_now = time.time()
	pos_now = pos

	speed = ((pos_before - pos_now)/48)/(time_now - time_before)*math.pi*.0635

	speed = 1/speed * 100
	print("100m = " + str(speed))


	time_now = time.time()
	kit.motor1.throttle = .99
	time.sleep(.5)

	time_before = time.time()
	pos_before = pos
	time.sleep(5)
	time_now = time.time()
	pos_now = pos

	speed = ((pos_before - pos_now)/48)/(time_now - time_before)*math.pi*.0635

	speed = 1/speed * 100
	print("100m = " + str(speed))


	time_now = time.time()
	kit.motor1.throttle = .98
	time.sleep(.5)

	time_before = time.time()
	pos_before = pos
	time.sleep(5)
	time_now = time.time()
	pos_now = pos

	speed = ((pos_before - pos_now)/48)/(time_now - time_before)*math.pi*.0635

	speed = 1/speed * 100
	print("100m = " + str(speed))


	time_now = time.time()
	kit.motor1.throttle = .98
	time.sleep(.5)

	time_before = time.time()
	pos_before = pos
	time.sleep(5)
	time_now = time.time()
	pos_now = pos

	speed = ((pos_before - pos_now)/48)/(time_now - time_before)*math.pi*.0635

	speed = 1/speed * 100
	print("100m = " + str(speed))

	#kit.motor1.throttle = None
	#time.sleep(2)
	#kit.motor1.throttle = -1
	#time.sleep(1)
	#kit.motor1.throttle = 0

	time.sleep(1)

	kit.motor1.throttle = None

	decoder.cancel()

	pi.stop()





main()