import wx
from bufferedcanvas import *
import wx.lib.plot as plot



class TestCanvas(BufferedCanvas):

    def __init__(self,parent,ID=-1):
        BufferedCanvas.__init__(self,parent,ID)


    def draw(self, dc):
        dc.SetBackground(wx.Brush("Black"))
        dc.Clear()

        dc.SetBrush(wx.BLUE_BRUSH)
        dc.SetPen(wx.Pen('Red', 4))
        dc.DrawRectangle(20,20,300,200)


class MyFrame(wx.Frame):

 def __init__(self):
    self.frame1 = wx.Frame(None, title="Raspberry Pis' Clients Plotting", id=-1, size=(800, 600))
    self.panel1 = wx.Panel(self.frame1)
    self.panel1.SetBackgroundColour("green")
    
    status=self.CreateStatusBar()
    menubar=wx.MenuBar()
    first=wx.Menu()
    second=wx.Menu()
    
    # Difference between wxPython26 and wxPython28 into count
    if wx.VERSION[1] < 7:
      plotter = plot.PlotCanvas(self.panel1, size=(800, 600))
    else:
      plotter = plot.PlotCanvas(self.panel1)
      plotter.SetInitialSize(size=(800, 600))
      
    plotter.SetEnableZoom(True)

    data = [(1,2), (2,10), (3,4), (4,5), (5,6), (6,7), (7,8), (-8,9)]
    
    marker = plot.PolyMarker(data, marker='circle')
    
    gc = plot.PlotGraphics([marker], 'Clients Location', 'Location by signal in X axis', 'Location by signal in Y axis')
    plotter.Draw(gc, xAxis=(-10,10), yAxis=(-15,15))
    
    self.frame1.Show(True)

def main():
    app = wx.PySimpleApp()
    frame = MyFrame()
    app.MainLoop()

if __name__ == '__main__':
    main()
