##https://askubuntu.com/questions/105536/tool-to-shutdown-system-when-there-is-no-network-traffic

## Download Monitor v0.1 - March 2012

# Set the interface you wish to monitor, eg: eth0, wlan0, usb0
INTERFACE = "eth0"

# Set the minimum download speed in KB/s that must be achieved.
MINIMUM_SPEED = 150

# Set the number of retries to test for the average minimum speed. If the average speed is less
# than the minimum speed for x number of retries, then shutdown.
RETRIES = 5

# Set the interval (in seconds), between retries to test for the minimum speed.
INTERVAL = 10


import os, time
#from commands import getoutput

def worker ():
    RETRIES_COUNT = RETRIES
    while True:
        #SPEED = int(float(getoutput("ifstat -i %s 1 1 | awk '{print $1}' | sed -n '3p'" % INTERFACE)))
        SPEED = int(float(getSpeed()))
        print(SPEED)
        if (SPEED < MINIMUM_SPEED and RETRIES_COUNT <= 0):
            print("Se oprește!")
            os.system("shutdown -h now")
        elif SPEED < MINIMUM_SPEED:
            print("Versiunea elif.")
            RETRIES_COUNT -= 1
            time.sleep(INTERVAL)
        else:
            print("Versiunea else.")
            RETRIES_COUNT = RETRIES
            time.sleep(INTERVAL)

file = "speed.txt"

def getSpeed ():
    f = open(file, "r")
    speed = f.read()
    return str(speed)

worker()
