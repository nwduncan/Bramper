import time
import threading

count = 0

start_time = time.time()

def printit():
    t = threading.Timer(1.0, printit)
    # t.daemon = True
    t.start()
    global count
    if count == 1000:
        t.cancel()
        global start_time
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print count
        count+=1

## loses 2.8 seconds every 1000 seconds

printit()
