#!/bin/bash

# not the best in the world, but does the job of preserving my gentoo installation
# mount your gentoo partition and back it up ...

ROOT=$2

DIROUT=$1


tar vczf $DIROUT/gentoo.backup-`date +%Y-%m-%d`.tar.gz \
	--exclude=${ROOT}run/media/* \
	--exclude=${ROOT}root/* \
	--exclude=${ROOT}run/* \
	--exclude=${ROOT}lost+found/* \
	--exclude=${ROOT}tmp/*  \
	--exclude=${ROOT}dev/* \
	--exclude=${ROOT}proc/* \
	--exclude=${ROOT}home/* \
	--exclude=${ROOT}mnt/* \
	--exclude=${ROOT}usr/portage/distfiles/* \
	--exclude=${ROOT}usr/portage/packages/* \
	--exclude=${ROOT}usr/src/* \
	--exclude=${ROOT}var/tmp/portage/* \
	--exclude=${ROOT}var/tmp/genkernel/* \
	--exclude=${ROOT}var/lib/docker/* \
	--exclude=${ROOT}var/lib/libvirt/ \
	--exclude=${ROOT}var/log/* \
	--exclude=${ROOT}sys/* ${ROOT}

