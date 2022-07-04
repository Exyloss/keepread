#!/usr/bin/env python3
from keeplib import *
import keyring
import argparse

def pyfzf(items):
    if items != "":
        try:
            proc = subprocess.Popen(
                ["fzy"],
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        except OSError as err:
            print("erreur lors du lancement de fzy")

        with proc.stdin:
            if isinstance(items, list):
                for item in items:
                    proc.stdin.write(item)
                    proc.stdin.write('\n')
            elif isinstance(items, str):
                proc.stdin.write(items)
    else:
        return -1

    if proc.wait() == 0:
        return proc.stdout.read().rstrip('\n')

    stderr = proc.stderr.read()

    if stderr == '':
        return -1

parser = argparse.ArgumentParser(description="Lecteur de base de données keepass.")
parser.add_argument("--password", action="store_true",
        help="obtenir le mot de passe de l'entrée recherchée")
parser.add_argument("--username", action="store_true",
        help="obtenir le nom d'utilisateur de l'entrée à rechercher")
parser.add_argument("title", metavar="entrée", type=str, nargs="?",
        help="nom de l'entrée à rechercher")
args = parser.parse_args()

kp = pkp("/home/antonin/media/keepass/keepass3.kdbx", password=keyring.get_password("system", "keepass"))

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
                entry_title = pyfzf(entries)
                entry = search_entry(kp, entry_title)
                break
            elif r == "d":
                print("êtes-vous sûr de vouloir supprimer cette entrée ?")
                confirm = pyfzf(["oui", "non"])
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
                group = pyfzf(groups)
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
        print("")
        entry_title = pyfzf(entries)
        if entry_title in entries:
            entry = search_entry(kp, entry_title)
        elif entry_title == -1:
            break
        else:
            pass
