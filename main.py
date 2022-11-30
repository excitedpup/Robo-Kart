# This is our Main.py file containing our code
from spike import PrimeHub,ColorSensor, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer
from math import *

# Initialize
timer = Timer()
redtime = Timer()
greentime = Timer()
color_sensor_reactions = ColorSensor('E')
motor_pair = MotorPair('C','D')
hub = PrimeHub()
matrix = hub.light_matrix
left_motor = Motor('C')
right_motor = Motor('D')

def beep(amount):
    for i in range(amount):
        hub.speaker.beep()

def wait(seconds):
    wait_for_seconds(seconds)
    

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

# If red is sensed by light sensor, the robot's
# default speed will go down by 1.5 times.
def redDetected():
    redtime.reset()
    beep(1)
    base = motor_pair.get_default_speed()
    while (redtime.now() < 2):
        matrix.show_image('SAD')
        #!!!!!!!!!!having issues updating spped!!!!!!!!!!!!
        #motor_pair.set_default_speed(1)
        #motor_pair.set_default_speed(int(base / 1.5))
        motor_pair.start(0)
    motor_pair.set_default_speed(base)

# If green is sensed by light sensor, the robot's
# default speed will go up by 1.5 times.
def greenDetected():
    greentime.reset()
    beep(1)
    base = motor_pair.get_default_speed()
    while (greentime.now() < 2):
        matrix.show_image('HAPPY')
        #!!!!!!!!!!having issues updating spped!!!!!!!!!!!!
        #motor_pair.set_default_speed(3)
        #motor_pair.set_default_speed(int(base * 1.5))
        motor_pair.start(4)
    motor_pair.set_default_speed(base)

# create '!' on matrix
def showCaution():
    hub.light_matrix.set_pixel(2, 0)
    hub.light_matrix.set_pixel(2, 1)
    hub.light_matrix.set_pixel(2, 2)
    hub.light_matrix.set_pixel(2, 4)

# If yellow is sensed by light sensor, the robot's
# default speed will go up by 1.5 times.
def yellowDetected():
    base = motor_pair.get_default_speed()
    showCaution()
    #!!!!!!!!!!Need to make rotation a little faster and wider!!!!!!!!!!!!
    left_motor.run_for_rotations(0.25,base*-2)
    right_motor.run_for_rotations(0.25,base*2)
    motor_pair.set_default_speed(base)

def isColor(colorVal, getColor, numRange):
    if colorVal[0]-numRange <= getColor[0] <= colorVal[0]+numRange:
        if colorVal[1]-numRange <= getColor[1] <= colorVal[1]+numRange:
            if colorVal[2]-numRange <= getColor[2] <= colorVal[2]+numRange:
                if colorVal[3]-numRange <= getColor[3] <= colorVal[3]+numRange:
                    return True
    else:
        return False

def isYellow(colorVal, getColor, numRange):
    if colorVal[1]-numRange <= getColor[1] <= colorVal[1]+numRange:
        if colorVal[2]-numRange <= getColor[2] <= colorVal[2]+numRange:
            return True
    else:
        return False

def main(red, green, yellow, blue, violet, black, white, duration=10, midLight=50):
    timer.reset()
    beep(1)
    while (timer.now() < duration):
        motor_pair.start(2)
        if isColor(red, color_sensor_reactions.get_rgb_intensity(), 80):
            print("red")
            redDetected()
            #wait(0.1)
        elif isColor(green, color_sensor_reactions.get_rgb_intensity(), 80):
            print("green")
            greenDetected()
            #wait(0.1)
        elif isYellow(yellow, color_sensor_reactions.get_rgb_intensity(), 80):
            print("yellow")
            yellowDetected()
            #wait(0.1)
        elif isColor(blue, color_sensor_reactions.get_rgb_intensity(), 80):
            print("blue")
            wait(0.1)
        elif isColor(violet, color_sensor_reactions.get_rgb_intensity(), 60):
            print("violet")
            wait(0.1)
        elif isColor(black, color_sensor_reactions.get_rgb_intensity(), 40):
            print("black")
            wait(0.1)
        else:
            print("white")
            wait(0.1)
    
    motor_pair.stop()

red, green, yellow, blue, violet, black, white = calibrateSensor(color_sensor_reactions)
main(red=red, green=green, yellow=yellow, blue=blue, violet=violet, black=black, white=white)
