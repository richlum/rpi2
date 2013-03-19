import sys
if not hasattr(sys, 'frozen'):
    import wxversion
    wxversion.ensureMinimal('2.8')

import wxmplot
import wx
import numpy

app = wx.App()

pframe = wxmplot.PlotFrame()
z = [1,2,3,4,5,6,7,8,9]
x = []
y = []
for i in range (0,len(z)):
  x.append(z[i])
  y.append(z[len(z)-1-i])
  pframe.add_text(str(i),x[i],y[i],side='left',rotation=None,ha='right',va='center',size=10,color='green')

pframe.scatterplot(x, y, title='Nearby Wifi Clients', size=20,xlabel='Distance (meters)',ylabel='Distance (meters)')
pframe.Show()

app.MainLoop()