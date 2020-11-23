#!/usr/bin/env python3


from adafruit_motorkit import MotorKit
import time
import math

import pigpio
import rotary_encoder

def callback_R(way):
	global pos_R

	pos_R += way

	print("pos={}".format(pos))

def callback_L(way):
	global pos_L

	pos_L += way

	print("pos={}".format(pos))


class DriveTrain:

	def __init__(self, encoderR_A, encoderR_B, encoderL_A, encoderL_B):
		self.pi = pigpio.pi()
		self.encoder_R = rotary_encoder.decoder(self.pi, encoderR_A, encoderR_B, callback_R)
		self.encoder_L = rotary_encoder.decoder(self.pi, encoderL_A, encoderL_B, callback_L)

		kit = MotorKit()
		self.motor_L = kit.motor1
		self.motor_R = kit.motor2


if __name__ == '__main__':

	Rabbit = DriveTrain(22, 23, 5, 6)
	
	Rabbit.motor_L.throttle = 1
	time.sleep(1)
	Rabbit.motor_L.throttle = None



	decoder.cancel()
	pi.stop()
