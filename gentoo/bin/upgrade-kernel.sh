#!/bin/bash

# upgrade kernel the gentoo way - this assumes old config exists
set -e

KERNEL_VERSION=$1

emerge -1 =sys-kernel/$KERNEL_VERSION

IFS='-' read -a KVA <<< "${KERNEL_VERSION}"
cd /usr/src/linux-${KVA[2]}-gentoo

cp /usr/src/linux/.config .
make silentoldconfig
make -j3
make install
make INSTALL_MOD_STRIP=1 modules_install

eselect kernel --set $KERNEL_VERSION
genkernel --install initramfs
cp -v /boot/grub/grub.cfg /boot/grub/grub.cfg.bu_`date +%Y-%m-%d`
grub-mkconfig -o /boot/grub/grub.cfg
