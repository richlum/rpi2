#Updated February 27,2013

import wx
import wx.lib.plot as plot


class MyFrame(wx.Frame):
  def __init__(self):
    self.frame1 = wx.Frame(None, title="Raspberry Pis' Clients Plotting", id=-1, size=(800, 600))
    self.panel1 = wx.Panel(self.frame1)
    self.panel1.SetBackgroundColour("green")
    
    # taking difference between wxPython26 and wxPython28 into count
    if wx.VERSION[1] < 7:
      plotter = plot.PlotCanvas(self.panel1, size=(800, 600))
    else:
      plotter = plot.PlotCanvas(self.panel1)
      plotter.SetInitialSize(size=(800, 600))
      
    # enable the zoom feature (drag a box around area of interest)
    plotter.SetEnableZoom(True)

    # list of (x,y) test file
    data = [(1,2), (2,10), (3,4), (4,5), (5,6), (6,7), (7,8), (-8,9)]
    
    marker = plot.PolyMarker(data, marker='circle')
    
    gc = plot.PlotGraphics([marker], 'Clients Location', 'Location by signal in X axis', 'Location by signal in Y axis')
    plotter.Draw(gc, xAxis=(-10,10), yAxis=(-15,15))
    
    self.frame1.Show(True)

application = wx.PySimpleApp()
f = MyFrame()
application.MainLoop()
