# use this script to initialize work on gentoo install
# this is the base for fully installing automatically
# we still have lot's of work to do ...

# mount everything needed for a working chroot
set -e
function mount_all(){
	echo $1
	mount $1 /mnt/gentoo
	mount -t proc proc /mnt/gentoo/proc
	mount --rbind /sys /mnt/gentoo/sys
	mount --make-rslave /mnt/gentoo/sys
	mount --rbind /dev /mnt/gentoo/dev
	mount --make-rslave /mnt/gentoo/dev
	mount --bind /dev/shm /mnt/gentoo/dev/shm
        mount --bind /dev/pts /mnt/gentoo/dev/pts
	for dr in /mnt/gentoo/ /mnt/gentoo/run /mnt/gentoo/run/udev; do
		if [ ! -d $dr ]; then
			mkdir -p $dr
		fi
	done
        mount --bind /run/udev /mnt/gentoo/run/udev
}

# clean up after exiting chroot
function unmount_all(){
	umount -l /mnt/gentoo/proc
	umount -l /mnt/gentoo/sys
	umount -l /mnt/gentoo/dev/shm
	echo $1
	if [[ $1 =~ "LABEL" ]]; then
		# extact everything after =
		VOL=`blkid -L ${1#*=}`
		umount -l $VOL
	else
		umount -l $1
	fi

}

# run the script with LABEL=GENTOO or /dev/sda6 as the first parameter
if [ -z $1 ]; then
	echo "please run again with `basename $0` partition-to-mount"
	exit 1;
fi


function mount_resolvconf(){
	if [ -L /etc/resolv.conf ]; then
                touch /mnt/gentoo/etc/resolv.conf
		mount --bind /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
	else
		cat /etc/resolv.conf > /mnt/gentoo/etc/resolv.conf
	fi
}

mount_all $1
mount_resolvconf
chroot /mnt/gentoo/ /bin/bash --rcfile /.bashrc 
unmount_all $1
