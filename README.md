# KeepRead
## Dépendances
 - [python](https://python.org)
 - python-pip
 - [dmenu](https://tools.suckless.org/dmenu/) (avec le patch "[password](https://tools.suckless.org/dmenu/patches/password/)")
 - [pykeepass](https://github.com/libkeepass/pykeepass) (pip install pykeepass)
 - notify-send
 - [mintotp](https://github.com/susam/mintotp) (installer avec pip)
 - kwallet (optionel)

## Utiliser les programmes

Lancez le script install.sh pour modifier la variable "path" et pour installer les programmes.
Lancez kwalletd5 en fond de tâche si vous souhaitez utiliser le keyring afin de sauvegarder le mot de passe.

## Fonctionnement
Le script utilisant dmenu utilise le clavier pour rentrer un mot de passe, donc lorsque vous souhaitez rentrer un mot de passe, votre
curseur doit se trouver dans le champ de saisie du mot de passe.
