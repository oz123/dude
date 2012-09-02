#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import argparse
import time
import subprocess as sp

# max allowed temp: level 
MAXTEMP_LEVEL = {53:0, 60:1, 64:2, 70:5, 75:7}

BASE_POLL_TIME_INTERVAL = 10
TEMP_SENSOR = "/proc/acpi/ibm/thermal"
FAN_INFO = "/proc/acpi/ibm/fan"

# todo:
# 1. add pid file under /var/run
# 2. add option to damonize
# 3. add logging (python logging module?)
# 4. document properly

def best_fan_level(clevel,ctemp):
    """
    in case fan level is auto, we need to find the right level to 
    start with ...
    """
    nearest_temp=min(MAXTEMP_LEVEL.keys(), key=lambda k: abs(k-ctemp))
    # this is the same as doing:
    # temp_d={}
    # for k in MAXTEMP_LEVEL.keys():
    #     temp_d[abs(k-ctemp)] = k
    # print temp_d[min(temp_d.key())]
    #if clevel < MAXTEMP_LEVEL[mintemp]:
    #    print "current level is", str(clevel), "we should be on ",str(MAXTEMP_LEVEL[mintemp])
    #print "T: %d L: %d  Tnear: %d Levelnear: %d" % (ctemp, 
    #clevel, nearest_temp, MAXTEMP_LEVEL[nearest_temp])
    
    if ctemp >= nearest_temp and clevel < MAXTEMP_LEVEL[nearest_temp]:
        print "T: %d L: %d  Tnear: %d Levelnear: %d, fan increased" % (ctemp, 
    clevel, nearest_temp, MAXTEMP_LEVEL[nearest_temp])
    if ctemp < nearest_temp and clevel > MAXTEMP_LEVEL[nearest_temp]:
        print "T: %d L: %d  Tnear: %d Levelnear: %d, fan decreased" % (ctemp, 
    clevel, nearest_temp, MAXTEMP_LEVEL[nearest_temp])
       
    elif ctemp < nearest_temp and clevel == MAXTEMP_LEVEL[nearest_temp]:
        print "T: %d L: %d  Tnear: %d Levelnear: %d, fan safe" % (ctemp, 
    clevel, nearest_temp, MAXTEMP_LEVEL[nearest_temp])
    
    elif ctemp > nearest_temp and clevel == MAXTEMP_LEVEL[nearest_temp]:
        print "T: %d L: %d  Tnear: %d Levelnear: %d, fan safe*" % (ctemp, 
    clevel, nearest_temp, MAXTEMP_LEVEL[nearest_temp])
        
    
    #print "sent ", MAXTEMP_LEVEL[nearest_temp]
    return MAXTEMP_LEVEL[nearest_temp]

            
def set_level(new_level):
    """
    set fan to new level
    """
    cmd = "echo \"level "+str(new_level)+"\" >"+FAN_INFO
    #print cmd
    setcmd = sp.Popen(cmd, shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
    err, out = setcmd.communicate()
    
def poll():
    with open(TEMP_SENSOR) as ts:
        ts = ts.next()
        #print ts.strip('\n')
        ts = re.search('\d+', ts)
        cputemp = ts.group()
        #print "cputemp ", cputemp
    with open(FAN_INFO) as faninfo:
        faninfo = faninfo.readlines()
        faninfo = faninfo[2]
        if  'auto' in faninfo:
            fan_level = 'auto'
        else:
            faninfo = re.search('\d+', faninfo)
            fan_level = faninfo.group()
        #print  "fan_level ", fan_level
    return fan_level, cputemp

def loop_sleep(args):
    """
    the polling loop
    """
    fanlevel, cpu_temp = poll()
    if fanlevel == 'auto':
        fanlevel = 0
                
    continue_polling = True
    while continue_polling:
        newlevel=best_fan_level(int(fanlevel), int(cpu_temp))
        set_level(newlevel)
        
        fanlevel, cpu_temp = poll()
        if fanlevel == 'auto':
            fanlevel = 0
        time.sleep(5)
            

def main():
    if not os.getuid() == 0:
        print "You must be root to change fan speed."
        sys.exit(2)
        
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Control the Fan of Lenovo \
    thinkpad x121e')
    parser.add_argument('--poll',help='Poll the tempratures, do nothing \
    real', action="store_true")
    
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args=parser.parse_args()
    
    if args.poll:
        print "polling turned on"
        loop_sleep(args)
        
if __name__ == '__main__':
    main()


