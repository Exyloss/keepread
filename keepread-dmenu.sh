#!/bin/sh
sel_entry() {
    entry=$(echo "$1" | dmenu -p "utilisateur:" -l 10) || exit 1
    echo "$entry"
}
vals=$(keepread --list)
while :; do
    entry=$( sel_entry "$vals" ) || exit 1
    echo "$vals" | grep -q "$entry" || continue
    sel=""
    infos=$(keepread --username "$entry" --password "$entry" --totp "$entry")
    while [ "$sel" != "q" ]; do
        sel=$(echo "$infos" | dmenu -p "copier:" -l 10) || sel="q"
        sel=${sel#*:}
        [ "$sel" != "q" ] && echo "$sel" && py_keyboard.py "$sel"
    done
done
