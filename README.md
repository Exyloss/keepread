# KeepRead
## Dépendances
 - [python](https://python.org)
 - python-pip
 - [dmenu](https://tools.suckless.org/dmenu/) (avec le patch "[password](https://tools.suckless.org/dmenu/patches/password/)")
 - [pykeepass](https://github.com/libkeepass/pykeepass) (pip install pykeepass)
 - notify-send

## Utiliser le script

Éditez la variable "path" et renseignez-y le chemin absolu (avec /home/user/...) vers votre base de donnnées KeePass.
Puis, lancez le script install.sh pour installer les programmes.

## Fonctionnement
Le script utilisant dmenu utilise le clavier pour rentrer un mot de passe, donc lorsque vous souhaitez rentrer un mot de passe, votre
curseur doit se trouver dans le champ de saisie du mot de passe.
