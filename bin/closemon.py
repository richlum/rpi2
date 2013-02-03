#!/usr/bin/python
import subprocess

cmdstr='airmon-ng stop mon0'
cmd=cmdstr.split()
rc= subprocess.call(cmd)
