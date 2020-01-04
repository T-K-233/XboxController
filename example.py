import time
import sys

from XboxController import XboxController, Hand

def listDevices():
    numbers, sticks = XboxController.enumerateDevices()
    print("found %d devices: %s" % (len(numbers), numbers))
    
    if not sticks:
        sys.exit(0)

    for stick in sticks:        
        print("stick num" % stick.device_number)
        print(stick.getBatteryInformation())

def loopBasedExample():
    """
    """
    stick = XboxController(0)

    while True:
        stick.dispatchEvents()
        stick.setRumble(Hand.k_left, abs(stick.axes["LTrigger"]))
        stick.setRumble(Hand.k_right, abs(stick.axes["RTrigger"]))
        print("A Btn:", stick.getAButton(), end="")
        print("\tPOV:", stick.getPOV(), end="")
        print("\tX Axis:", stick.getX(Hand.k_left))
        time.sleep(.01)

def eventBasedExample():
    """
    """
    stick = XboxController(0)

    @stick.event
    def onButton(button, state):
        print("button", button, state)
        pass
    
    @stick.event
    def onAxis(axis, value):
        print("axis", axis, value)
        if axis == "LTrigger":
            stick.setRumble(Hand.k_left, value)
        if axis == "RTrigger":
            stick.setRumble(Hand.k_right, value)

    while True:
        stick.dispatchEvents()
        time.sleep(.01)


if __name__ == "__main__":
    loopBasedExample()
    # eventBasedExample()

