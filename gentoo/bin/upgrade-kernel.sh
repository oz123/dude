#!/bin/bash

# upgrade kernel the gentoo way - this assumes old config exists
set -e

function trim() {
    local var="$*"
    # remove leading whitespace characters
    var="${var#"${var%%[![:space:]]*}"}"
    # remove trailing whitespace characters
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}

function emerge_latest(){
   LATEST=`equery m gentoo-sources | egrep  'Keywords:\s+4.9'| tail -1 | cut -d":" -f 2`
   LATEST=`trim ${LATEST}`
   emerge -1 =sys-kernel/gentoo-sources-${LATEST}
}


JOBS=${JOBS:-3}  # If variable not set, use default.
KERNEL_VERSION=$1

if [ -z ${KERNEL_VERSION} ]; then
    emerge_latest
    KERNEL_VERSION=${KERNEL_VERSION:-${LATEST}}
fi

cd /usr/src/linux-${KERNEL_VERSION}-gentoo

IFS='-' read -a KVA <<< "${KERNEL_VERSION}"
cd /usr/src/linux-${KVA[2]}-gentoo

cp /usr/src/linux/.config .
make silentoldconfig
make -j$JOBS
make install
make -j$JOBS INSTALL_MOD_STRIP=1 modules_install

eselect kernel --set linux-${KVA[2]}-gentoo
genkernel --install initramfs
cp -v /boot/grub/grub.cfg /boot/grub/grub.cfg.bu_`date +%Y-%m-%d`
grub-mkconfig -o /boot/grub/grub.cfg
emerge @module-rebuild
