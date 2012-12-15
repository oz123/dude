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
# http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
# http://motoma.io/daemonizing-a-python-script/
# https://github.com/kasun/YapDi

import sys, time,os,argparse
from daemon import Daemon
import re
import sys
import os
import argparse
import time
import subprocess as sp
import signal
import kmod

#cat /proc/modules | cut -f 1 -d " " | while read module; do  echo "Module: $module";  if [ -d "/sys/module/$module/parameters" ]; then   ls /sys/module/$module/parameters/ | while read parameter; do    echo -n "Parameter: $parameter --> ";    cat /sys/module/$module/parameters/$parameter;   done;  fi;  echo; done

# max allowed temp: level 
MAXTEMP_LEVEL = {53:0, 68:1, 69:2, 70:5, 75:7}

BASE_POLL_TIME_INTERVAL = 10
TEMP_SENSOR = "/proc/acpi/ibm/thermal"
FAN_INFO = "/proc/acpi/ibm/fan"

class FanControlDaemon(Daemon):
    
    def best_fan_level(self,c_fan_level,ctemp):
        """
        in case fan level is auto, we need to find the right level to 
        start with ...
        """
        nearest_temp = min(MAXTEMP_LEVEL.keys(), key=lambda k: abs(k-ctemp))
        #print "nt " ,  nearest_temp, "ctemp", ctemp
        allowed_fan_level = MAXTEMP_LEVEL[nearest_temp]
        if ctemp >= nearest_temp and c_fan_level <= allowed_fan_level:
            print "T: %d L: %d  Tnear: %d Levelnear: %d, fan increased" % (ctemp, 
            c_fan_level, nearest_temp, allowed_fan_level)
            return allowed_fan_level
        if ctemp <= nearest_temp and c_fan_level > allowed_fan_level:
            print "T: %d L: %d  Tnear: %d Levelnear: %d, fan decreased" % (ctemp, 
            c_fan_level, nearest_temp, allowed_fan_level)
            return allowed_fan_level
        elif ctemp <= nearest_temp and c_fan_level == allowed_fan_level:
            print "T: %d L: %d  Tnear: %d Levelnear: %d, fan safe" % (ctemp, 
            c_fan_level, nearest_temp, allowed_fan_level)
            return allowed_fan_level
        #elif ctemp >= nearest_temp and c_fan_level == allowed_fan_level:
        #    print "T: %d L: %d  Tnear: %d Levelnear: %d, fan safe*" % (ctemp, 
        #    c_fan_level, nearest_temp, allowed_fan_level)
        #    return allowed_fan_level
        print "whopps ", ctemp, c_fan_level
        
        
    def poll(self):
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
                fan_level = 1
            else:
                faninfo = re.search('\d+', faninfo)
                fan_level = faninfo.group()
            #print  "fan_level ", fan_level
        return fan_level, cputemp    
    
    def set_level(self,new_level):
        """
        set fan to new level
        """
        cmd = "echo \"level "+str(new_level)+"\" >"+FAN_INFO
        setcmd = sp.Popen(cmd, shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
        err, out = setcmd.communicate()
        
    def run(self):
        while True:
            fanlevel, cpu_temp = self.poll()
            if fanlevel == 'auto':
                fanlevel = 0
                    
            newlevel = self.best_fan_level(int(fanlevel), int(cpu_temp))
            self.set_level(newlevel)
            time.sleep(5)
    
    
    def start(self):
        """
        Start in forground
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        
        pid = str(os.getpid())
        print "[pid: %s]" % pid   
        open(self.pidfile,'w+').write("%s\n" % pid)
        self.run()
    
    def startd(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        self.run()

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.startd()

def check_config():
    """
    this function checks that we can change the fan speed
    and that the correct modules are loaded 
    lsmod | grep coretemp
    lsmod | grep thinkpad_acpi
    grep /etc/modprobe.d/thinkfan.conf
    """        
    print "not yet implemented"
    # first that we have the modules loades
    loaded_modules = [ m.name for m in km.loaded() ]
    if u"thinkpad_acpi" in [ m.name for m in km.loaded()]:
        # module is loaded!
        # is it loaded with the right parameters?
        #/sys/module/thinkpad_acpi/parameters/fan_control # -> 
        # should point to "Y"!
        cfg = open("/sys/module/thinkpad_acpi/parameters/fan_control")   
        if cfg.readline().strip() != "Y":
            raise EnvironmentError("misconfigured")
            sys.exit(2)
    if u"coretemp" not in [ m.name for m in km.loaded()]:
        # module is not loaded!   
        raise EnvironmentError("Module 'coretemp is not loaded'")
        sys.exit(2)
    
    #cat /etc/modprobe.d/thinkfan.conf 
    #options thinkpad_acpi fan_control=1

    




if __name__ == "__main__":
    daemon = FanControlDaemon('/tmp/thinkpadfan.pid')
    if not os.getuid() == 0:
        print "You must be root to change fan speed."
        sys.exit(2)
        
    parser = argparse.ArgumentParser(description='Control the Fan of Lenovo \
    thinkpad x121e.',usage='%(prog)s start|stop|restart [-p|-d]')
    parser.add_argument('-p','--poll',help='Poll the tempratures, do nothing \
    real', action="store_true")
    parser.add_argument('-D','--NoDaemon', help='Do not fork, start in foreground', 
    action="store_true")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    action = sys.argv[1]
    
    if not 'start' == action and not 'stop' == action and not 'restart' == action:
        parser.print_help()
        sys.exit(1)

    sys.argv = sys.argv[1:]
    #print sys.argv
    args = parser.parse_args()
    
    if action == 'start' and args.NoDaemon:
        try:
            daemon.start()
        except KeyboardInterrupt:
            daemon.set_level("auto")
            daemon.stop()
    if action == "restart":
        daemon.restart()
    if action == "stop":
        daemon.set_level("auto")
        daemon.stop()
