#!/bin/bash

# not the best in the world, but does the job of preserving my gentoo installation
# mount your gentoo partition and back it up ...

tar czf ../gentoo.backup-`date +%Y-%m-%d`.tar.gz --exclude=./run \
	--exclude=./lost+found \
	--exclude=./tmp  \
	--exclude=./dev \
	--exclude=./proc \
	--exclude=./usr/portage/distfiles \
	--exclude=./usr/portage/packages \
	--exclude=./var/lib/docker \
	--exclude=./sys  .

