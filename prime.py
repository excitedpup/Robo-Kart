# This is the file we have to copy/paste into Spike Prime
# This is our Main.py file containing our code
from spike import PrimeHub,ColorSensor, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer
from math import *
import random

# Initialize
timer = Timer()
racetimer = Timer()
color_sensor_reactions = ColorSensor('A')
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

def blueDetected():
    base = motor_pair.get_default_speed()
    #Goes at 3/4 current speed if going fast and half speed if going slow
    fast = False
    waterSpeed = 0
    if base >= 35:
        waterSpeed = int(base * 3/4)
        fast = True
    else:
        waterSpeed = int(base/2)

    while colorRight.get_color() != 'white':
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

    motor_pair.set_default_speed(base)

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
# ********** NOT TESTED YET ***********
def hover(distance=20):
    base = motor_pair.get_default_speed()

    # # Honk Honk Honk
    # beep(3)

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
        print(steer)
        wait(.3)
    motor_pair.start(steering=0, speed=35)

def turnLeft(base = 50):
    steer = -(random.randint(80,90))
    while colorRight.get_color() == 'black':
        motor_pair.start(steering=steer, speed=base)
        print(steer)
        wait(.3)
    motor_pair.start(steering=0, speed=35)

def testTurn():
    motor_pair.start(steering = 0, speed=35)

    while(True):
        if colorLeft.get_color() == 'black':
            turnRight()
        elif colorRight.get_color() == 'black':
            turnLeft()
        else:
            motor_pair.start(steering = 0, speed=35)


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
    fastestLap = 0

    while (timer.now() < duration):
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
            yellowDetected(2, 100, .1)
            #wait(0.1)
        elif isColor(blue, color_sensor_reactions.get_rgb_intensity(), 80):
            print("blue")
            wait(0.1)
        elif isColor(violet, color_sensor_reactions.get_rgb_intensity(), 60):
            print("violet")
            #print(racetimer.now())
            # fastestLap declaration here can be taken out I think!!!
            fastestLap = raceTimer(racetimer.now())
            counter = counter + 1
            wait(1) # CHANGE BACK WHEN YOU STOP LIFTING BOT UP/BOT ABLE TO TRACK FOLLOW
        elif isColor(black, color_sensor_reactions.get_rgb_intensity(), 40):
            print("black")
            wait(0.1)
        else:
            print("white")
            wait(0.1)
        if distance_sensor.get_distance_cm() == None:
            pass
        elif distance_sensor.get_distance_cm() <= 30:
            print(distance_sensor.get_distance_cm())
            print("It got here")
            hover(30)

    motor_pair.stop()
    if lap1<lap2 and lap1<lap2:
        fastestLap = lap1
    elif lap2<lap1 and lap2<lap3:
        fastestLap = lap2
    else:
        fastestLap = lap3
    print('Fastest Lap is:')
    print(fastestLap)


#red, green, yellow, blue, violet, black, white = calibrateSensor(color_sensor_reactions)
#main(red=red, green=green, yellow=yellow, blue=blue, violet=violet, black=black, white=white, duration=60)


def main2(red, green, yellow, blue, violet, black, white, duration=15):
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
    fastestLap = 0
    base = 35

    while (timer.now() < duration):
        print(distance_sensor.get_distance_cm())
        if distance_sensor.get_distance_cm() is None:
            pass
        elif distance_sensor.get_distance_cm() <= 30:
            print(distance_sensor.get_distance_cm())
            print("It got here")
            hover(30)

        if not colorStatus:
            motor_pair.start(steering=0, speed=base)
            if isColor(red, color_sensor_reactions.get_rgb_intensity(), 80):
                print("red")
                colorStatus = True
                colorTime = timer.now() + 2
                redDetected()
            elif isColor(green, color_sensor_reactions.get_rgb_intensity(), 80):
                print("green")
                colorStatus = True
                colorTime = timer.now() + 2
                greenDetected()
            elif isYellow(yellow, color_sensor_reactions.get_rgb_intensity(), 80):
                print("yellow")
                yellowDetected(2, 100, .1)
            elif isColor(blue, color_sensor_reactions.get_rgb_intensity(), 80):
                print("blue")
                blueDetected()
        else:
            if colorTime < timer.now():
                colorStatus = False
                hub.light_matrix.off()


        if isColor(violet, color_sensor_reactions.get_rgb_intensity(), 60):
            print("violet")
            #print(racetimer.now())
            # fastestLap declaration here can be taken out I think!!!
            fastestLap = raceTimer(racetimer.now())
            counter = counter + 1
            wait(1) # CHANGE BACK WHEN YOU STOP LIFTING BOT UP/BOT ABLE TO TRACK FOLLOW

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

#red, green, yellow, blue, violet, black, white = calibrateSensor(color_sensor_reactions)
red = (315, 84, 123, 407)
green = (136, 207, 137, 360)
yellow = (613, 522, 318, 1016)
blue = (76, 153, 259, 321)
violet = (83, 79, 138, 207)
black = (47, 51, 52, 111)
white = (601, 607, 608, 1011)
main2(red=red, green=green, yellow=yellow, blue=blue, violet=violet, black=black, white=white, duration=60)