#!/usr/bin/env python3


from adafruit_motorkit import MotorKit
import time
import math

import pigpio
import rotary_encoder

#def callback_R(way):
#	global pos_R

#	pos_R += way

#	print("pos_R={}".format(pos_R))

#def callback_L(way):
#	global pos_L

#	pos_L += way

#	print("pos_L={}".format(pos_L))


class DriveTrain:

	def callback_R(self, way):
		self.pos_R += way
		#print("pos_R={}".format(self.pos_R))


	def callback_L(self, way):
		self.pos_L += way
		#print("pos_L={}".format(self.pos_L))

	def __init__(self, encoderR_A, encoderR_B, encoderL_A, encoderL_B):
		print("Initializing...")
		self.pi = pigpio.pi()
		self.encoder_R = rotary_encoder.decoder(self.pi, encoderR_A, encoderR_B, self.callback_R)
		self.encoder_L = rotary_encoder.decoder(self.pi, encoderL_A, encoderL_B, self.callback_L)
		self.pos_L = 0
		self.pos_R = 0

		kit = MotorKit()
		self.motor_L = kit.motor1
		self.motor_R = kit.motor2

	def drive(self, throttle, dif):
		self.motor_R.throttle = throttle + dif
		self.motor_L.throttle = throttle - dif

	def shutdown(self):
		print("Shutting Down...")
		self.motor_L.throttle = None
		self.motor_R.throttle = None
		self.encoder_R.cancel()
		self.encoder_L.cancel()
		self.pi.stop()


if __name__ == '__main__':

	R_A = 5
	R_B = 6
	L_A = 22
	L_B = 23

	Rabbit = DriveTrain(R_A, R_B, L_A, L_B)

	Rabbit.drive(.70, .25)	
	time.sleep(2)

	Rabbit.shutdown()

