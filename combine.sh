#!/bin/sh
# Utilisation: ./combine.sh programme_sortie script_principal.py dependance1.py [dependance2.py...]

[ "$1" = "" ] && exit 1
[ -f "$1" ] && exit 1

program_name="$1"
shift

main_file="$1"
shift

project_dir=$(pwd)
temp_dir=$(mktemp -d)
cp "$main_file" "${temp_dir}/__main__.py"

# On copie les dépendances dans le dossier temporaire
for i in "$@"
do
    cp "$i" "${temp_dir}/"
done

# On rassemble le programme principal et ses dépendances dans un seul fichier zippé
cd "$temp_dir" || exit 1
zip -r "${project_dir}/${program_name}.zip" ./*

# Ajout du shebang au début du zip et on rend le programme exécutable
cd "$project_dir" || exit 1
echo '#!/usr/bin/env python3' | cat - "$program_name".zip > "$program_name"
chmod a+x "$program_name"

# Nettoyage
rm "$program_name".zip
rm -rf "$temp_dir"
