#!/bin/bash

# upgrade kernel the gentoo way - this assumes old config exists
set -e
set -x

function trim() {
    local var="$*"
    # remove leading whitespace characters
    var="${var#"${var%%[![:space:]]*}"}"
    # remove trailing whitespace characters
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}

function emerge_latest(){
   local KV=$(uname -r)
   local MAJOR=${KV%.[[:digit:]]*} # extract 4.9 from 4.9.XY
   LATEST=`equery m gentoo-sources | egrep  "Keywords:\s+${MAJOR}"| tail -1 | cut -d":" -f 2`
   LATEST=`trim ${LATEST}`
   echo "=sys-kernel/gentoo-sources-${LATEST} ~amd64" > /etc/portage/package.accept_keywords/kernel
   emerge -n1 =sys-kernel/gentoo-sources-${LATEST}
}


function copy_config(){
	cd /usr/src/linux-${KERNEL_VERSION}-gentoo

	if [ -r /usr/src/linux/.config ]; then
		cp /usr/src/linux/.config .
	else
		cp /boot/config-`uname -r` .config
	fi
}

function build_all(){

	make silentoldconfig
	make -j$JOBS vmlinux bzImage
	make -j$JOBS modules
	make install
	make -j$JOBS INSTALL_MOD_STRIP=1 modules_install
}

function install_kernel(){
	eselect kernel --set linux-${KERNEL_VERSION}-gentoo

	# optionally build an initramfs
	if [ ! -z ${WITH_INITRAM_FS} ]; then
		genkernel --install initramfs
	fi

	cp -v /boot/grub/grub.cfg /boot/grub/grub.cfg.bu_`date +%Y-%m-%d`
	grub-mkconfig -o /boot/grub/grub.cfg
	emerge @module-rebuild

}

JOBS=${JOBS:-3}  # If variable not set, use default.
KERNEL_VERSION=$1
WITH_INITRAM_FS=""

if [ -z ${KERNEL_VERSION} ]; then
    emerge_latest
    KERNEL_VERSION=${KERNEL_VERSION:-${LATEST}}
fi

copy_config
build_all
install_kernel
