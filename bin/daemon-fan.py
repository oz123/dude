#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
   daemon-fan.py 
   
   Tested only on my LOUSY Lenove Thinkpad x121e, use at your own risk.
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
#  WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING 
#  
#  This program can FRY your COMPUTER! I am not to be held responsible if 
#  you trust this program for 100 precent without reading what it does!!!
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

# below 63 fan level is set to 0
# below 68 fan level is set to 1
# MAXTEMP_LEVEL = {63:0, 68:1, 69:2, 70:5, 75:7}
# the key is the maximum temperature allowed for fan level (value)
# max allowed temp: level 
# this configuration is pretty much usable without recharger!
# when charging the battery, the avg. temperature increases to 
# 69 degrees
# avg. temp. when laptop is idle (no cpu usage) is about 63.5
# celsius degrees


BASE_POLL_TIME_INTERVAL = 5
TEMP_SENSOR = "/proc/acpi/ibm/thermal"
FAN_INFO = "/proc/acpi/ibm/fan"
# below 63
MAXTEMP_LEVEL = {64:0, 66:1, 69:2, 70:5, 75:7}

class FanControlDaemon(Daemon):
    """
    define the FanControl Daemon and methods to:
    - manipulate fan speed.
    - determine temperatures
    - determine the fan speed
    - determine appropriate fan speed at right temp
    """
    def best_fan_level(self,c_fan_level,ctemp):
        """
        Determine the best fan speed based on temperature.
        In case fan level is auto, we need to find the right level to 
        start with ...
        """
        nearest_temp = min(MAXTEMP_LEVEL.keys(), key=lambda k: abs(k-ctemp))
        allowed_fan_level = MAXTEMP_LEVEL[nearest_temp]
        print "allowed ", allowed_fan_level
        #new_fan_level = 'auto'
        #print "!c_fan_lavel: %s, new_fan_level %s, ctemp %d, ntemp %d " % (c_fan_level, new_fan_level, ctemp, nearest_temp) 

        if ctemp <= nearest_temp and c_fan_level <= allowed_fan_level:
            print "T: %d L: %d  Tnear: %d Levelnear: %d, fan safe" % (ctemp, 
            c_fan_level, nearest_temp, allowed_fan_level)
            new_fan_level = c_fan_level
            print "new_fan_level modified in cond 1"
            
        if ctemp > nearest_temp:
            new_fan_level = allowed_fan_level+1
            print "new_fan_level modified in cond 2 ", new_fan_level
            if new_fan_level > c_fan_level:
                print "T: %d L: %d  Tnear: %d Levelnear: %d, New Level %d, fan increased" % (ctemp, 
            c_fan_level, nearest_temp, allowed_fan_level, new_fan_level)
            
            elif new_fan_level == c_fan_level:
                print "T: %d L: %d  Tnear: %d Levelnear: %d, fan safe*" % (ctemp, 
                c_fan_level, nearest_temp, allowed_fan_level)
    
        elif  c_fan_level > allowed_fan_level:
            new_fan_level = allowed_fan_level
            print "new_fan_level modified in cond 3 ", new_fan_level
            print "T1: %d L: %d  Tnear: %d Levelnear: %d, New Level %d, fan decreased" % (ctemp, 
            c_fan_level, nearest_temp, allowed_fan_level, new_fan_level)
         
        print "c_fan_lavel: %s, new_fan_level %s, ctemp %d, ntemp %d " % ( 
        c_fan_level, new_fan_level, ctemp, nearest_temp) 
        print '****'
        return new_fan_level
        
    def poll(self):
        """
        get the the tempratures
        """
        with open(TEMP_SENSOR) as ts:
            ts = ts.next()
            ts = re.search('\d+', ts)
            cputemp = ts.group()
        with open(FAN_INFO) as faninfo:
            faninfo = faninfo.readlines()
            faninfo = faninfo[2]
            if  'auto' in faninfo:
                fan_level = 1
            else:
                faninfo = re.search('\d+', faninfo)
                fan_level = faninfo.group()
        return fan_level, cputemp    
    
    def set_level(self,new_level):
        """
        set fan to new level
        """
        cmd = "echo \"level "+str(new_level)+"\" >"+FAN_INFO
        setcmd = sp.Popen(cmd, shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
        err, out = setcmd.communicate()
        
    def run(self):
        """
        execute the main fan control loop
        """
        while True:
            fanlevel, cpu_temp = self.poll()
            if fanlevel == 'auto':
                fanlevel = 0
            newlevel = self.best_fan_level(int(fanlevel), int(cpu_temp))
            self.set_level(newlevel)
            time.sleep(5)
    
    def check_proc(self):
        """
        check for pid file
        """
        # Check for a pidfile to see if the daemon already runs
        # instead opening self pidfile many times, we should just
        # set self.controlpid
        try:
            pf = open(self.pidfile,'r')
            proc = pf.read()
            pid = int(proc.strip())
            pf.close()
            return pid
        except IOError:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            
    def has_process(self):
        """
        go trough the processes tree and see if daemon.pid exists.
        if pid exists, and cli args for pid are the same as the 
        calling program it is safe to kill the program. 
        Hence, return some positive integer.
        Else, return negative. 
        If a positive integer is returned: the stop method
        will kill the process.
        If a negative integer is returned: it silently erases the file.
        """
        pid = self.check_proc()
        if pid:
            ptree = sp.Popen(['ps', '-eo' ,'pid,args'], stdout=sp.PIPE, 
                stderr=sp.PIPE)
            ptree, notused = ptree.communicate()
            ptree = ptree.splitlines()
            pids, cmds = zip(*[ line.lstrip().split(' ',1) for line in ptree ])
            try:
                idx = pids.index(str(pid))
                cmdlne = cmds[idx]
                # if cmdlne is the same as in the pid file, 
                if self.name in cmdlne:
                    return pid
                else:
                    idx = None
                    return idx
            except ValueError:
                idx = None
                return idx
        elif pid != None:
            print "%s in %s not found ..." % (pid, self.pidfile)
            return None
        
    def exit_running(self):
        """
        do not start if already running
        """
        if os.path.exists(self.pidfile):
            pf = open(self.pidfile,'r')
            proc = pf.read()
            running = int(proc.strip())
            message = "pidfile %s already exists. Daemon already running?\n"
            message += "check if process %d still exists\n"
            sys.stderr.write(message % (self.pidfile, running))
            sys.exit(1)
    
    def start(self):
        """
        Start in forground
        """
        self.exit_running()
        self.run()
    
    def startd(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        self.exit_running()
        #if not os.path.exists(self.pidfile):
            # Start the daemon
        self.daemonize()
            # after self.daemonize()
            # all output is redirected
        print open(self.pidfile).read()
        self.run()

    def stop(self):
        """
        Pranoid stop
        Stop the daemon, but only if pid has the right args.
        """
        pid = self.has_process()
        if pid > 0:
            # Try killing the daemon process    
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError, err:
                err = str(err)
                print err
                sys.exit(1)
        else:
            pass
            
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)
            
    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.startd()

def load_module(module_name, opts=''):
    """
    wrap around modprobe -i module_name
    """
    cmd = "modprobe -i %s %s" % module_name, opts
    modprobe = sp.Popen(cmd, shell=True)
    stat = modprobe.poll()
    if stat != 0:
        print "could not load module %s" % module_name
        sys.exit(2)

def chk_module_cfg(mname,syscfgfile, param):
    """
    check in /sys/module that the module was loaded with the correct
    parameters.
    e.g.
    /sys/module/thinkpad_acpi/parameters/fan_control # -> 
    should point to "Y"!
    """
    cfg = open(syscfgfile)   
    if cfg.readline().strip() != param:
        print "warning: %s is misconfigured ..." % mname
        return 1
    return 0

def perm_module_load(module_name):
    """
    add module to /etc/modules so that moduels load 
    at boot time.
    Is this unique to Debian?
    """
    with open('/etc/modules', 'a') as modules:
        modules.write(module_name+'\n')
        
def check_config():
    """
    this function checks that we can change the fan speed
    and that the correct modules are loaded 
    lsmod | grep coretemp
    lsmod | grep thinkpad_acpi
    grep /etc/modprobe.d/thinkfan.conf
    """        
    import kmod 
    km = kmod.Kmod()
    # first that we have the modules loades
    loaded_modules = [ m.name for m in km.loaded() ]  
    if u"thinkpad_acpi" not in loaded_modules:
        load_module("thinkpad_acpi", "fan_control=1")
    cfgval = chk_module_cfg("thinkpad_acpi",
    "/sys/module/thinkpad_acpi/parameters/fan_control", 'Y')
    if cfgval != 0:
        print "You should configure thinkpad_acpi with fan_control=1."
        print """
edit /etc/modprobe.d/thinkfan.conf to contain: 
options thinkpad_acpi fan_control=1 
Would you like to fix it now [Y/n]?
"""
        ans = raw_input()
        if ans.lower() == 'y':
            conf = open("/etc/modprobe.d/thinkfan.conf", 'a')
            conf.write('\noptions thinkpad_acpi fan_control=1\n')
            conf.close()    
        else:
            print "Refusing to continue... this could harm your computer..."
            print "You should really load thinkpad_acpi to run this script" 
            sys.exit(2)
        perm_module_load("thinkpad_acpi")
    if u"coretemp" not in loaded_modules:
        load_module("coretemp")
        #module is not loaded!   
        ans = 'Y'
        ans = raw_input("Module 'coretemp is not loaded', would you ", 
        "like to load it [Y/n] ?")
        if ans.lower() == 'y':
            #km.modprobe is broken
            load_module("coretemp")
            perm_module_load("core_temp")
        else:
            print "Refusing to continue... this could harm your computer..."
            print "You should really load thinkpad_acpi to run this script" 
            sys.exit(2)
        
if __name__ == "__main__":
    
    if not os.getuid() == 0:
        print "You must be root to change fan speed."
        sys.exit(2)
    
    parser = argparse.ArgumentParser(
    description="Control the Fan of Lenovo Thinkpad x121e.",
    usage='%(prog)s start|stop|restart|status [-p|-d]\n',
    )
    parser.add_argument('-p','--poll',help='Poll the tempratures, do nothing \
    real', action="store_true")
    parser.add_argument('-D','--NoDaemon', help='Do not fork, start in foreground', 
    action="store_true", default=False)

    ext_usage="""\n%s start - starts the fan control.
%s stop - stops the fan control, sets control mode to 'auto'.
%s status - check if the process is already running. 
""" % (parser.prog, parser.prog, parser.prog)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    action = sys.argv[1]
    
    
    
    if not 'start' == action and not 'stop' == action and not 'restart' == action \
        and not 'status' == action:
        parser.print_help()
        print ext_usage
        sys.exit(1)
    
    # check that everything is OK
    check_config()
    sys.argv = sys.argv[1:]
    
    args = parser.parse_args()
    
    daemon = FanControlDaemon(parser.prog,'/var/run/%s.pid' % parser.prog)
    if action == 'status':
        running = daemon.check_proc()
        if running:
            print "%s already runs with pid: %d" % (parser.prog, running)
    if action == 'start' and args.NoDaemon:
        try:
            daemon.start()
        except KeyboardInterrupt:
            daemon.set_level("auto")
            daemon.stop()
    if action == 'start' and not args.NoDaemon:
        daemon.startd()
    if action == "restart":
        daemon.restart()
    if action == "stop":
        daemon.set_level("auto")
        daemon.stop()

