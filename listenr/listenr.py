#!/usr/bin/python


from subprocess import call

# setup
cmd="airmon-ng"
options="start wlan0"
call([cmd, options])

# start capturing
cmd="tshark"
options="-i mon0"
call ([cmd, options])


