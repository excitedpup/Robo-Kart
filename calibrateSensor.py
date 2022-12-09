from spike.control import wait_for_seconds


def beep(amount, hub):
    for i in range(amount):
        hub.speaker.beep()

def wait(seconds):
    wait_for_seconds(seconds)

# get rgb calibration
def calibrateSensor(sensor, hub):
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