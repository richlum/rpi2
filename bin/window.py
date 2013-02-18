#!/usr/bin/python

import wx

app = wx.App()

frame = wx.Frame(None, -1, 'pi viewer',style=wx.MAXIMIZE_BOX | wx.RESIZE_BORDER|wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX , size=(640,480))



frame.Show(True)
canvas = wx.PaintDC(frame)
wx.FutureCall(2000,canvas.DrawLine(50,60,190,60))


app.MainLoop()

