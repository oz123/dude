#!/bin/bash

# yuck eclean-kernel seems dead
# eclean-kernel2 is written in c++ and seems buggy

# USAGE: $script 4.9.72-gentoo
KV=$1

rm -vRf /boot/*$KV
rm -vRf /lib/modules/*$KV*


VI=$(NAMEVERSION="<category>/<name>-<version>\n" eix -I --format '<installedversions:NAMEVERSION>\n' sources | grep ${KV%%"-"*})
if [ ! -z $VI]; then
    emerge -Ca =$VI
fi
rm -vRf /usr/src/*$KV*
