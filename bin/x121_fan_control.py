#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
""" 
   
   x121_fan_control.py 


#  Copyright 2012 Oz N <nahumoz__AT_NONONO_SPAMHERE g m a i l dot com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
"""

import re
import ConfigParser,sys
import os
#from optparse import OptionParser
import argparse

# max allowed temp: level 


#LEVELS = (0,  1,  2,  5,  6,  7)
#LIMITS = (0, 53, 63, 67, 73, 100)

BASE_POLL_TIME_INTERVAL = 10
TEMP_SENSOR = "/proc/acpi/ibm/thermal"
FAN_INFO = "/proc/acpi/ibm/fan"

def poll():
    with open(TEMP_SENSOR) as ts:
        ts = ts.next()
        print ts.strip('\n')
        ts = re.search('\d+', ts)
        cputemp = ts.group()
        print "cputemp ", cputemp
    with open(FAN_INFO) as faninfo:
        faninfo = faninfo.readlines()
        faninfo = faninfo[2]
        if  'auto' in faninfo:
            fan_level = 'auto'
        else:
            faninfo = re.search('\d+', faninfo)
            fan_level = faninfo.group()
            #fan_level = faninfo.split(':')
        print  "fan_level ", fan_level
    return fan_level, cputemp




def main():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Control the Fan of Lenovo \
    thinkpad x121e')
    parser.add_argument('--poll',help='Poll the tempratures, do nothing \
    real', action="store_true")
    args = parser.parse_args()
    
    if args.poll:
        print "polling turned on"
        fanlevel, cpu_temp = poll()
    # do the actual control
    if fanlevel == 'auto':
        fanlevel = 0
    print "fanlevel ", fanlevel
    # dictionaries suck!
    MAXTEMP_LEVEL = {53:0, 56:1, 58:2, 70:5, 75:7}
    for k,v in MAXTEMP_LEVEL.iteritems():
        print "max temp allowed for the level ", k, "is ",v
        if int(fanlevel) >= v and int(cpu_temp) < k:
            print "fan is overworking will reduce one level"
            print "call to some_reduce_function"
            break
        if int(fanlevel) <= v and int(cpu_temp) > k:
            print "fan is under working will increase one level"
            print "call to some_increase_function"
            break
            

if __name__ == '__main__':
    main()


