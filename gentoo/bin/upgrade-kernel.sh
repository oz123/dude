#!/bin/bash

# upgrade kernel the gentoo way - this assumes old config exists
set -e

KERNEL_VERSION=$1

cd /usr/src/$KERNEL_VERSION

cp /usr/src/linux/.config .
make silentoldconfig
make -j3
make install
make INSTALL_MOD_STRIP=1 modules_install

eselect kernel --set $KERNEL_VERSION
genkernel --install initramfs
cp -v /boot/grub/grub.cfg /boot/grub/grub.cfg.bu_`date +%Y-%m-%d`
grub-mkconfig -o /boot/grub/grub.cfg
