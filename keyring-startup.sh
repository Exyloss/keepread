#!/bin/sh
while [ "$DISPLAY" = "" ]; do
    :
done
/etc/X11/xinit/xinitrc.d/50-systemd-user.sh && exit 0
