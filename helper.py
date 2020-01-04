""" helper.py
"""

from XboxController import XboxController, Hand

def determineOptimalSampleRate(joystick=None):
    """
    Poll the joystick slowly (beginning at 1 sample per second)
    and monitor the packet stream for missed packets, indicating
    that the sample rate is too slow to avoid missing packets.
    Missed packets will translate to a lost information about the
    joystick state.
    As missed packets are registered, increase the sample rate until
    the target reliability is reached.
    """
    # in my experience, you want to probe at 200-2000Hz for optimal
    #  performance
    if joystick is None:
        joystick = XboxController.enumerateDevices()[0]

    stick = joystick

    print("Move the joystick or generate button events characteristic of your app")
    print("Hit Ctrl-C or press button 6 (<, Back) to quit.")

    # here I use the joystick object to store some state data that
    #  would otherwise not be in scope in the event handlers

    # begin at 1Hz and work up until missed messages are eliminated
    stick.probe_frequency = 1  # Hz
    stick.quit = False
    stick.target_reliability = .99  # okay to lose 1 in 100 messages

    @stick.event
    def onButton(button, pressed):
        # flag the process to quit if the < button ('back') is pressed.
        stick.quit = stick.getBumper(Hand.k_left)

    @stick.event
    def onMissedPacket(number):
        print('missed %(number)d packets' % vars())
        total = stick.received_packets + stick.missed_packets
        reliability = stick.received_packets / float(total)
        if reliability < stick.target_reliability:
            stick.missed_packets = stick.received_packets = 0
            stick.probe_frequency *= 1.5

    while not j.quit:
        stick.dispatchEvents()
        time.sleep(1.0 / stick.probe_frequency)
    print("final probe frequency was %s Hz" % stick.probe_frequency)
