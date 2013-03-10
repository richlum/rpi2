import wx
import wx.lib.plot as plot

class rpiframe(wx.Frame):
  
  def __init__(self,parent,id):
    wx.Frame.__init__(self,parent,id,'RPI-2 Group', size=(800,600))
    self.InitUI()
    self.Centre()
    self.Show()
    
  def InitUI(self):
  
    self.panel=wx.Panel(self)
    status=self.CreateStatusBar()
    menubar=wx.MenuBar()
    first=wx.Menu()
    second=wx.Menu()
    first.Append(wx.NewId(),"Quit", "Quit Program")
    second.Append(wx.NewId(),"Refresh Data", "Refresh Data")
    menubar.Append(first,"File")
    menubar.Append(second,"Data")
    self.SetMenuBar(menubar)
    
    plotter = plot.PlotCanvas(self.panel)
    plotter.SetInitialSize(size=(800,600))
    plotter.SetEnableZoom(True)
    
    data=[(1,2)]
    
    marker = plot.PolyMarker(data, marker='circle')
    
    gc = plot.PlotGraphics([marker], 'Clients Location', 'Location by signal in X axis', 'Location by signal in Y axis')
    plotter.Draw(gc, xAxis=(-10,10), yAxis=(-15,15))
        
if __name__=='__main__':
  app=wx.PySimpleApp()
  frame=rpiframe(parent=None,id=-1)
  frame.Show()
  app.MainLoop()