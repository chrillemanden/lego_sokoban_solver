from pybricks.hubs import EV3Brick
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time

# import our own modules
import robot
import fast_robot

# print the current forward velocity of the vehicle
# to the console to find the maximum speed of the vehicle
def find_max_forward_speed(speed):
    # motors
    leftMotor = Motor(Port.A)
    rightMotor = Motor(Port.B)

    # vehicle
    vehicle = DriveBase(leftMotor, rightMotor, 56, 114)

    while (True):
        vehicle.drive(speed, 0)
        distance, drive_speed, angle, turn_rate = vehicle.state()
        print(drive_speed)