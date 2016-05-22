# This script is used to the change the backlight on a
# UX303L ASUS Laptop, because the built in function keys don't 
# worki with linux kernel 4.2 (at least on Ubuntu 14.04).

# This script is a free software distributed under the terms
# of the GPL v3 or later. 

# Copyright 2016 Oz Nahum Tiram <Oz N Tiram>

#!/bin/bash

LC_NUMERIC="en_US.UTF-8"

function round {
	printf "%.$2f" $1
}



DATA_STORE=/sys/class/backlight/intel_backlight/brightness

LEVEL=`cat $DATA_STORE`
echo $LEVEL
L=/tmp/log
while getopts ":ri" opt; do
	case $opt in
		r)
		    NL=`bc <<< "0.9*$LEVEL"`
			tee $DATA_STORE <<< $(round $NL 0)

			;;
		i)  			
			
		    NL=$(bc <<< "1.1*$LEVEL")
			echo $NL >> $L
			tee $DATA_STORE <<< $(round $NL 0)
			;;
		\?) 
			;;
	esac
done

