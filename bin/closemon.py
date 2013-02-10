#!/usr/bin/python
import subprocess

cmdstr='sudo airmon-ng stop mon0'
cmd=cmdstr.split()
rc= subprocess.call(cmd)
