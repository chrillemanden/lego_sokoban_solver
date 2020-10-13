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

# motors
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)

# vehicle
vehicle = DriveBase(leftMotor, rightMotor, 56, 114)

# print the current forward velocity of the vehicle
# to the console to find the maximum speed of the vehicle
def find_max_forward_speed(speed):
    while (True):
        vehicle.drive(speed, 0)
        distance, drive_speed, angle, turn_rate = vehicle.state()
        print(drive_speed)

def test_cross_detection_at_speed(speed, n_crosses_to_pass, robot_name):
    
    print("Test of Cross Detection at a Given Speed")
    print("----------------------------------------")
    print("Robot: " + robot_name)
    print("Target Speed: " + str(speed))
    print("Target Crosses to pass: " + str(n_crosses_to_pass))
    print("")
    cross_counter = 0
    n_blacks = 0
    total_blacks = 0
    at_cross = False
    while (True):
        vehicle.drive(speed, 0)
        if (at_cross):
            if (robot.are_both_black()):
                n_blacks += 1
                total_blacks += 1
            else:
                at_cross = False
                cross_counter += 1
                print ("New cross -- Number of detected blacks in this cross: " + str(n_blacks))
                n_blacks = 0
        else:
            if (robot.are_both_black()):
                at_cross = True
                
        
        if (cross_counter >= n_crosses_to_pass):
            vehicle.stop()
            print ("")
            print ("Done!")
            print ("Passed " + str(cross_counter) + " crosses.")
            print ("Found a total of " + str(total_blacks) + " blacks.")
            break
        


            

        