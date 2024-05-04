# KeepRead
## Dépendances
 - [python](https://python.org)
 - [dmenu](https://tools.suckless.org/dmenu/) (avec le patch [password](https://tools.suckless.org/dmenu/patches/password/))
 - [pykeepass](https://github.com/libkeepass/pykeepass)
 - [mintotp](https://github.com/susam/mintotp)
 - [gnome-keyring](https://gitlab.gnome.org/GNOME/gnome-keyring) (optionel)
 - [fzy](https://github.com/jhawthorn/fzy)

## Utiliser les programmes
Installer les dépendances python :
```
pip install -r requirements.txt
```
Lancez le script install.sh pour initialiser la configuration et pour installer les programmes.

Lancez aussi
```
systemctl --user enable --now gnome-keyring-daemon
```
au démarrage de votre serveur X si vous souhaitez utiliser le keyring afin de sauvegarder le mot de passe de votre base de données.

Pour activer le keyring, lancez la commande suivante dans un shell et rentrez votre mot de passe :
```
keyring system keepass
```

## Fonctionnement
Le script utilisant dmenu utilise le clavier pour rentrer un mot de passe, donc lorsque vous souhaitez rentrer un mot de passe dans un champ, votre
curseur doit se trouver dans le champ de saisie du mot de passe.
