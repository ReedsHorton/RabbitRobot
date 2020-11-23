#!/usr/bin/env python3


from adafruit_motorkit import MotorKit
import time
import math

import pigpio
import rotary_encoder




class DriveTrain:

	def __init__(self, encoderR_A, encoderR_B, encoderL_A, encoderL_B):
		self.pi = pigpio.pi()
		self.encoder_R = rotary_encoder.decoder(self.pi, encoderR_A, encoderR_B, callback)
		self.encoder_L = rotary_encoder.decoder(self.pi, encoderL_A, encoderL_B, callback)

		kit = MotorKit()
		self.motor_L = kit.motor1
		self.motor_R = kit.motor2

		