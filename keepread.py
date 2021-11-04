#!/usr/bin/env python3
from pykeepass import PyKeePass as pkp
import sys
import getpass
import subprocess

path=""
print(path)

if path == "":
    print("Veuillez editer la variable path avec le chemin vers votre base de données dans le fichier keepread.py.")
    quit()

if len(sys.argv) == 1:
    print("Vous devez renseigner le nom de l'identifiant dont vous souhaitez obtenir les informations.\nPour obtenir la liste des identifiants, faire keepread.py -l")
    quit()

try:
    r=getpass.getpass("mot de passe : ")
    kp = pkp(path, password=r)
except:
    print("Mot de passe erroné.")
    quit()

def copy(text):
    text = str(text)
    p = subprocess.Popen(['xclip', '-selection', "clip"],
                         stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text.encode('utf-8'))

def new_entry(arg):
    entry = kp.find_entries(title=arg, first=True)
    if entry == None:
        print("Erreur, l'id. n'existe pas, vous pouvez les lister avec la commande keepread.py -l")
        quit()
    return entry

if sys.argv[1] == "-l":
    e = kp.find_entries(title=".*", regex=True)
    temp = ""
    for i in e:
        field = str(i).replace("/", " ").strip().split()
        temp += "\n"+field[2]
    print(temp)
    r = input("Nom de l'id. ( q = quitter ) : ")
    if r == "q":
        quit()
    entry = new_entry(r)
elif sys.argv[1] == "-d" and len(sys.argv) == 3:
    r = input("Êtes-vous sûr de vouloir supprimer l'id. "+sys.argv[2]+" ? (o/n) ")
    if r == "o":
        kp.delete_entry(entry)
        print("l'id. a bien été supprimé.")
    quit()
else:
    entry = new_entry(sys.argv[1])

while True:
    print("m : copier mot de passe (",entry.password,")\nn : copier nom d'utilisateur (",entry.username,")\nr : séléctionner un autre id.\nl : lister les id.\nq : quitter.")
    r = input(":")
    if r == "q":
        break
    elif r == "m":
        copy(entry.password)
    elif r == "n":
        copy(entry.username)
    elif r == "r":
        r = input("Nom de l'id. : ")
        entry = new_entry(r)
    elif r == "l":
        e = kp.find_entries(title=".*", regex=True)
        temp = ""
        for i in e:
            field = str(i).replace("/", " ").strip().split()
            temp += "\n"+field[2]
        print(temp)
