#!/usr/bin/python

#is monitor already running
cmd='ifconfig'
res = subprocess.check_output(cmd)
m=re.search(r"\n(mon\d)\s+Link",res)
if m:
        interface=m.group(1)
else:
        interface=None

if (interface is not None):
    cmd=[]
    cmd.append("airmon-ng")
    cmd.append("stop")
    cmd.append(interface)

    rc = subprocess.call(cmd)

