# This is the file we have to copy/paste into Spike Prime
# This is our Main.py file containing our code
from spike import PrimeHub,ColorSensor, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer
from math import *
import random

# Initialize
timer = Timer()
racetimer = Timer()
colorLeft = ColorSensor('A')
colorRight = ColorSensor('B')
motor_pair = MotorPair('C','D')
hub = PrimeHub()
matrix = hub.light_matrix
left_motor = Motor('C')
right_motor = Motor('D')
distance_sensor =DistanceSensor('F')


counter = 0
lap1 = 0
lap2 = 0
lap3 = 0
colorStatus = False
colorTime = 0


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
    return red, green, yellow, blue, violet, black, white

# If red is sensed by light sensor, the robot's
# default speed will go down by 1.5 times.
def redDetected():
    base = motor_pair.get_default_speed()
    matrix.show_image('SAD')
    motor_pair.start(steering=0, speed=int(base/1.5))

# If green is sensed by light sensor, the robot's
# default speed will go up by 1.5 times.
def greenDetected():
    base = motor_pair.get_default_speed()
    matrix.show_image('ARROW_N')
    motor_pair.start(steering=0, speed=int(base *1.5))

# create '!' on matrix
def showCaution():
    hub.light_matrix.set_pixel(2, 0)
    hub.light_matrix.set_pixel(2, 1)
    hub.light_matrix.set_pixel(2, 2)
    hub.light_matrix.set_pixel(2, 4)

# If yellow is sensed by light sensor, the robot's
# default speed will go up by 1.5 times.
def yellowDetected(duration, direction, pause):
    base = motor_pair.get_default_speed()
    showCaution()
    for _ in range(duration):
        left_motor.start(-(direction))
        wait(pause)
        left_motor.stop()
        right_motor.start(direction)
        wait(pause)
        right_motor.stop()
    motor_pair.start(steering=0, speed=base)
    hub.light_matrix.off()

# If blue is detected, simulate the robot going into a puddle and either hydroplaning if going fast
# or heavily slowing down if going slow
def blueDetected(base):
    #Goes at 3/4 current speed if going fast and half speed if going slow
    fast = False
    waterSpeed = 0
    if base >= 35:
        waterSpeed = int(base * 3/4)
        fast = True
    else:
        waterSpeed = int(base/2)

    while colorRight.get_color() != 'white' or colorLeft.get_color() != 'white':
        #Boundry detected and if going fast "hits" the boundary, stops, and adjusts to get back on track
        if colorRight.get_color() == 'black':
            if fast:
                motor_pair.stop()
                wait_for_seconds(2)
                turnRight(base)
                waterSpeed = int(base/2)
                fast = False
            else:
                turnLeft(base)
                motor_pair.start(steering=0, speed=int(base/2))
        elif colorLeft.get_color() == 'black':
            if fast:
                motor_pair.stop()
                wait_for_seconds(2)
                turnRight(base)
                waterSpeed = int(base/2)
                fast = False
            else:
                turnLeft(base)
                motor_pair.start(steering=0, speed=int(base/2))
        else:
            motor_pair.start(steering=0, speed=waterSpeed)

    motor_pair.set_default_speed(35)

# If violet is detected by the light sensor, a
# counter will be started and increased storing
# lap upon next violet sense.
def raceTimer(time):

    global counter
    global lap1
    global lap2
    global lap3

    if counter == 0:
        lap1 = time
        print('lap1')
        print(lap1)
    elif counter == 1:
        lap2 = time - lap1
        print('lap1')
        print(lap1)
        print('lap2')
        print(lap2)
    elif counter == 2:
        lap3 = time - lap1 - lap2
        print('lap1')
        print(lap1)
        print('lap2')
        print(lap2)
        print('lap3')
        print(lap3)
    elif counter == 3:
        print("more than 3 laps")

# force sensor should try to avoid object when sensing them ahead of it
def isObstacle(distance=20):
    base = motor_pair.get_default_speed()

    left_motor.start(-(100))
    wait(0.3)    # Might have to switch these values
    left_motor.stop()
    motor_pair.start(steering=0, speed=base)
    wait(0.4)
    motor_pair.stop()
    right_motor.start(50)
    wait(0.5)# Might have to switch these values
    right_motor.stop()
    motor_pair.start(steering=0, speed=base)

def isColor(colorVal, getColor, numRange):
    if colorVal[0]-numRange <= getColor[0] <= colorVal[0]+numRange:
        if colorVal[1]-numRange <= getColor[1] <= colorVal[1]+numRange:
            if colorVal[2]-numRange <= getColor[2] <= colorVal[2]+numRange:
                if colorVal[3]-numRange <= getColor[3] <= colorVal[3]+numRange:
                    return True
    else:
        return False

def turnRight(base = 50):
    steer = random.randint(80,90)
    while colorLeft.get_color() == 'black':
        motor_pair.start(steering=steer, speed=base)
        wait(.3)
    motor_pair.start(steering=0, speed=35)

def turnLeft(base = 50):
    steer = -(random.randint(80,90))
    while colorRight.get_color() == 'black':
        motor_pair.start(steering=steer, speed=base)
        wait(.3)
    motor_pair.start(steering=0, speed=35)

# The variants of the first and last values in the range were too drastic to properly
# detect, this function just allows for the simpler detection of yellow.
def isYellow(colorVal, getColor, numRange):
    if colorVal[1]-numRange <= getColor[1] <= colorVal[1]+numRange:
        if colorVal[2]-numRange <= getColor[2] <= colorVal[2]+numRange:
            return True
    else:
        return False

def main(red, green, yellow, blue, violet, black, white, duration=15):
    timer.reset()
    racetimer.reset()
    print(racetimer.now())
    beep(1)
    base = motor_pair.set_default_speed(35)
    motor_pair.start(steering=0, speed=base)

    global counter
    global lap1
    global lap2
    global lap3
    global colorStatus
    global colorTime
    currentSpeed = 35
    fastestLap = 0
    base = 35
    violetStatus = False
    violetTime = 0

    while (timer.now() < duration):
        tempDist = distance_sensor.get_distance_cm()
        if tempDist is not None:
            if tempDist <= 30:
                isObstacle(30)

        if not colorStatus:
            motor_pair.start(steering=0, speed=base)
            if isColor(red, colorLeft.get_rgb_intensity(), 80) or isColor(red, colorRight.get_rgb_intensity(), 80):
                print("red")
                colorStatus = True
                colorTime = timer.now() + 2
                currentSpeed = int(base / 2)
                redDetected()
            elif isColor(green, colorLeft.get_rgb_intensity(), 30) or isColor(green, colorRight.get_rgb_intensity(), 30):
                print("green")
                colorStatus = True
                colorTime = timer.now() + 2
                currentSpeed = int(base * 1.5)
                greenDetected()
            elif isYellow(yellow, colorLeft.get_rgb_intensity(), 80) or isYellow(yellow, colorRight.get_rgb_intensity(), 80):
                print("yellow")
                yellowDetected(2, 100, .1)
        else:
            if colorTime < timer.now():
                currentSpeed = 35
                colorStatus = False
                hub.light_matrix.off()

        if isColor(blue, colorLeft.get_rgb_intensity(), 30) or isColor(blue, colorRight.get_rgb_intensity(), 30):
                print("blue")
                blueDetected(currentSpeed)

        if not violetStatus:
            if isColor(violet, colorLeft.get_rgb_intensity(), 30) or isColor(violet, colorRight.get_rgb_intensity(), 30):
                print("violet")
                #print(racetimer.now())
                # fastestLap declaration here can be taken out I think!!!
                fastestLap = raceTimer(racetimer.now())
                counter = counter + 1
                violetTime = timer.now()+10
                violetStatus=True
        else:
            if violetTime < timer.now():
                violetStatus=False

        if isColor(black, colorLeft.get_rgb_intensity(), 40):
            turnRight()
            print("black")
        elif isColor(black, colorRight.get_rgb_intensity(), 40):
            turnLeft()
            print("black")

    motor_pair.stop()
    if lap1<lap2 and lap1<lap2:
        fastestLap = lap1
    elif lap2<lap1 and lap2<lap3:
        fastestLap = lap2
    else:
        fastestLap = lap3
    print('Fastest Lap is:')
    print(fastestLap)

#red, green, yellow, blue, violet, black, white = calibrateSensor(colorLeft)
red = (352, 87, 130, 455)
green =  (143, 217, 141, 380)
yellow = (627, 535, 311, 992)
blue = (83, 166, 281, 353)
violet = (77, 71, 126, 193)
black = (47, 48, 48, 106)
white = (624, 622, 604, 989)
main(red=red, green=green, yellow=yellow, blue=blue, violet=violet, black=black, white=white, duration=180)