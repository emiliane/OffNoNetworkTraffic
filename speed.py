interface = "wlp2s0"
file = "speed.txt"
##########################

def getReceiveBytes():
    dev = open("/proc/net/dev", "r").readlines()
    header_line = dev[1]
    header_names = header_line[header_line.index("|")+1:].replace("|", " ").split()

    values={}
    for line in dev[2:]:
        intf = line[:line.index(":")].strip()
        values[intf] = [int(value) for value in line[line.index(":")+1:].split()]

        print (intf,values[intf])

    return values[interface][0]

def writeFile(filename, value):
    f = open(filename, "w")
    f.write(str(value))
    f.close()

def storeSpeed():
    old = getReceiveBytes()
    new = getReceiveBytes()

    import time
    while (True):
        old = new
        new = getReceiveBytes()

        print(old)
        print(new)

        sizeBs = new - old
        print(sizeBs)

        sizeKBs = sizeBs / 1024
        print(sizeKBs)

        sizeMBs = sizeBs / 1024 / 1024
        print(sizeMBs)

        writeFile(file, str(sizeKBs))

        # making delay for 1 second
        time.sleep(1)

storeSpeed()