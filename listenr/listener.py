#!/usr/bin/python

# kill potentially interfering processes with airmom 
# do not kill supplicant process = internet access
/usr/local/sbin/airmon-ng check wlan0 | /bin/grep -v supplicant | /bin/grep -P -e"^[0-9]{4}"  -o


