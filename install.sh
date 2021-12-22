#!/bin/sh
[ "$1" = "" ] && echo "Erreur : veuillez renseigner le chemin vers votre base de données en argument." && exit 1
ans=$(echo "$1" | sed "s|~|/home/$USER|")
cp keepread.py ~/.local/bin/keepread
cp keepread-dmenu.py ~/.local/bin/keepread-dmenu
cp totp.sh ~/.local/bin
sed -i "s|path=\"\"|path=\"$ans\"|" ~/.local/bin/keepread
sed -i "s|path=\"\"|path=\"$ans\"|" ~/.local/bin/keepread-dmenu
