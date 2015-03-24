#!/usr/bin/env python2                                                                                                                                                                                                                   i
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

__author__ = "Knut Lorvik (knutlor 'at' tihlde.org)"

# Script for setting laptop brightness based on 
# current time relative to sunrise and sunset.
# Needs xbacklight to work.

# Imports
from datetime import datetime
import os
import urllib2
import re

# Settings
AREACODE = '865157'
MIN_LEVEL = 10
MAX_LEVEL = 100

# Get data from Yahoo API
try:
    response = urllib2.urlopen('http://weather.yahooapis.com/forecastrss?w=%s' % AREACODE)
except HTTPError as e:
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
    sunrise = 6
    sunset = 20
except URLError as e:
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
    sunrise = 6
    sunset = 20
else:
    # Parse response
    for line in response.read().splitlines():
        if "astronomy" in line:
            string = line.split( )
            sunrise = (string[1]+string[2]).split('"')[1]
            sunset = (string[3]+string[4]).split('"')[1]
    
    print 'Sunrise: %s' % sunrise
    print 'Sunset: %s' % sunset

    sunrise = sunrise.split(':')
    sunset = sunset.split(':')

    # Convert 12-hour times to 24-hour
    if 'pm' in sunrise[1]:
        sunrise = int(sunrise[0]) + 12
    else:
        sunrise = int(sunrise[0])
    if 'pm' in sunset[1]:
        sunset = int(sunset[0]) + 12
    else:
        sunset = int(sunset[0])

# Get current time
current_time = int(datetime.now().strftime("%H"))

# Set level based on current time
if(current_time < sunrise or current_time > sunset):
    level = MIN_LEVEL
else:
    x = float((sunset-sunrise)/2)
    if (current_time >= sunrise and current_time < sunrise+x):
        level = ((current_time-sunrise) / x) * MAX_LEVEL
    else:
        level = ((sunset-current_time) / x ) * MAX_LEVEL
        
if (level < MIN_LEVEL):
    level = MIN_LEVEL

# Set backlight
print 'Setting backlight to %d percent' % level
os.system('xbacklight -set %s' % level)