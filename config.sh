#!/bin/sh
printf "Rentrez le chemin vers votre base de données keepass :\n"
set -f 
read -r rep
rep=$(echo "$rep" | sed "s|~|/home/$USER|")
#printf "%s" "$rep"
sed -i "s|path=\"\"|path=\"$rep\"|" keepread.py
sed -i "s|path=\"\"|path=\"$rep\"|" keepread-dmenu.py
cp keepread.py keepread-dmenu.py ~/.local/bin/
