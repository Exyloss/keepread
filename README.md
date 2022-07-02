# KeepRead
## Dépendances
 - [python](https://python.org)
 - python-pip
 - [dmenu](https://tools.suckless.org/dmenu/) (avec le patch "[password](https://tools.suckless.org/dmenu/patches/password/)")
 - [pykeepass](https://github.com/libkeepass/pykeepass) (pip install pykeepass)
 - notify-send
 - [mintotp](https://github.com/susam/mintotp) (installer avec pip)
 - gnome-keyring (optionel)

## Utiliser les programmes

Lancez le script install.sh pour modifier la variable "path" et pour installer les programmes.
Lancez 
```
export $(gnome-keyring-daemon --start)
keyring-startup.sh &
```
au lancement de votre système si vous souhaitez utiliser le keyring afin de sauvegarder le mot de passe.

## Fonctionnement
Le script utilisant dmenu utilise le clavier pour rentrer un mot de passe, donc lorsque vous souhaitez rentrer un mot de passe, votre
curseur doit se trouver dans le champ de saisie du mot de passe.
