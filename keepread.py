#!/usr/bin/env python3
from pykeepass import PyKeePass as pkp
import sys
import getpass
import subprocess

#Variable à éditer
path=""
print(path)

if path == "":
    print("Veuillez editer la variable path avec le chemin vers votre base de données dans le fichier keepread.py.")
    quit()

if len(sys.argv) == 1:
    print("Vous devez renseigner le nom de l'identifiant dont vous souhaitez obtenir les informations.\nPour obtenir la liste des identifiants, faire keepread.py -l")
    quit()

while True:
    r=getpass.getpass("mot de passe : ")
    try:
        kp = pkp(path, password=r)
        break
    except:
        print("Mot de passe erroné.")
        continue

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

def del_entry(arg):
    entry = kp.find_entries(title=arg, first=True)
    try:
        kp.delete_entry(entry)
        print("l'id. a bien été supprimé.")
    except:
        print("erreur lors de la suppression de l'id.")
    quit()

def print_entries():
    e = kp.find_entries(title=".*", regex=True)
    temp = ""
    j = 0
    for i in e:
        field = str(i).replace("/", " ").strip().split()
        if field[1] != '"Corbeille':
            temp += field[2]+" | "
            j+=1
            if j == 10:
                temp+="\n"
                j = 0
    print(temp)

if sys.argv[1] == "-l":
    print_entries()
    r = input("Nom de l'id. ( q = quitter ) : ")
    if r == "q":
        quit()
    entry = new_entry(r)
elif sys.argv[1] == "-d" and len(sys.argv) == 3:
    r = input("Êtes-vous sûr de vouloir supprimer l'id. "+sys.argv[2]+" ? (o/n) ")
    if r == "o":
        del_entry(sys.argv[2])
else:
    entry = new_entry(sys.argv[1])

while True:
    try:
        totp = subprocess.check_output("totp.sh "+entry.get_custom_property("otp"), shell=True).decode('utf-8').replace("\n", "")
    except:
        totp = "Pas de TOTP"
    print("m : copier mot de passe (",entry.password,")\n\
n : copier nom d'utilisateur (",entry.username,")\n\
r : séléctionner un autre id.\n\
l : lister les id.\n\
t : totp (",totp,") \n\
d : supprimer l'entrée \n\
q : quitter.")
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
    elif r == "t":
        copy(totp)
    elif r == "l":
        print_entries()
    elif r == "d":
        del_entry(entry.username)
