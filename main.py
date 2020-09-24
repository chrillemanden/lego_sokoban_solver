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

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
#ev3.speaker.beep()

# reflection limit
reflection_limit = 20

# states for driving squares
turning = 0
forward = 1
state = forward

north = 0
south = 1
west = 2
east = 3

left = "l"
right = "r"
up = "u"
down = "d"

orient = north
init_instr = True
finished_instr = False

# motors
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)

# sensors
leftLineSensor = ColorSensor(Port.S4)
rightLineSensor = ColorSensor(Port.S1)

# vehicle

robot = DriveBase(leftMotor, rightMotor, 56, 114)

def are_both_black():
    #print("Right sensor: " + str(rightLineSensor.reflection()))
    #print("Left sensor: " + str(leftLineSensor.reflection()))
    if (rightLineSensor.reflection() < reflection_limit and leftLineSensor.reflection() < reflection_limit):
        #print("True")
        return True
        
    else:
        #print("False")
        return False


def left_black():
    if (leftLineSensor.reflection() < reflection_limit):
        return True
    else:
        return False

def right_black():
    if (rightLineSensor.reflection() < reflection_limit):
        return True
    else:
        return False

# def alwaysStraight():
#     if (rightLineSenor.reflection() < 20 and leftLineSensor.reflection() < 20):
#         #robot.drive(200, 0)
#         leftMotor.run(1000)
#         rightMotor.run(1000)
#     elif (rightLineSenor.reflection() < 20): #black is seen
#         #leftMotor.run()
        
#         # turn slightly left
#         #robot.drive(100, -40)
#         leftMotor.run(650)
#         rightMotor.run(1000)
#     elif(leftLineSensor.reflection() < 20): #black is seen

#         # turn slightly right
#         #robot.drive(100, 40)
#         leftMotor.run(1000)
#         rightMotor.run(650)

#     else:
#         #robot.drive(200, 0)
#         leftMotor.run(1000)
#         rightMotor.run(1000)

def lineFollow(speed):
    if (right_black()): #black is seen
        # turn slightly left
        robot.drive(speed, -0.4*speed)
    elif(left_black()): #black is seen
        # turn slightly right
        robot.drive(speed, 0.4*speed)
    else:
        robot.drive(speed, 0)

def grid_left_tank_turn():
    #first_black = False
    robot.drive(40, 0)
    time.sleep(1)
    while (not left_black()):
        robot.drive(20, 45)
    print("Found first black")
    while (not right_black()):
        robot.drive(20, 45)
    print("Found second black")


def grid_right_tank_turn():
    #first_black = False
    robot.drive(40, 0)
    time.sleep(1)
    while (not left_black()):
        robot.drive(20, -45)
    print("Found first black")
    while (not right_black()):
        robot.drive(20, -45)
    print("Found second black")
    time.sleep(0.5)

def driveSquare():
    lineFollow(50)
    if (are_both_black()):        
        grid_right_tank_turn()
        robot.stop()
        

def up_action():
    global orient
    global north
    global east
    global west
    global south
    global init_instr
    global finished_instr
    if (orient == north):
        if (init_instr):
            robot.drive(40, 0)
            time.sleep(1)
        while(not are_both_black()):
            lineFollow(50)
        finished_instr = True
    elif(orient == west):
        grid_right_tank_turn()
    elif(orient == east):
        grid_left_tank_turn()
    else:
        grid_left_tank_turn()
        grid_left_tank_turn()
    orient = north;
    init_instr = False

def down_action():
    global orient
    global north
    global east
    global west
    global south
    global init_instr
    global finished_instr
    if (orient == south):
        if (init_instr):
            robot.drive(40, 0)
            time.sleep(1)
        while(not are_both_black()):
            lineFollow(50)
        finished_instr = True
    elif(orient == east):
        grid_right_tank_turn()
    elif(orient == west):
        grid_left_tank_turn()
    else:
        grid_left_tank_turn()
        grid_left_tank_turn()
    
    orient = south;
    init_instr = False

def left_action():
    global orient
    global north
    global east
    global west
    global south
    global init_instr
    global finished_instr
    if (orient == west):
        if (init_instr):
            robot.drive(40, 0)
            time.sleep(1)
        while(not are_both_black()):
            lineFollow(50)
        finished_instr = True
    elif(orient == north):
        grid_left_tank_turn()
    elif(orient == south):
        grid_right_tank_turn()
    else:
        grid_left_tank_turn()
        grid_left_tank_turn()
    
    orient = west;
    init_instr = False

def right_action():
    global orient
    global north
    global east
    global west
    global south
    global init_instr
    global finished_instr
    if (orient == east):
        if (init_instr):
            robot.drive(40, 0)
            time.sleep(1)
        while(not are_both_black()):
            lineFollow(50)
        finished_instr = True
    elif(orient == south):
        grid_left_tank_turn()
    elif(orient == north):
        grid_right_tank_turn()
    else:
        grid_left_tank_turn()
        grid_left_tank_turn()
    
    orient = east;
        
        

time.sleep(2)
counter = 0

instructions = "urrrrdlullld"
instr_index = 0

while (True):
    if (instr_index >= len(instructions)):
        robot.stop()
        brick.display.clear()
        brick.display.text("Finished", (60, 50))
        while (True):
            counter = 0
    else:
        curr_instr = instructions[instr_index]
        print("current instruction: " + str(curr_instr))
        init_instr = True
        while (not finished_instr):
            if (curr_instr == up):
                up_action()
            elif (curr_instr == down):
                down_action()
            elif (curr_instr == left):
                left_action()
            elif (curr_instr == right):
                right_action()
            else:
                robot.stop()
                brick.display.clear()
                brick.display.text("Invalid instruction", (60, 50))

        # increment the pointer
        instr_index += 1
        finished_instr = False
    
    
    # while (not are_both_black()):
    #     lineFollow(50)
    # grid_left_tank_turn()
    # robot.stop()
    # while True:
    #     counter = 0
    

    
        

    #print("Right sensor: " + str(rightLineSensor.reflection()))
    #print("Left sensor: " + str(leftLineSensor.reflection()))
    #time.sleep(1)
    #are_both_black()
        # state = turning
        # # Clear the display
        # 
        # # Print ``Hello`` near the middle of the screen
        # brick.display.text("Double Black", (60, 50))
        # robot.stop()
        # while (True):
        #     state = turning
