#!/bin/bash

# yuck eclean-kernel seems dead
# eclean-kernel2 is written in c++ and seems buggy

set -e
# Option strings
SHORT=vk:
LONG=verbose,kernel:

# read the options
OPTS=$(getopt --options $SHORT --long $LONG --name "$0" -- "$@" 2>/dev/null)

function usage(){
	echo >&2 \
	echo "usage: $0 [-v] [-k version] version ..."
	exit 1 ;
}

RES=$?
if [ $RES != 0 ] ; then
	usage
fi

eval set -- "$OPTS"

# set initial values
VERBOSE=false

# extract options and their arguments into variables.
while true ; do
  case "$1" in
    -v | --verbose )
      VERBOSE=true
      shift
      ;;
    -k | --kernel )
      KV="$2"
      shift 2
      ;;
    -- )
      shift
      break
      ;;
    *)
      echo "Internal error!"
      exit 1
      ;;
  esac
done

if [ -z ${KV} ]; then
	usage
fi

if [ "$VERBOSE" = true ] ; then
    RMO=vRf
else
    RMO=Rf
fi

rm -${RMO} /boot/*$KV*
rm -${RMO} /lib/modules/*$KV*


VI=$(NAMEVERSION="<category>/<name>-<version>\n" eix -I --format '<installedversions:NAMEVERSION>\n' sources | grep ${KV%%"-"*})
if [ ! -z $VI ]; then
    emerge -Ca =$VI
fi
rm -${RMO} /usr/src/*$KV*
