#!/usr/bin/python


import threading
import thread
import time


class storage(threading.Thread):
    def run(self):
        self.data=['zz']
        self.dlock = thread.allocate_lock()
        while(True):
            self.dlock.acquire()
            self.displaydata()
            self.dlock.release()
            time.sleep(4)

    def __init__(self):
        super(storage,self).__init__()
        testfield = 'test'

    def input(self, stuff):
        self.dlock.acquire()
        self.data.append(stuff)
        self.dlock.release()

    def displaydata(self):
        for idx, x in enumerate(self.data):
            print str(idx) + str(self.data)



store = storage()
store.start()

print("Value to store(x to exit):")
foo=raw_input()
while str(foo)[0] != "x":
    print "storing %s\n" % foo
    store.input(str(foo))
    foo=raw_input("Value to store(x to exit):")


        
