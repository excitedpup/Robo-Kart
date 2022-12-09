# This is our Main.py file containing our code
from spike import PrimeHub,ColorSensor, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer
from math import *

from calibrateSensor import beep, wait, calibrateSensor

# Initialize
timer = Timer()
racetimer = Timer()
color_sensor_reactions = ColorSensor('E')
motor_pair = MotorPair('C','D')
hub = PrimeHub()
matrix = hub.light_matrix
left_motor = Motor('C')
right_motor = Motor('D')
distance_sensor =  DistanceSensor('F')

counter = 0
lap1 = 0
lap2 = 0
lap3 = 0



# If red is sensed by light sensor, the robot's
# default speed will go down by 1.5 times.
def redDetected():
    base = motor_pair.get_default_speed()
    matrix.show_image('SAD')
    motor_pair.start(steering=0, speed=int(base/1.5))
    wait(2)
    motor_pair.start(steering=0, speed=base)
    hub.light_matrix.off()

# If green is sensed by light sensor, the robot's
# default speed will go up by 1.5 times.
def greenDetected():
    base = motor_pair.get_default_speed()
    matrix.show_image('ARROW_N')
    motor_pair.start(steering=0, speed=int(base *1.5))
    wait(2)
    motor_pair.start(steering=0, speed=base)
    hub.light_matrix.off()

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
def hover(distance=30):
    base = motor_pair.get_default_speed()
    
    # Honk Honk
    beep(1, hub)
    wait(0.3)
    beep(1, hub)
    wait(0.3)
    beep(1, hub)
    
    while True:
        if (distance_sensor.get_distance_cm() == None) or (distance_sensor.get_distance_cm() >= distance):
            left_motor.start(-(100))
            wait(0.1)    # Might have to switch these values
            left_motor.stop()
            right_motor.start(50)
            wait(0.4)   # Might have to switch these values
            right_motor.stop()
        else:
            motor_pair.start(steering=0, speed=base)
            break

# This detects the color by taking in the color value it sensed and compares it to 
#  the color values upon calebration and 
# returns True if the value is in the number range
def isColor(colorVal, getColor, numRange):
    if colorVal[0]-numRange <= getColor[0] <= colorVal[0]+numRange:
        if colorVal[1]-numRange <= getColor[1] <= colorVal[1]+numRange:
            if colorVal[2]-numRange <= getColor[2] <= colorVal[2]+numRange:
                if colorVal[3]-numRange <= getColor[3] <= colorVal[3]+numRange:
                    return True
    else:
        return False

# This is different from the isColor method, because the yellow seemed to not always work.
# ****** WE SHOULD RECHECK THIS *******
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
    beep(1, hub)
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
            wait(6) # CHANGE BACK WHEN YOU STOP LIFTING BOT UP/BOT ABLE TO TRACK FOLLOW
        elif isColor(black, color_sensor_reactions.get_rgb_intensity(), 40):
            print("black")
            wait(0.1)
        else:
            print("white")
            wait(0.1)
    
    motor_pair.stop()
    if lap1<lap2 and lap1<lap2:
        fastestLap = lap1
    elif lap2<lap1 and lap2<lap3:
        fastestLap = lap2
    else:
        fastestLap = lap3
    print('Fastest Lap is:')
    print(fastestLap)
    

red, green, yellow, blue, violet, black, white = calibrateSensor(color_sensor_reactions, hub)
main(red=red, green=green, yellow=yellow, blue=blue, violet=violet, black=black, white=white, duration=60)
