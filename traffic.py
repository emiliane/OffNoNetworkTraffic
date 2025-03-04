interface = "wlp2s0"
file = "speed.txt"
##########################

import asyncio
import datetime
import time

def get_received_bytes():
    dev = open("/proc/net/dev", "r").readlines()
    #print(dev)
    header_line = dev[1]
    header_names = header_line[header_line.index("|")+1:].replace("|", " ").split()
    #print(header_names)

    values={}
    for line in dev[2:]:
        intf = line[:line.index(":")].strip()
        values[intf] = [int(value) for value in line[line.index(":")+1:].split()]

        #print (intf,values[intf])

    return values[interface][0]

def get_new_received_bytes(lastReceiveBytes):
    totalReceiveBytes = get_received_bytes()
    receivedBs = totalReceiveBytes - lastReceiveBytes
    return receivedBs, totalReceiveBytes

async def display_speed():
    totalReceiveBytes = get_received_bytes()
    global speed
    while True:
        #print(datetime.datetime.now())
        speed,totalReceiveBytes = get_new_received_bytes(totalReceiveBytes)
        print("Viteza de descărcare este de " + str(speed) + " octeți pe secundă.")
        await asyncio.sleep(1)

async def snmp():
    while True:
        print("Doing the snmp thing")
        await asyncio.sleep(1)

async def proxy():
    while True:
        print("Doing the proxy thing")
        print()
        print("Viteza actuală " + str(speed) + " octeți pe secundă.")
        print()
        await asyncio.sleep(1)
  






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

async def worker ():
    print("Începe lucrătorul.")
    RETRIES_COUNT = RETRIES
    while True:
        print("-")
        #SPEED = int(float(getoutput("ifstat -i %s 1 1 | awk '{print $1}' | sed -n '3p'" % INTERFACE)))
        SPEED = speed
        print("Viteza este de " + str(speed) + " octeți/s.")
        SPEED = speed
        #print(SPEED)
        if (SPEED < MINIMUM_SPEED and RETRIES_COUNT <= 0):
            print("Se oprește imediat!")
            #os.system("shutdown -h now")
            os.system("shutdown -h +44")
            break
        elif SPEED < MINIMUM_SPEED:
            print("S-a întâmplat de " + str(RETRIES -RETRIES_COUNT + 1) + " din " + str(RETRIES) + " consecutiv ca viteza să fie mai mică decât " + str(MINIMUM_SPEED) + "KB/s.")
            RETRIES_COUNT -= 1
            print("Așteaptă pentru " + str(INTERVAL) + " secunde.")
            #time.sleep(INTERVAL)
            await asyncio.sleep(INTERVAL)
        else:
            print("Mai încearcă.")
            RETRIES_COUNT = RETRIES
            print("Doarme pentru " + str(INTERVAL) + " secunde.")
            #time.sleep(INTERVAL)
            await asyncio.sleep(INTERVAL)


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
#bucla()



#loop = asyncio.get_event_loop()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(display_speed())
#loop.create_task(snmp())
#loop.create_task(proxy())
loop.create_task(worker())
loop.run_forever()