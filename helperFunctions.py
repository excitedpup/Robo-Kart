from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()
motors = MotorPair('C', 'D')
color = LightSensor('B')
matrix = hub.light_matrix

# If red is sensed by light sensor, the robot's
# default speed will go down by 1.5 times.
def redDetected():
    base = motors.get_default_speed()
    matrix.show_image('SAD')
    if base >= 20:
        motors.set_default_speed(base / 1.5)

# If green is sensed by light sensor, the robot's
# default speed will go up by 1.5 times.
def greenDetected():
    base = motors.get_default_speed()
    matrix.show_image('HAPPY')
    if base <= 60:
        motors.set_default_speed(base * 1.5)

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
        if color.get_color() == 'violet':
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
                print(f"Finish Time: {finish_time}\n - Lap 1: {lap1}\n - Lap 2: {lap2}\n - Lap 3: {lap3}")
            counter = counter + 1

# If blue is sensed by color sensor, the robot
# simulates hitting water and either hydroplaning
# or slowing down.
def waterHazard():
    base = motors.get_default_speed()
    while color.get_color() == 'blue':
        if base >= 35:
            motors.start()
        else:
            motors.set_default_speed(base/2)
    motors.set_default_speed(base)   