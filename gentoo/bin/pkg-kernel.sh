#!/bin/bash

# helper script to package the latest kernel installed
# This script assumes there is only one compiled version
# on disk

# This is like uname -r, but for the installed kernel
# no the one running
set -e
set +x

LATEST=`eselect kernel show | grep linux | cut -d"/" -f 4 | cut -d"-" -f 2`


echo $LATEST

cd /usr/src

tar czf linux-$LATEST.tar.gz \
	/boot/config-$LATEST-* \
	/boot/initramfs-genkernel-*-$LATEST-* \
        /boot/System.map-$LATEST-* \
        /boot/vmlinuz-$LATEST-* \
        /lib/modules/$LATEST-*
