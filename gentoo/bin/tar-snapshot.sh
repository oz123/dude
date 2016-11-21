#!/bin/bash

# not the best in the world, but does the job of preserving my gentoo installation
# mount your gentoo partition and back it up ...

DIROUT=$1

tar czf $DIROUT/gentoo.backup-`date +%Y-%m-%d`.tar.gz --exclude=./run \
	--exclude=./lost+found \
	--exclude=./tmp  \
	--exclude=./dev \
	--exclude=./proc \
	--exclude=./home \
	--exclude=./usr/portage/distfiles \
	--exclude=./usr/portage/packages \
	--exclude=./var/lib/docker \
	--exclude=./sys  .

