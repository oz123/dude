General notes
=============

To enable boot logging with openrc:

```
sudo sed -i /rc_logger="NO"/rc_logger="YES"/ /etc/rc.conf
```

Logging
-------

 - install syslog-ng and logrotate
 

KVM
---

in `/lib64/elogind/system-sleep/suspend-vms.sh`: 
```
#!/bin/bash

case $1/$2 in
  pre/*)
    for vm in $(virsh list --name) ; do virsh suspend --domain $vm; done
    ;;
  post/*)
    # Put here any commands expected to be run when resuming from suspension or thawing from hibernation.
    for vm in $(virsh list --name) ; do virsh resume --domain $vm; done
    ;;
esac
```
