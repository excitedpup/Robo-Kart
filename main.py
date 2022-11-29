# This is our Main.py file containing our code
from spike import PrimeHub,ColorSensor, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer
from math import *

# Initialize
timer = Timer()

color_sensor_reactions = ColorSensor('E')
motor_pair = MotorPair('C','D')
hub = PrimeHub()

# not used yet
#color_sensor_track = ColorSensor('F')
# distance_sensor = DistanceSensor('B')
# left_motor = Motor('C')
# right_motor = Motor('D')

def beep(amount):
    for i in range(amount):
        hub.speaker.beep()

def wait(seconds):
    wait_for_seconds(seconds)

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

#get rgb calibration
def calibrateSensor(sensor):
    beep(2)
    # Put the color sensor directly above the red
    # Press left button
    hub.left_button.wait_until_pressed()
    wait(0.5)
    red = sensor.get_rgb_intensity()
    print(red)
    beep(1)
    # Put the color sensor directly above the green
    # Press left button
    hub.left_button.wait_until_pressed()
    wait(0.5)
    green = sensor.get_rgb_intensity()
    print(green)
    beep(1)
    # Put the color sensor directly above the yellow
    # Press left button
    hub.left_button.wait_until_pressed()
    wait(0.5)
    yellow = sensor.get_rgb_intensity()
    print(yellow)
    beep(1)
    # Put the color sensor directly above the blue
    # Press left button
    hub.left_button.wait_until_pressed()
    wait(0.5)
    blue = sensor.get_rgb_intensity()
    print(blue)
    beep(1)
    # Put the color sensor directly above the violet
    # Press left button
    hub.left_button.wait_until_pressed()
    wait(0.5)
    violet = sensor.get_rgb_intensity()
    print(violet)
    beep(1)
    # Put the color sensor directly above the black
    # Press left button
    hub.left_button.wait_until_pressed()
    wait(0.5)
    black = sensor.get_rgb_intensity()
    print(black)
    beep(1)
    # Put the color sensor directly above the white
    # Press left button
    hub.left_button.wait_until_pressed()
    wait(0.5)
    white = sensor.get_rgb_intensity()
    print(white)
    beep(1)
    beep(5)
    # How line follow was done - kept for reference in future
    #print(not_line)
    #avg = (line + not_line) / 2
    #print(int(avg))
    return red, green, yellow, blue, violet, black, white

def isColor(colorVal, getColor):
    if colorVal[0]-50 <= getColor[0] <= colorVal[0]+50:
        if colorVal[1]-50 <= getColor[1] <= colorVal[1]+50:
            if colorVal[2]-50 <= getColor[2] <= colorVal[2]+50:
                if colorVal[3]-50 <= getColor[3] <= colorVal[3]+50:
                    return True
    else:
        return False

def isYellow(colorVal, getColor):
    if colorVal[1]-50 <= getColor[1] <= colorVal[1]+75:
        if colorVal[2]-50 <= getColor[2] <= colorVal[2]+50:
            return True
    else:
        return False

def main(red, green, yellow, blue, violet, black, white, duration=20, midLight=50):
    timer.reset()
    beep(1)
    while (timer.now() < duration):
        #motor_pair.start(1)
        if isColor(red, color_sensor_reactions.get_rgb_intensity()):
            print("red")
            #wait(0.5)
        elif isColor(green, color_sensor_reactions.get_rgb_intensity()):
            print("green")
            #wait(0.5)
        elif isYellow(yellow, color_sensor_reactions.get_rgb_intensity()):
            print("yellow")
            #wait(0.5)
        elif isColor(blue, color_sensor_reactions.get_rgb_intensity()):
            print("blue")
            #wait(0.5)
        elif isColor(violet, color_sensor_reactions.get_rgb_intensity()):
            print("violet")
            #wait(0.5)
        elif isColor(black, color_sensor_reactions.get_rgb_intensity()):
            print("black")
            wait(0.5)
        else:
            print("white")
            #wait(0.5)
    
    #motor_pair.stop()


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

red, green, yellow, blue, violet, black, white = calibrateSensor(color_sensor_reactions)
main(red=red, green=green, yellow=yellow, blue=blue, violet=violet, black=black, white=white)