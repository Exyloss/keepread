#!/bin/sh
[ "$1" = "" ] && echo "Erreur: veuillez renseigner le chemin vers votre base de données en argument." && exit 1
mkdir "$XDG_CONFIG_HOME"/keepread
cp config.ini "$XDG_CONFIG_HOME"/keepread/config.ini
sed -i "s|^path=$|path=$1|" "$XDG_CONFIG_HOME"/keepread/config.ini && echo "La configuration a bien été appliquée."

./combine.sh kr kr.py clip_linux.py keeplib.py
./combine.sh dkr dkr.py clip_linux.py keeplib.py
mv kr dkr ~/.local/bin
cp totp.sh ~/.local/bin
cp mintotp/mintotp ~/.local/bin
