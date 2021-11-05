#!/bin/sh
printf "Veuillez renseigner un chemin vers votre base de données.\n"
set -f
read ans
[ "$ans" = "" ] && exit 1
ans=$(echo "$ans" | sed "s|~|/home/$USER|")
cp keepread.py ~/.local/bin/keepread
cp keepread-dmenu.py ~/.local/bin/keepread-dmenu
cp totp.sh ~/.local/bin
sed -i "s|path=\"\"|path=\"$ans\"|" ~/.local/bin/keepread
sed -i "s|path=\"\"|path=\"$ans\"|" ~/.local/bin/keepread-dmenu
