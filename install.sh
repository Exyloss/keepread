#!/bin/sh
is_empty=$(grep "path=\"\"" keepread.py)
[ "$is_empty" != "" ] && printf "Vous n'avez pas renseigné de base de données." && exit 1
is_empty=$(grep "path=\"\"" keepread-dmenu.py)
[ "$is_empty" != "" ] && printf "Vous n'avez pas renseigné de base de données." && exit 1
cp keepread.py ~/.local/bin/keepread
cp keepread-dmenu.py ~/.local/bin/keepread-dmenu
