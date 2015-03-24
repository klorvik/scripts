#!/usr/bin/env python2                                                                                                                                                                                                                   i
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

__author__ = "Knut Lorvik (knutlor 'at' tihlde.org)"

# Script for adding multitouch to ubuntu based distros.
# Currently only supports two-finger swipes.

# Imports
import os
import re
import subprocess
import time

# Settings
SENSITIVITY_Y = 900
SENSITIVITY_X = 200
SWIPE_TIME = 0.37 # in ms

COMMAND_UP = "xdotool key ctrl+alt+Up"
COMMAND_DOWN = "xdotool key ctrl+alt+Down"
COMMAND_LEFT = "xdotool key alt+Left"
COMMAND_RIGHT = "xdotool key alt+Right"

# Command for fetching input data
cmd = "synclient -m 100"

# Start subprocess
p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
start = False
start_x = 0
start_y = 0
diff_x = 0
diff_y = 0	
timeStart = 0
timeEnd = 0
try:
    while True:
    line = p.stdout.readline()
    if not line:
	break
    try:
	# Parse data
	tokens = [x for x in re.split('([^0-9\.])+', line.strip()) if x.strip()]
	x, y, fingers = int(tokens[1]), int(tokens[2]), int(tokens[4])
	if fingers==3:
	    if not start:
	 	start_x = x
		start_y = y
		start = True
		timeStart = time.time()
	if start and not fingers==3:
	    if time.time()-timeStart>SWIPE_TIME:
		start = False
		start_x = 0
		start_y = 0
		diff_x = 0
		diff_y = 0        
	    else:
		diff_x = x-start_x
		diff_y = y-start_y
		if diff_y > SENSITIVITY_Y:
		    os.system(COMMAND_UP)
		elif diff_y < -SENSITIVITY_Y:
		    os.system(COMMAND_DOWN)
		elif diff_x > SENSITIVITY_X:
		    os.system(COMMAND_RIGHT)
		elif diff_x < -SENSITIVITY_X:
		    os.system(COMMAND_LEFT)
		start = False
		start_x = 0
 		start_y = 0
		diff_x = 0			
		diff_y = 0
    except (IndexError, ValueError):
        pass
except KeyboardInterrupt:
    pass
