#!/usr/bin/env python3
from pykeepass import PyKeePass as pkp
from random import randint
import subprocess

def prompt_sel(args, items):
    """
    Fonction permettant à l'utilisateur d'interagir avec son menu depuis python
    args: commande sous forme de tableau, chaque élément représente un "mot" de la fonction
    items: liste des valeurs à afficher
    """
    if items != "":
        try:
            proc = subprocess.Popen(
                args,
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        except OSError as err:
            print("erreur lors du lancement du menu")

        with proc.stdin:
            if isinstance(items, list):
                for item in items:
                    proc.stdin.write(item)
                    proc.stdin.write('\n')
            elif isinstance(items, str):
                proc.stdin.write(items)
    else:
        proc = subprocess.Popen(args)

    if proc.wait() == 0:
        return proc.stdout.read().rstrip('\n')

    stderr = proc.stderr.read()

    if stderr == '':
        return -1

def pass_gen(size=12, spe=True):
    """
    Générateur de mots de passe, prend comme arguments :
    size: longueur du mot de passe
    spe: inclure les caractères spéciaux (booléen)
    retourne un mot de passe
    """
    try:
        chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if spe:
            chars += "&?,.;/:!#@+-*=_()[]çàéè~^$%ù"
        len_chars=len(chars)
        passwd = ""
        for i in range(size):
            passwd += chars[randint(0,len_chars-1)]
        return passwd
    except:
        return 1


def search_entry(kp, arg):
    """
    Fonction utilisée par kr.py et dkr.py afin d'obtenir la première occurence
    kp: base de données keepass (objet PyKeePass)
    arg: valeur recherchée
    """
    entry = kp.find_entries(title=arg, first=True)
    if entry == None:
        return 1
    else:
        return entry


def del_entry(kp, entry):
    """
    Fonction supprimant l'entrée spécifiée en argument de la base de données renseignée
    kp: base de données keepass (objet PyKeePass)
    entry: objet entry de PyKeePass
    """
    try:
        kp.delete_entry(entry)
        kp.save()
        return 0
    except:
        return 1

def edit_entry(kp, entry, uname, passwd, title):
    """
    commande éditant l'entrée spécifiée avec différentes valeurs :
    kp: base de données de l'entrée
    entry: objet entry
    uname: nouveau nom d'utilisateur
    passwd: nouveau mot de passe
    title: nouveau titre
    """
    try:
        kp.add_entry(entry.group, title, uname, passwd)
        kp.delete_entry(entry)
        kp.save()
        return 0
    except:
        return 1

def create_entry(kp, group, title, uname, passwd):
    """
    commande créant une entrée avec différentes valeurs :
    kp: base de données de l'entrée
    group: groupe de l'entrée
    uname: nouveau nom d'utilisateur
    passwd: nouveau mot de passe
    title: nouveau titre
    """
    try:
        g = kp.find_groups(name=group, first=True)
        if g == None:
            g = kp.root_group
        kp.add_entry(g, title, uname, passwd)
        kp.save()
        return 0
    except:
        return 1

def get_entries(kp):
    """
    Fonction listant les entrées présentes dans la base de données kp.
    kp: Objet PyKeePass
    """
    e = kp.find_entries(title=".*", regex=True)
    entries = []
    for i in e:
        if i.group.name != 'Corbeille' and i.title != None:
            entries.append(i.title)
    return entries

def get_groups(kp):
    """
    Fonction listant les groupes présents dans la base de données kp.
    kp: Objet PyKeePass
    """
    e = kp.find_groups(name=".*", regex=True)
    entries = []
    for i in e:
        if i.name != 'Corbeille':
            entries.append(i.name)
    return entries

def entry_values(entry):
    """
    Fonction utilisée par kr.py et dkr.py afin d'obtenir les données
    d'un identifiant renseigné
    entry: entrée PyKeePass
    """
    try:
        totp = subprocess.check_output(
            "totp.sh "+entry.otp, shell=True
        ).decode('utf-8').replace("\n", "")
    except:
        totp = None
    entry_result = {}
    if entry.username != None:
        entry_result["nom d'utilisateur"] = entry.username

    if entry.password != None:
        entry_result["mot de passe"] = "*"*len(entry.password)

    if totp != None:
        entry_result["totp"] = totp
    return entry_result

def get_pass(entry):
    return entry.password
