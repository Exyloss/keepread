#!/bin/sh
[ "$1" = "" ] && echo "Erreur : veuillez renseigner le chemin vers votre base de données en argument." && exit 1
sed -i "s|^path=$|path=$1|" "$XDG_CONFIG_HOME"/keepread/config.ini
mkdir "$XDG_CONFIG_HOME"/keepread 2>/dev/null
printf "Copier le fichier de config initial (O/n) : "
set -f
read -r ans
case "$ans" in
    "o"|"O")
        cp config.ini "$XDG_CONFIG_HOME"/keepread/config.ini && echo "La configuration a bien été appliquée." ;;
    *)
        echo "Aucuns changements ne seront effecutés sur le fichier de config."
esac
cp kr.py ~/.local/bin/kr
cp dkr.py ~/.local/bin/dkr
cp totp.sh ~/.local/bin
