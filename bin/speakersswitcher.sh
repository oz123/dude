#!/bin/bash

####
#  A small script to switch between bluetooth speakers and the laptop
#  speakers.
#  This script should work on Mate-Desktop or GNOME Desktop
#  Written by Oz Nahum Tiram <nahum oz at no no spampam gmail dot com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You can find a copy of this license at:
#  http://www.gnu.org/licenses/gpl-3.0.en.html
####


BIN="mateconftool-2"
# if using GNOME
# BIN="gconftool-2"

DIALOG=""

if [ -x /usr/bin/matedialog ]; 
	then
	DIALOG="/usr/bin/matedialog"
elif [ ! -L /usr/bin/zenity ]; 
	then
	DIALOG="/usr/bin/zenity"
fi

state=`${BIN} --get /system/gstreamer/0.10/default/musicaudiosink | cut -d"	" -f1`

if [  "${state}" == "autoaudiosink"  ] 
    then
     ${BIN} -t string -s /system/gstreamer/0.10/default/musicaudiosink \
    "alsasink device=bluetooth" 


	sed -i s/^[a]lsa\-audio\-device\=default/alsa\-audio\-device\=bluetooth/ ~/.config/vlc/vlcrc
	
	if [ ! -z $DIALOG ]; then	
		$DIALOG --info --title="GStreamer" --text="Switched to bluetooth speakers"
	fi

else
    ${BIN} -t string -s /system/gstreamer/0.10/default/musicaudiosink "autoaudiosink"
    
	sed -i s/^[a]lsa\-audio\-device\=bluetooth/alsa\-audio\-device\=default/ ~/.config/vlc/vlcrc
	
	if [ ! -z $DIALOG ]; then
		$DIALOG --info --title="GStreamer" --text="Switched to laptop speakers"  
	fi
fi
