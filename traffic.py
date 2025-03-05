## https://askubuntu.com/questions/105536/tool-to-shutdown-system-when-there-is-no-network-traffic
## Download Monitor v0.1 - March 2012

# Set the interface you wish to monitor, eg: eth0, wlan0, usb0
INTERFACE = "wlp2s0"

# Set the minimum download speed in KB/s that must be achieved.
MINIMUM_SPEED = 444

# Set the number of retries to test for the average minimum speed. If the average speed is less
# than the minimum speed for x number of retries, then shutdown.
RETRIES = 5

# Set the interval (in seconds), between retries to test for the minimum speed.
INTERVAL = 10

import os, asyncio, datetime, time
#from commands import getoutput

def received_bytes():
    dev = open("/proc/net/dev", "r").readlines()

    header_line = dev[1]
    header_names = header_line[header_line.index("|")+1:].replace("|", " ").split()
    #print(header_names)

    values={}
    for line in dev[2:]:
        intf = line[:line.index(":")].strip()
        values[intf] = [int(value) for value in line[line.index(":")+1:].split()]
        #print (intf,values[intf])

    return values[INTERFACE][0]

async def new_bytes():
    global speedBytes
    lastReceiveBytes = received_bytes()
    totalReceiveBytes = received_bytes()

    while (True):
        lastReceiveBytes = totalReceiveBytes
        totalReceiveBytes = received_bytes()

        totalReceiveBytes = received_bytes()
        receivedBs = totalReceiveBytes - lastReceiveBytes

        speedBytes = receivedBs
        #print("Viteza de descărcare este de " + str(speedBytes) + " octeți pe secundă.")

        await asyncio.sleep(1)

async def worker():
    await asyncio.sleep(2)
    RETRIES_COUNT = RETRIES
    while True:
        SPEED = speedBytes / 1024
        #print("Viteza este de " + str(SPEED) + " KO/s.")

        if (SPEED < MINIMUM_SPEED and RETRIES_COUNT <= 0):
            print("Se oprește imediat!")
            os.system("shutdown -h now")
            break
        elif SPEED < MINIMUM_SPEED:
            print("Viteza de descărcare " + str(SPEED) + " KO/s este mai mică decât cea minimă " + str(MINIMUM_SPEED) + "KB/s. S-a întâmplat consecutiv de " + str(RETRIES -RETRIES_COUNT + 1) + " din " + str(RETRIES) + " ori!")
            RETRIES_COUNT -= 1
            await asyncio.sleep(INTERVAL)
        else:
            print("Viteza de descărcare " + str(SPEED) + " KO/s este mai mare decât cea minimă " + str(MINIMUM_SPEED) + "KB/s.")
            RETRIES_COUNT = RETRIES
            await asyncio.sleep(INTERVAL)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.create_task(new_bytes())
loop.create_task(worker())

loop.run_forever()