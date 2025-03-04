##https://askubuntu.com/questions/105536/tool-to-shutdown-system-when-there-is-no-network-traffic
## Download Monitor v0.1 - March 2012

# Set the interface you wish to monitor, eg: eth0, wlan0, usb0
INTERFACE = "eth0"

# Set the minimum download speed in KB/s that must be achieved.
MINIMUM_SPEED = 444

# Set the number of retries to test for the average minimum speed. If the average speed is less
# than the minimum speed for x number of retries, then shutdown.
RETRIES = 5

# Set the interval (in seconds), between retries to test for the minimum speed.
INTERVAL = 10


import os, time
#from commands import getoutput

def worker ():
    print("Începe lucrătorul.")
    RETRIES_COUNT = RETRIES
    while True:
        print("-")
        #SPEED = int(float(getoutput("ifstat -i %s 1 1 | awk '{print $1}' | sed -n '3p'" % INTERFACE)))
        print("Viteza este de " + getSpeed() + " KB/s.")
        SPEED = int(float(getSpeed()))
        #print(SPEED)
        if (SPEED < MINIMUM_SPEED and RETRIES_COUNT <= 0):
            print("Se oprește imediat!")
            os.system("shutdown -h now")
            #os.system("shutdown -h +44")
            break
        elif SPEED < MINIMUM_SPEED:
            print("S-a întâmplat de " + str(RETRIES -RETRIES_COUNT + 1) + " din " + str(RETRIES) + " consecutiv ca viteza să fie mai mică decât " + str(MINIMUM_SPEED) + "KB/s.")
            RETRIES_COUNT -= 1
            print("Așteaptă pentru " + str(INTERVAL) + " secunde.")
            time.sleep(INTERVAL)
        else:
            print("Mai încearcă.")
            RETRIES_COUNT = RETRIES
            print("Doarme pentru " + str(INTERVAL) + " secunde.")
            time.sleep(INTERVAL)


def getSpeed():
    file = "speed.txt"
    f = open(file, "r")
    speed = f.read()
    return str(speed)

def bucla():
    while (True):
        print("Începe bucla.")
        try:
            worker()
        except:
            print("A avut loc o erare.")
            print("Reîncepe bucla după " + str(INTERVAL) + " secunde.")
            time.sleep(INTERVAL)

#worker()
bucla()