from pybricks.hubs import EV3Brick
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time 

# reflection limit
reflection_limit = 20

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
junction_black = False

# motor rotations
rotations = 1.40
calc_rotations = 360 * rotations

# motors
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)

# sensors
leftLineSensor = ColorSensor(Port.S4)
rightLineSensor = ColorSensor(Port.S1)

# vehicle

robot = DriveBase(leftMotor, rightMotor, 56, 114)

# returns whether or not both sensors see black 
def are_both_black():
    if (rightLineSensor.reflection() < reflection_limit and leftLineSensor.reflection() < reflection_limit):
        return True
    else:
        return False

# returns whether or not a junction has been passed
def is_junction():
    global junction_black
    if (junction_black):
        if (not are_both_black()):
            junction_black = False
            return True
    else:
        if (are_both_black()):
            junction_black = True

# does the left sensor show black
def left_black():
    if (leftLineSensor.reflection() < reflection_limit):
        return True
    else:
        return False

# does the right sensor show black
def right_black():
    if (rightLineSensor.reflection() < reflection_limit):
        return True
    else:
        return False

# follow the line keeping both colour sensors on the white patch 
# and the black line in between
def lineFollow(speed):
    if (right_black()): #black is seen
        # turn slightly left
        robot.drive(speed, -0.4*speed)
    elif(left_black()): #black is seen
        # turn slightly right
        robot.drive(speed, 0.4*speed)
    else:
        robot.drive(speed, 0)

def reverse_line_follow(speed):
    if (right_black()):
        # turn slightly right
        robot.drive(-speed, -0.4*speed)
    elif(left_black()):
        #turn slightly left
        robot.drive(-speed, 0.4*speed)
    else:
        robot.drive(-speed, 0)

# turn the vehicle 90 degrees anticlockwise
def grid_left_tank_turn():
    robot.drive(40, 0)
    time.sleep(1)
    while (not left_black()):
        robot.drive(20, 45)
    while (not right_black()):
        robot.drive(20, 45)

# turn the vehicle 90 degrees clockwise
def grid_right_tank_turn():
    robot.drive(40, 0)
    time.sleep(1)
    while (not right_black()):
        robot.drive(20, -45)
    while (not left_black()):
        robot.drive(20, -45)

# turn the vehicle 180 degrees
def grid_180_turn():
    robot.stop()
    leftMotor.run_angle(-100, 180, Stop.COAST, False)
    rightMotor.run_angle(100, 180, Stop.COAST, False)
    time.sleep(2)
    while (not right_black()):
        leftMotor.run_angle(-100, 5, Stop.COAST, False)
        rightMotor.run_angle(100, 5, Stop.COAST, False)
        time.sleep(0.1)
    while (not left_black()):
        leftMotor.run_angle(-100, 5, Stop.COAST, False)
        rightMotor.run_angle(100, 5, Stop.COAST, False)
        time.sleep(0.1)

    
# drive around in a square of four close junctions
def driveSquare():
    lineFollow(50)
    if (are_both_black()):        
        grid_right_tank_turn()
        robot.stop()   

# move one UP on the grid
def up_action(deliver_can):
    global orient
    global init_instr
    global finished_instr
    global calc_rotations
    if (orient == north):
        if (deliver_can):
            robot.stop()
            # drive forward with the can
            leftMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
            rightMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
            time.sleep(6)
            # drive backwards with the can
            leftMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
            rightMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
            time.sleep(6)
        elif (init_instr):
            robot.drive(40, 0)
            time.sleep(1)
        while(not are_both_black() and not deliver_can):
            lineFollow(50)
        finished_instr = True
    elif(orient == west):
        grid_right_tank_turn()
    elif(orient == east):
        grid_left_tank_turn()
    else:
        grid_180_turn()

    orient = north
    init_instr = False

# move one DOWN on the grid
def down_action(deliver_can):
    global orient
    global init_instr
    global finished_instr
    global calc_rotations
    if (orient == south):
        if (deliver_can):
            robot.stop()
            # drive forward with the can
            leftMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
            rightMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
            time.sleep(6)
            # drive backwards with the can
            leftMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
            rightMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
            time.sleep(6)
        elif (init_instr):
            robot.drive(40, 0)
            time.sleep(1)
        while(not are_both_black() and not deliver_can):
            lineFollow(50)
        finished_instr = True
    elif(orient == east):
        grid_right_tank_turn()
    elif(orient == west):
        grid_left_tank_turn()
    else:
        grid_180_turn()
    
    orient = south
    init_instr = False

# move one LEFT on the grid
def left_action(deliver_can):
    global orient
    global init_instr
    global finished_instr
    global calc_rotations
    if (orient == west):
        if (deliver_can):
            robot.stop()
            # drive forward with the can
            leftMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
            rightMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
            time.sleep(6)
            # drive backwards with the can
            leftMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
            rightMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
            time.sleep(6)
        elif (init_instr):
            robot.drive(40, 0)
            time.sleep(1)
        while(not are_both_black() and not deliver_can):
            lineFollow(50)
        finished_instr = True
    elif(orient == north):
        grid_left_tank_turn()
    elif(orient == south):
        grid_right_tank_turn()
    else:
        grid_180_turn()
    
    orient = west
    init_instr = False

# move one RIGHT on the grid
def right_action(deliver_can):
    global orient
    global init_instr
    global finished_instr
    global calc_rotations
    if (orient == east):
        if (deliver_can):
            robot.stop()
            # drive forward with the can
            leftMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
            rightMotor.run_angle(100, calc_rotations, Stop.BRAKE, False)
            time.sleep(6)
            # drive backwards with the can
            leftMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
            rightMotor.run_angle(-100, calc_rotations, Stop.BRAKE, False)
            time.sleep(6)
        elif (init_instr):
            robot.drive(40, 0)
            time.sleep(1)            
        while(not are_both_black() and not deliver_can):
            lineFollow(50)
        finished_instr = True
    elif(orient == south):
        grid_left_tank_turn()
    elif(orient == north):
        grid_right_tank_turn()
    else:
        grid_180_turn()
    
    orient = east
    init_instr = False

# execute a string of grid-instructions for the robot to follow
def execute_instr(instr):
    global init_instr
    global finished_instr

    # insert f to indicate that is finished at the end
    instructions = instr + "f"

    instr_index = 0
    while(True):
        if (instr_index >= len(instructions) -1):
            robot.stop()
            brick.display.clear()
            brick.display.text("Finished", (60, 50))
            break
            while (True):
                instr_index = 0
        else:
            curr_instr = instructions[instr_index]
            next_instr = instructions[instr_index+1]
            print("current instruction: " + str(curr_instr))
            init_instr = True
            deliver_can = False
            if (curr_instr.isupper() and next_instr.islower()):
                deliver_can = True
            curr_instr = curr_instr.lower() 
            while (not finished_instr):
                if (curr_instr == up):
                    up_action(deliver_can)
                elif (curr_instr == down):
                    down_action(deliver_can)
                elif (curr_instr == left):
                    left_action(deliver_can)
                elif (curr_instr == right):
                    right_action(deliver_can)
                else:
                    robot.stop()
                    brick.display.clear()
                    brick.display.text("Invalid instruction", (60, 50))

            # increment the pointer
            instr_index += 1
            finished_instr = False


# class SlowRobot():
#     """
#     docstring
#     """
#     def __init__(self):
#         super(SlowRobot, self).__init__()
#         #self.orient = orientation



#         # motors
#         leftMotor = Motor(Port.A)
#         rightMotor = Motor(Port.B)
        
#         #vehicle
#         self.vehicle = DriveBase(leftMotor, rightMotor, 56, 114)

#         # sensors
#         self.leftLineSensor = ColorSensor(Port.S4)
#         self.rightLineSensor = ColorSensor(Port.S1)

#         # states
#         self.junction_black = False
#         self.orient = north
#         self.init_instr = True
#         self.finished_instr = False

#     # class functions

#     # returns whether or not both sensors see black 
#     def are_both_black():
#         #print("Right sensor: " + str(rightLineSensor.reflection()))
#         #print("Left sensor: " + str(leftLineSensor.reflection()))
#         if (self.rightLineSensor.reflection() < reflection_limit and self.leftLineSensor.reflection() < reflection_limit):
#             return True
#         else:
#             return False

    # returns whether or not a junction has been passed
    def is_junction():
        if (self.junction_black):
            if (not are_both_black()):
                self.junction_black = False
                return True
        else:
            if (are_both_black()):
                self.junction_black = True
            
#     # does the left sensor show black
#     def left_black():
#         if (self.leftLineSensor.reflection() < reflection_limit):
#             return True
#         else:
#             return False

#     # does the right sensor show black
#     def right_black():
#         if (self.rightLineSensor.reflection() < reflection_limit):
#             return True
#         else:
#             return False

#     # follow the line keeping both colour sensors on the white patch and the black line in between
#     def lineFollow(self, speed):
#         if (right_black()): #black is seen
#             # turn slightly left
#             self.vehicle.drive(speed, -0.4*speed)
#         elif(left_black()): #black is seen
#             # turn slightly right
#             self.vehicle.drive(speed, 0.4*speed)
#         else:
#             self.vehicle.drive(speed, 0)

#     # turn the vehicle 90 degrees anticlockwise
#     def grid_left_tank_turn():
#         self.vehicle.drive(40, 0)
#         time.sleep(1)
#         while (not left_black()):
#             self.vehicle.drive(20, 45)
#         while (not right_black()):
#             self.vehicle.drive(20, 45)

#     # turn the vehicle 90 degrees clockwise
#     def grid_right_tank_turn():
#         self.vehicle.drive(40, 0)
#         time.sleep(1)
#         while (not right_black()): 
#             self.vehicle.drive(20, -45)
#         while (not left_black()):
#             self.vehicle.drive(20, -45)

#     # move one UP on the grid
#     def up_action(self):
#         if (self.orient == north):
#             if (self.init_instr):
#                 self.vehicle.drive(40, 0)
#                 time.sleep(1)
#             while(not are_both_black()):
#                 lineFollow(50)
#             self.finished_instr = True
#         elif(self.orient == west):
#             grid_right_tank_turn()
#         elif(self.orient == east):
#             grid_left_tank_turn()
#         else:
#             grid_left_tank_turn()
#             grid_left_tank_turn()
#         self.orient = north;
#         self.init_instr = False

#     # move one DOWN on the grid
#     def down_action():
#         if (self.orient == south):
#             if (self.init_instr):
#                 self.vehicle.drive(40, 0)
#                 time.sleep(1)
#             while(not are_both_black()):
#                 lineFollow(50)
#             self.finished_instr = True
#         elif(orient == east):
#             grid_right_tank_turn()
#         elif(orient == west):
#             grid_left_tank_turn()
#         else:
#             grid_left_tank_turn()
#             grid_left_tank_turn()
        
#         self.orient = south
#         self.init_instr = False

#     # move one LEFT on the grid
#     def left_action():
#         if (self.orient == west):
#             if (self.init_instr):
#                 self.vehicle.drive(40, 0)
#                 time.sleep(1)
#             while(not are_both_black()):
#                 lineFollow(50)
#             self.finished_instr = True
#         elif(orient == north):
#             grid_left_tank_turn()
#         elif(orient == south):
#             grid_right_tank_turn()
#         else:
#             grid_left_tank_turn()
#             grid_left_tank_turn()
        
#         self.orient = west
#         self.init_instr = False

#     # move one RIGHT on the grid
#     def right_action():
#         if (self.orient == east):
#             if (self.init_instr):
#                 self.vehicle.drive(40, 0)
#                 time.sleep(1)
#             while(not are_both_black()):
#                 lineFollow(50)
#             self.finished_instr = True
#         elif(orient == south):
#             grid_left_tank_turn()
#         elif(orient == north):
#             grid_right_tank_turn()
#         else:
#             grid_left_tank_turn()
#             grid_left_tank_turn()
        
#         self.orient = east
#         self.init_instr = False

#     # drive the robot around in a square. Gimmick!
#     # def driveSquare(self):
#     #     lineFollow(50)
#     #     if (are_both_black()):        
#     #         grid_right_tank_turn()
#     #         robot.stop()


#     # execute a string of grid-instructions for the robot to follow
#     def execute(self, instructions):
          
#         instr_index = 0
#         while(True):
#             if (instr_index >= len(instructions)):
#                 self.vehicle.stop()
#                 brick.display.clear()
#                 brick.display.text("Finished", (60, 50))
#                 while (True):
#                     counter = 0
#             else:
#                 curr_instr = instructions[instr_index]
#                 print("current instruction: " + str(curr_instr))
#                 self.init_instr = True
#                 while (not self.finished_instr):
#                     if (curr_instr == up):
#                         self.up_action()
#                     elif (curr_instr == down):
#                         self.down_action()
#                     elif (curr_instr == left):
#                         self.left_action()
#                     elif (curr_instr == right):
#                         self.right_action()
#                     else:
#                         counter = 0
#                         self.vehicle.stop()
#                         brick.display.clear()
#                         brick.display.text("Invalid instruction", (60, 50))

#                 # increment the pointer
#                 instr_index += 1
#                 self.finished_instr = False

    