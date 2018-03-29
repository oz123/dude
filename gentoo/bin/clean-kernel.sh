#!/bin/bash

# yuck eclean-kernel seems dead
# eclean-kernel2 is written in c++ and seems buggy

# Option strings
function usage(){
	echo >&2 \
	echo "usage: $0 [-v] [-k version ] ..."
	exit 1 ;
}

SHORT="vhk:"
LONG="verbose,help,kernel:"

OPTS=`getopt -o $SHORT --long $LONG -n $0 -- "$@" 2>/dev/null`

if [ $? != 0 ] ; then usage ; fi

eval set -- "$OPTS"

VERBOSE=false
declare -a KV

while true; do
  case "$1" in
    -v|--verbose ) VERBOSE=true; shift ;;
    -h|--help )    usage; shift ;;
    -k|--kernel )
       KV+=("${@:2}") ; shift;;
    --) shift; break ;;
    *) break ;;
  esac
done

if [ ${#KV[@]} -eq 0 ]; then
    usage
fi

KVC=()
for i in "${KV[@]}"; do
	[[ "$i" != "-v" ]] && [[ $i != "--" ]] && KVC+=( "$i" );
done

if [ "$VERBOSE" = true ] ; then
    RMO=vRf
else
    RMO=Rf
fi

function clean () {
    local VERSION=$1
    VI=$(NAMEVERSION="<category>/<name>-<version>\n" eix -I --format '<installedversions:NAMEVERSION>\n' sources | grep ${VERSION%%"-"*})
    if [ ! -z $VI ]; then
        emerge -Ca =$VI
    fi
    rm -${RMO} /usr/src/*$VERSION*

    rm -${RMO} /boot/*$VERSION*
    rm -${RMO} /lib/modules/*$VERSION*
}



for i in "${KVC[@]}"
do
   echo "Cleaning kernel version $i"
   clean "$i"
done
