#!/bin/bash
lo=`setxkbmap -query | grep lay | cut -d : -f 2| sed 's/^ *//g'`

case $lo in
    "il" )
        setxkbmap de ;;
    "de" )
        setxkbmap us ;;
    "us" )
        setxkbmap il ;;
esac
