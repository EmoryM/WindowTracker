# proof of concept for an Upwork job where the client
# wanted to track time spent in Windows

import win32gui
import time
import win_unicode_console
import os
from operator import itemgetter

win_unicode_console.enable()

def Save(totals):
    sortedTotals = list(totals.items())
    sortedTotals.sort(key=itemgetter(1))

    with open("log.csv", "w") as csvfile:
        for tup in sortedTotals:
            csvfile.write("{0}, {1:.2f}\n".format(tup[0].replace(",", " "), tup[1]))

lastIn = ""
lastTimeIn = time.time()
totals = {}

w = win32gui

while True:
    currentlyIn = w.GetWindowText(w.GetForegroundWindow())
    if lastIn != currentlyIn:
        if lastIn != "":
            minutesIn = (time.time() - lastTimeIn)/60.0
            print("Spent {0:.2f} minutes in {1}".format(minutesIn, lastIn))
            if lastIn in totals:
                totals[lastIn] = totals[lastIn] + minutesIn
            else:
                totals[lastIn] = minutesIn
            print(" for a total of {0:.2f} minutes".format(totals[lastIn]))
            try:
                Save(totals)
            except Exception as e:
                print(type(e))

        lastTimeIn = time.time()
        lastIn = currentlyIn

    time.sleep(1.0)