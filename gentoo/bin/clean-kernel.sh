#!/bin/bash

# yuck eclean-kernel seems dead
# eclean-kernel2 is written in c++ and seems buggy

# Option strings
function usage(){
    echo >&2 "usage: $0 [-v] [-k version ] [-c|--clean]..."
    echo >&2 ""
    echo >&2 "OPTIONS:"
    echo >&2 "-c | --clean    execute make clean in each kernel sources directory"
    echo >&2 "-p | --purege   remove kernel package, sources, modules, installed files in /boot/"
    echo >&2 "-l | --list     list existing kernels in the system"
    echo >&2 "-g | --grub     update grub after removing kernels"
    exit 1 ;
}

SHORT="vhclk:p"
LONG="verbose,help,clean,list,kernel:"

OPTS=$(getopt -o "${SHORT}" --long "${LONG}" -n "$0" -- "$@" 2>/dev/null || usage)

eval set -- "$OPTS"

VERBOSE=false
CMD=""

declare -a KV

while true; do
  case "$1" in
    -v|--verbose )    VERBOSE=true ; shift ;;
    -h|--help    )    usage        ; shift ;;
    -p|--purge   )    CMD="purge"  ; shift ;;
    -l|--list    )    CMD="list"   ; shift ;;
    -c|--clean   )    CMD="clean"  ; shift ;;
    -g|--grub    )    CMD="clean"  ; shift ;;
    -k|--kernel  )
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
    VI=$(NAMEVERSION="<category>/<name>-<version>\n" eix -I --format '<installedversions:NAMEVERSION>\n' sources | grep ${VERSION%%"-"*} 2>/dev/null)
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

function update_grub() {
	printf  "\nBackup grub configuration\n"
	cp -v /boot/grub/grub.cfg /boot/grub/grub.cfg-$(date +%Y-%m-%dT%H%M)
	printf  "\nUpdating grub configuration\n"
	grub-mkconfig -o /boot/grub/grub.cfg
}

function list() {
    local sysmaps
    local configs
    local modules
    # systesmaps in /boot/
    sysmaps=( $( ls /boot/System.map-*| cut -d"-" -f 2- ) )
    # kernel config in /boot/
    configs=( $(ls /boot/config-* | cut -d"-" -f 2-) )
    # modules in /lib/modules
    modules=( $(basename -a $(ls -d /lib/modules/* | cut -d"-" -f 1-)) )
    # kernel images in /boot
    images=( $(ls /boot/vmlinuz-* | cut -d"-" -f 2-) )
    # sources in /usr/src
    sources=( $(ls -d /usr/src/linux-* | cut -d"-" -f2-) )

    local rows=${#sysmaps[*]}
    if [ ${#configs[*]} -gt $rows ]; then rows=${#configs[*]}; fi
    if [ ${#modules[*]} -gt $rows ]; then rows=${#modules[*]}; fi
    if [ ${#images[*]}  -gt $rows ]; then rows=${#modules[*]}; fi
    if [ ${#sources[*]} -gt $rows ]; then rows=${#modules[*]}; fi

    printf "%-20s| Sysmap | Config | Image | Modules | Sources |\n" Kernel
    for i in $(seq 0 $(( $rows - 1))); do
        has_sysmap="-"
        has_config="-"
        has_image="-"
        has_modules="-"
        has_source="-"
        if [[ "${sysmaps[*]}" =~ ${modules[$i]} ]]; then has_sysmap="+" ; fi
        if [[ "${configs[*]}" =~ ${modules[$i]} ]]; then has_config="+" ; fi
        if [[ "${images[*]}"  =~ ${modules[$i]} ]]; then has_image="+" ; fi
        if [[ "${modules[*]}" =~ ${modules[$i]} ]]; then has_modules="+" ; fi
        if [[ "${sources[*]}" =~ ${modules[$i]} ]]; then has_source="+" ; fi

        printf '%0.1s' "-"{1..66}
        printf '|\n'
        printf "%-20s|   %s    |   %s    |   %s   |    ${has_modules}   |     ${has_source}    | \n" ${modules[$i]} $has_sysmap $has_config $has_image
    done
    printf '%0.1s' "-"{1..66}
    printf '|\n'
}

if [ x${CMD} == x"clean" ]; then
    clean_all
elif [ x${CMD} == x"list" ]; then
    list
    exit 0
fi

for i in "${KVC[@]}"
do
   echo "purge kernel version $i"
   purge "$i"
done

# vim: set softtabstop=4 tabstop=4 expandtab shiftwidth=4:
