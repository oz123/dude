#!/bin/bash

# not the best in the world, but does the job of preserving my gentoo installation
# mount your gentoo partition and back it up ...

tar czf ../gentoo.backup-08-Sep-2016.tar.gz --exclude=./run \
	--exclude=./lost+found \
	--exclude=./tmp  \
	--exclude=./dev \
	--exclude=./proc \
	--exclude=./usr/portage/distfiles \
	--exclude=./usr/portage/packages \
	--exclude=./var/lib/docker \
	--exclude=./sys  .

