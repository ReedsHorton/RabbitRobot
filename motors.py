#!/usr/bin/env python3

from adafruit_motorkit import MotorKit
import time
import math

import pigpio
import rotary_encoder


class DriveTrain:

	def callback_R(self, way):
		self.pos_R += way
		if self.pos_R % 48 == 0:
			time_now = time.time()
			time_diff = time_now - self.prev_time_R
			self.prev_time_R = time_now
			self.speed_R = 1/((48/48)/time_diff*math.pi*.063) * 100 #48 ticks per rotation, 2.5" (.063m) diamater
		#print("pos_R={}".format(self.pos_R))
			print("Speed_R={}".format(self.speed_R))


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

		self.prev_time_R = time.time()
		self.prev_time_L = time.time()
		self.speed_R = 0
		self.speed_L = 0

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

	Rabbit.drive(.70, .3)	
	time.sleep(10)

	Rabbit.shutdown()

