from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()
motors = MotorPair('C', 'D')
color = ColorSensor('B')
matrix = hub.light_matrix
left_motor = Motor('C')
right_motor = Motor('D')

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
        
# create '!' on matrix
def showCaution():
    hub.light_matrix.set_pixel(2, 0)
    hub.light_matrix.set_pixel(2, 1)
    hub.light_matrix.set_pixel(2, 2)
    hub.light_matrix.set_pixel(2, 4)
            
# If yellow is sensed by light sensor, the robot's
# default speed will go up by 1.5 times.
def yellowDetected():
    base = motors.get_default_speed()
    showCaution()
    if base <= 60:
        left_motor.run_for_rotations(0.25,base * 1)
        right_motor.run_for_rotations(0.25,base * -1)
        motors.set_default_speed(base)

# If violet is detected by the light sensor, a 
# counter will be started and increased storing 
# lap upon next violet sense.
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
    
#Line Follow
#Assumes the midLight value is halfway between the reflections of “line” and “not line” to follow a line for duration seconds, and then stops.
"""
def lineFollow(duration=15, midLight=50):
    timer.reset()
    beep(1)
    while (timer.now() < duration):
        if color_sensor_track.get_reflected_light() < midLight:
            #follow on outside. try to stay in midlight
            right_motor.stop()
            left_motor.set_default_speed(-30)
            left_motor.start()
        elif color_sensor_track.get_reflected_light() > midLight:
            left_motor.stop()
            right_motor.set_default_speed(30)
            right_motor.start()
        else:
            motor_pair.set_default_speed(30)
            motor_pair.start()
    left_motor.stop()
    right_motor.stop()
    motor_pair.stop()

    # Present each colored brick to the Color Sensor and observe what happens; it will detect each color for 2 seconds
    while timer.now() < 2:
        color = color_sensor_reactions.wait_for_new_color()
        if color == 'blue':
            left_motor.run_for_rotations(1)
        elif color == 'yellow':
            right_motor.run_for_rotations(1)
"""
"""

    # This will use the reflected value of the colors to set the motor speed (yellow is approximately 80% and violet 60%)
while True:
    color = color_sensor_reactions.wait_for_new_color()
    percentage = color_sensor_reactions.get_reflected_light()
    if color == 'blue':
        motor_pair.run_for_rotations(1, percentage)
    elif color == 'yellow':
        while timer.now() < 2:
            motor_pair.set_default_speed(75)
"""
"""
def reset_speed():
    motor_pair.set_default_speed(50)

#oreientation sensor program
while True:
    orientation = hub.motion_sensor.wait_for_new_orientation()
    angle = abs(hub.motion_sensor.get_pitch_angle()) * 2
    #Shows happy brighter depending on posistion
    hub.light_matrix.show_image('HAPPY', angle)


    if orientation == 'front':
        hub.light_matrix.show_image('ASLEEP')
        app.start_sound('Snoring')
    elif orientation == 'up':
        hub.light_matrix.show_image('HAPPY')
        app.start_sound('Triumph')

"""

#Force Push Hover
# Use force sensor to go
"""
# Kept for reference
def hover(distance=30, duration=15):
    timer.reset()
    beep(1)
    while (timer.now() <= duration):
        if (distance_sensor.get_distance_cm() == None) or (distance_sensor.get_distance_cm() >= distance):
            motor_pair.set_default_speed(20)
            motor_pair.start()
        else:
            motor_pair.set_default_speed(-20)
            motor_pair.start()
    wait(0.5)
    motor_pair.stop()
    wait(0.1)
    beep(2)
"""