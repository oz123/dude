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
        check for pid file, create pid file
        """
        # Check for a pidfile to see if the daemon already runs
        # instead opening self pidfile many times, we should just
        # set self.controlpid
        try:
            pf = open(self.pidfile,'r')
            proc = pf.read()
            pid = int(proc.strip())
            pf.close()
        except IOError:
            pid = None
            return pid
        if pid:
            return pid
    
    def has_process(self):
        """
        go trough the processes tree and see if daemon.pid exists.
        # if not silently erase the file
# if pid exists as a process and the command line args are really daemon-fan.py
       
        #process = Popen(['ps', '-eo' ,'pid,args'], stdout=PIPE, stderr=PIPE)
#stdout, notused = process.communicate()
#
#    pid, cmdline = line.split(' ', 1)
    #Do whatever filtering and processing is needed
# [ line for line in stdout.splitlines() ]
# pids, cmds = zip(*[ line.split() for line in stdout.splitlines() ])
# stop method
# if not silently erase the file
# if pid exists as a process and the command line args are really daemon-fan.py
        """
        pid = self.check_proc()
        if pid:
            ptree = sp.Popen(['ps', '-eo' ,'pid,args'], stdout=sp.PIPE, 
                stderr=sp.PIPE)
            ptree, notused = ptree.communicate()
            ptree = ptree.splitlines()
            pids, cmds = zip(*[ line.split(' ',1) for line in ptree ])
            try:
                idx = pids.index(pid)
                cmdlne = cmds[idx]
                # if cmdlne is the same as in the pid file, 
                # return ok
                # when ok, the next method self.stop()
                # can kill the process
            except ValueError:
                idx = None
                cmd = None
        
        else:
            return None
    def exit_running(self):
        """
        do not start if already running
        """
        running = self.check_proc()
        if running:
            message = "pidfile %s already exists. Daemon already running?\n"
            message += "check if process %d still exists\n"
            sys.stderr.write(message % (self.pidfile, running))
            sys.exit(1)
    
    def start(self):
        """
        Start in forground
        """
        self.exit_running()
        #pid = str(os.getpid())
        #print "[pid: %s , cli: %s]" % (pid, self.name)
        #open(self.pidfile,'w+').write("%s %s\n" % (pid, self.name))
        self.run()
    
    def startd(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        self.exit_running()
        # Start the daemon
        self.daemonize()
        # after self.daemonize()
        # all output is redirected
        print open(self.pidfile).read()
        self.run()

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
        

# todo: before killing the process make sure will kill the right process
# todo: before erasing the file try killing the process



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


#process = Popen(['ps', '-eo' ,'pid,args'], stdout=PIPE, stderr=PIPE)
#stdout, notused = process.communicate()
#for line in stdout.splitlines():
#    pid, cmdline = line.split(' ', 1)
    #Do whatever filtering and processing is needed
# [ line for line in stdout.splitlines() ]
# pids, cmds = zip(*[ line.split() for line in stdout.splitlines() ])
# stop method
# if pid exists as a process and the command line args are really daemon-fan.py
#    kill that process
#    than erase the file
# if not silently erase the file

#>>> process = sp.Popen(['ps', '-eo' ,'pid,args'], stdout=sp.PIPE, stderr=sp.PIPE)
#>>> stdout, notused = process.communicate()
#>>> 
#>>> pids
#('PID', '1', '2', '3', '6', '7', '21', '22', '23', '24', '25', '26', '27', '28', '32', '33', '34', '35', '36', '37', '121', '154', '172', '173', '174', '175', '176', '177', '228', '229', '356', '570', '578', '600', '606', '752', '1508', '1509', '1784', '1815', '1820', '1822', '1851', '1878', '1952', '2230', '2310', '2327', '2372', '2493', '2607', '2643', '2679', '2808', '2835', '2866', '2883', '2910', '2930', '2931', '2958', '3140', '3286', '3305', '3349', '3350', '3397', '3412', '3444', '3468', '3472', '3476', '3540', '3543', '3544', '3556', '3726', '3727', '3728', '3729', '3730', '3731', '3733', '3740', '3881', '3919', '3920', '3928', '3975', '3977', '3980', '4000', '4003', '4004', '4014', '4020', '4025', '4030', '4032', '4036', '4038', '4041', '4043', '4045', '4047', '4050', '4051', '4052', '4054', '4055', '4059', '4067', '4076', '4078', '4079', '4081', '4082', '4108', '4203', '4211', '4218', '4310', '4337', '4352', '4395', '4459', '4791', '5973', '6208', '6539', '6541', '6542', '6543', '6544', '6545', '6546', '6547', '6548', '6549', '6550', '6600', '6601', '6602', '6605', '6608', '6610', '7079', '7094', '7129', '7664', '7672', '7758', '7803', '7915', '8019', '8020', '8227', '8625', '9004', '9077', '9330', '9356', '9694', '10044', '13327', '13328', '13336', '13708', '13713', '16990', '17270', '18732', '18993', '18994', '19002', '19373', '19554', '19655', '19662', '19670', '19674', '19675', '19681', '19682', '20897', '20986', '23787', '24186', '24190', '27355', '28721', '29105', '29312', '29313', '29314', '29315', '29316', '29520', '30019', '30026', '31332', '31916', '31929')
