#!/usr/bin/python
import curses
import os

myscr= curses.initscr()
myscr.border(0)
yx = myscr.getmaxyx()
myscr.addstr(str(yx[0]) +"," +str(yx[1])  )
myscr.addstr(1,yx[1]/2-10, "RPI 2 Proximity")
myscr.refresh()
myscr.getch()

curses.endwin()

os.system('reset')
