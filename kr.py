#!/usr/bin/env python3
from keeplib import *
import keyring
import argparse
import os
from getpass import getpass
from configparser import ConfigParser

parser = argparse.ArgumentParser(description="Lecteur de base de données keepass.")
parser.add_argument("--password", action="store_true",
        help="obtenir le mot de passe de l'entrée recherchée")
parser.add_argument("--username", action="store_true",
        help="obtenir le nom d'utilisateur de l'entrée à rechercher")
parser.add_argument("title", metavar="entrée", type=str, nargs="?",
        help="nom de l'entrée à rechercher")
args = parser.parse_args()

config = ConfigParser()
config.read(os.environ["XDG_CONFIG_HOME"]+"/keepread/config.ini")
path = config["conf"]["path"]
key = config["conf"]["keyring"]

if key == "True":
    pw = keyring.get_password("system", "keepass")
else:
    pw = getpass("mot de passe:")

kp = pkp(path, password=pw)
pw = ""

if args.title != None:
    entry = search_entry(kp, args.title)
else:
    entry = 1

if args.username or args.password:
    if entry != 1:
        if args.username:
            print(entry.username)
        if args.password:
            print(entry.password)
        quit()
    else:
        quit(1)

entries = get_entries(kp)

while True:
    if entry != 1:
        vals = entry_values(entry)
        for i in vals:
            print(i+":"+vals[i])
        while True:
            r = input(":")
            if r == "q":
                quit()
            elif r == "h":
                print("aide:")
                print("a: afficher les informations sur l'entrée sélectionnée")
                print("u: copier le nom d'utilisateur")
                print("m: copier le mot de passe")
                print("t: copier le code totp")
                print("r: sélectionner une nouvelle entrée")
                print("n: créer une nouvelle entrée")
                print("d: supprimer l'entrée")
                print("q: quitter")
            elif r == "u":
                copy(vals["nom d'utilisateur"])
            elif r == "m":
                copy(vals["mot de passe"])
            elif r == "t":
                if "totp" in vals.keys():
                    copy(entry_values(entry)["totp"])
                else:
                    print("erreur, il n'y a pas de totp sur cette entrée.")
            elif r == "r":
                entry_title = prompt_sel(entries)
                entry = search_entry(kp, entry_title)
                break
            elif r == "d":
                print("êtes-vous sûr de vouloir supprimer cette entrée ?")
                confirm = prompt_sel(["oui", "non"])
                if confirm == "oui":
                    exit_code = del_entry(kp, entry)
                    if exit_code == 0:
                        print("l'entrée a bien été supprimée.")
                        entry = 1
                        break
                    else:
                        print("erreur lors de la suppression de l'entrée.")
                else:
                    print("l'entrée n'a pas été supprimée.")
            elif r == "n":
                groups = get_groups(kp)
                group = prompt_sel(groups)
                if group == -1: pass
                title = input("titre (laisser vide pour annuler):")
                if title == "": pass
                username = input("nom d'utilisateur:")
                if username == "": pass
                passwd = input("mot de passe:")
                if passwd == "": pass
                create_entry(kp, group, title, username, passwd)
                entries = get_entries(kp)
            elif r == "a":
                for i in vals:
                    print(i+":"+vals[i])

    else:
        print("sélectionner une entrée:")
        entry_title = prompt_sel(entries)
        if entry_title in entries:
            entry = search_entry(kp, entry_title)
        elif entry_title == -1:
            break
        else:
            pass
