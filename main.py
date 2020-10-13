#!/usr/bin/env pybricks-micropython
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

# Create your objects here.
ev3 = EV3Brick()


time.sleep(2)


# instructions to follow
#instructions = "uluLulldRlddrUUdRRuLLUlDrdLrrrRdrUUUluR"
instructions = "ullldlluRRRRRdrUUUluRRddldllllluRUrDldRRRdrUUruuRllDDD"

# function to pad instruction string
def convert_instructions(instr):
    instructions = instr
    instr_index = 1
    prev_instr = "s"
    while (instr_index < len(instructions)):
        curr_instr = instructions[instr_index]
        if (curr_instr.isupper() and curr_instr != prev_instr):
            instructions = instructions[:instr_index] + curr_instr.lower() + instructions[instr_index:]
            instr_index += 1
        
        prev_instr = curr_instr
        instr_index += 1
        
    return instructions

# pad the instruction string
instructions = convert_instructions(instructions)

#instructions = "udlrur"
# execute the given instructions
robot.execute_instr(instructions)



# 
# Experimenting with can pushing
#

# motors
# leftMotor = Motor(Port.A)
# rightMotor = Motor(Port.B)

# #vehicle = DriveBase(leftMotor, rightMotor, 56, 114)

# while ( not robot.are_both_black()):
#     robot.lineFollow(70)

# robot.robot.stop()

# # motor rotations
# rotations = 1.40
# calc_rotations = 360 * rotations
# #calc_rotations = 500

# leftMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
# rightMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
# time.sleep(6)

# leftMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
# rightMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
# time.sleep(6)

# while (not robot.are_both_black()):
#     robot.reverse_line_follow(60)
# robot.robot.stop()