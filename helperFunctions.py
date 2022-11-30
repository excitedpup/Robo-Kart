from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import random

hub = PrimeHub()
motors = MotorPair('C', 'D')
colorLeft = ColorSensor('A')
colorRight = ColorSensor('B')
matrix = hub.light_matrix
left_motor = Motor('C')
right_motor = Motor('D')

# If red is sensed by light sensor, the robot's
# default speed will go down by 1.5 times.
def redDetected():
    base = motors.get_default_speed()
    matrix.show_image('SAD')
    if base >= 20:
        motors.set_default_speed(int(base / 1.5))

# If green is sensed by light sensor, the robot's
# default speed will go up by 1.5 times.
def greenDetected():
    base = motors.get_default_speed()
    matrix.show_image('HAPPY')
    if base <= 60:
        motors.set_default_speed(int(base * 1.5))

# create '!' on matrix
def showCaution():
    hub.light_matrix.set_pixel(2, 0)
    hub.light_matrix.set_pixel(2, 1)
    hub.light_matrix.set_pixel(2, 2)
    hub.light_matrix.set_pixel(2, 4)

# If yellow is sensed by light sensor, the robot
# will lose traction for a quick rotation of the wheel
def yellowDetected():
    base = motors.get_default_speed()
    showCaution()
    if base <= 60:
        left_motor.run_for_rotations(0.25,base * 1)
        right_motor.run_for_rotations(0.25,base * -1)
        motors.set_default_speed(base)

# If violet is detected by the light sensor, a
# counter will be started and increased storing
# lap apon next violet sense.
def raceTimer():
    counter = 0
    lap1 = 0
    lap2 = 0
    lap3 = 0
    finish_time = 0
    while counter >= 3:
        if colorRight.get_color() == 'violet':
            if counter == 0:
                timer = Timer()
                matrix.write('1')
            elif counter == 1:
                lap1 = timer.now()
                matrix.write('2')
            elif counter == 2:
                lap2 = timer.now() - lap1
                matrix.write('3')
            elif counter == 3:
                finish_time = timer.now()
                lap3 = finish_time - lap1 - lap2
                matrix.show_image('FABULOUS')

            counter = counter + 1

# If blue is sensed by color sensor, the robot
# simulates hitting water and either hydroplaning
# or slowing down.
def waterHazard():
    base = motors.get_default_speed()
    #Goes at 3/4 current speed if going fast and half speed if going slow
    fast = False
    if base >= 35:
        motors.set_default_speed(int(base*(3/4)))
        fast = True
    else:
        motors.set_default_speed(int(base/2))
    #color will be changed to white from blue(testing purposes)
    while colorLeft.get_color() != 'blue' or colorRight.get_color() != 'blue':
        motors.start()

        #Boundry detected and if going fast "hits" the boundary, stops, and adjusts to get back on track
        if colorRight.get_color() == 'black':
            if fast:
                motors.stop()
                wait_for_seconds(1)
                turnLeft()
                motors.set_default_speed(int(base/2))
                fast = False
            else:
                turnLeft()
                motors.set_default_speed(int(base/2))
        elif colorLeft.get_color() == 'black':
            if fast:
                motors.stop()
                wait_for_seconds(2)
                turnRight()
                motors.set_default_speed(int(base/2))
                fast = False
            else:
                turnRight()
                motors.set_default_speed(int(base/2))
        #out of water, return to normal, same here will be changed to white from blue
        if colorRight.get_color() == 'blue' or colorLeft.get_color() == 'blue':
            break

    motors.set_default_speed(base)

def turnLeft():
    base = motors.get_default_speed()
    power = random.randint(int(base/4), int(base/2))
    motors.start_tank(base, base+power)

def turnRight():
    base = motors.get_default_speed()
    power = random.randint(int(base/4), int(base/2))
    motors.start_tank(base+power, base)
    

def waterHazardTest():
    motors.set_default_speed(30)
    while(True):
        motors.start()
        if(colorRight.get_color() == 'white' or colorLeft.get_color() == 'white'):
            waterHazard()

waterHazardTest()