#!/bin/sh
[ "$1" = "" ] && echo "Erreur : veuillez renseigner le chemin vers votre base de données en argument." && exit 1
sed -i "s|path=|path=$1|" config.ini
echo "Souhaitez-vous utiliser une application de keyring ? (o/n)"
set -f
read ans2
[ "$ans2" = "o" ] && sed -i "s|keyring=|keyring=True|" config.ini
echo "Fichier de config:"
cat config.ini
cp keepread.py ~/.local/bin/keepread
cp keepread-dmenu.py ~/.local/bin/keepread-dmenu
cp totp.sh ~/.local/bin
mkdir "$XDG_CONFIG_HOME"/keepread 2>/dev/null
cp config.ini "$XDG_CONFIG_HOME"/keepread/
