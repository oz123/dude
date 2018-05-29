#!/bin/bash

# yuck eclean-kernel seems dead
# eclean-kernel2 is written in c++ and seems buggy

# Option strings
function usage(){
	echo >&2 \
	echo "usage: $0 [-v] [-k version ] [-c|--clean]..."
	exit 1 ;
}

SHORT="vhk:c"
LONG="verbose,help,kernel:,clean"

OPTS=`getopt -o $SHORT --long $LONG -n $0 -- "$@" 2>/dev/null`

if [ $? != 0 ] ; then usage ; fi

eval set -- "$OPTS"

VERBOSE=false
CMD=""

declare -a KV

while true; do
  case "$1" in
    -v|--verbose ) VERBOSE=true; shift ;;
    -h|--help )    usage; shift ;;
    -c|--clean) CMD="clean"; shift;;
    -k|--kernel )
       KV+=("${@:2}") ; shift; shift ;;
    --) shift; break ;;
    *) usage ;;
  esac
done

#if [ ${#KV[@]} -eq 0 ]; then
#    usage
#fi

KVC=()
for i in "${KV[@]}"; do
	[[ "$i" != "-v" ]] && [[ $i != "--" ]] && KVC+=( "$i" );
done

if [ "$VERBOSE" = true ] ; then
    RMO=vRf
else
    RMO=Rf
fi

function purge () {
    local VERSION=$1
    VI=$(NAMEVERSION="<category>/<name>-<version>\n" eix -I --format '<installedversions:NAMEVERSION>\n' sources | grep ${VERSION%%"-"*})
    if [ ! -z $VI ]; then
        emerge -C =$VI
    fi
    echo "Removing sources for ${VERSION}"
    rm -${RMO} /usr/src/*$VERSION*


    echo "Removing built kernel for ${VERSION}"
    rm -${RMO} /boot/*$VERSION*

    echo "Removing built modules for ${VERSION}"
    rm -${RMO} /lib/modules/*$VERSION*
}


function clean_all () {
    local VERSIONS=$(find /usr/src/ -name "linux-*" -type d | grep -v $(readlink /usr/src/linux))
    for item in ${VERSIONS}; do
        make -C $item clean;
    done
}

if [ x${CMD} == x"clean" ]; then
    clean_all
fi

for i in "${KVC[@]}"
do
   echo "purge kernel version $i"
   purge "$i"
done
