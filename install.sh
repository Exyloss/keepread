#!/bin/sh
[ "$1" = "" ] && echo "Erreur : veuillez renseigner le chemin vers votre base de données en argument." && exit 1
mkdir "$XDG_CONFIG_HOME"/keepread 2>/dev/null
cp config.ini "$XDG_CONFIG_HOME"/keepread/
sed -i "s|^path=$|path=$1|" "$XDG_CONFIG_HOME"/keepread/config.ini
printf "Souhaitez-vous utiliser une application de keyring (oui par défaut) ? (o/n) "
set -f
read ans2
[ "$ans2" = "o" ] && sed -i "s|^keyring=$|keyring=True|" "$XDG_CONFIG_HOME"/keepread/config.ini || sed -i "s|keyring=|keyring=False|" "$XDG_CONFIG_HOME"/keepread/config.ini
printf "Serveur graphique (wayland par défaut) : "
set -f
read graphic
sed -i "s|^graphic=$|graphic=$graphic|" "$XDG_CONFIG_HOME"/keepread/config.ini
printf "Menu (bemenu par défaut) : "
set -f
read menu
sed -i "s|^menu=$|menu=$menu|" "$XDG_CONFIG_HOME"/keepread/config.ini
echo "Fichier de config:"
cat "$XDG_CONFIG_HOME"/keepread/config.ini
cp kr.py ~/.local/bin/kr
cp dkr.py ~/.local/bin/dkr
cp totp.sh ~/.local/bin
