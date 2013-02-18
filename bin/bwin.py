#!/usr/bin/python

import wx 
import time
import random

# http://www.daniweb.com/software-development/python/code/216881/drawing-on-a-wxpython-surface
class MyFrame(wx.Frame): 
    """a frame with a panel"""
    def __init__(self, parent=None, id=-1, title=None): 
        wx.Frame.__init__(self, parent, id, title) 
        self.panel = wx.Panel(self, size=(640, 480)) 
        self.panel.Bind(wx.EVT_PAINT, self.on_paint) 
        self.Fit() 
        self.dostuff();
    def on_paint(self, event):
        # establish the painting surface
        dc = wx.PaintDC(self.panel)
        #dc.SetPen(wx.Pen('blue', 4))
        # draw a blue line (thickness = 4)
        #dc.DrawLine(50, 20, 300, 20)
        #dc.SetPen(wx.Pen('red', 1))
        # draw a red rounded-rectangle
        #rect = wx.Rect(50, 50, 100, 100) 
        #dc.DrawRoundedRectangleRect(rect, 8)
        # draw a red circle with yellow fill
        dc.SetBrush(wx.Brush('yellow'))
        x = 250+(random.random()*50)
        y = 100
        r = 5
        print "dopaint %d %d %d\n" % (x,y,r) 
        dc.DrawCircle(x, y, r)
        self.Show()
    def update(self):
        dc = wx.PaintDC(self.panel)
        dc.SetBrush(wx.Brush('yellow'))
        x = 250+(random.random()*50)
        y = 100
        r = 5
        print "dopaint %d %d %d\n" % (x,y,r) 
        dc.DrawCircle(x, y, r)
        self.Show()
    def dostuff(self):
        for x in range (90):
            print "x=%d" % x
            self.update()
            time.sleep(1)


# test it ...
app = wx.PySimpleApp() 
frame1 = MyFrame(title='rounded-rectangle & circle') 
frame1.Center() 
frame1.Show() 
app.MainLoop()



