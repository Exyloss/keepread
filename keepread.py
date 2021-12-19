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
        if arg == "q":
            quit()
        else:
            r = input("Erreur, l'id. n'existe pas.\nnom de l'id. : ")
            return new_entry(r)
    else:
        return entry

def del_entry(entry):
    try:
        kp.delete_entry(entry)
        print("l'id. a bien été supprimé.")
        kp.save()
    except:
        print("erreur lors de la suppression de l'id.")
    quit()

def print_entries():
    e = kp.find_entries(title=".*", regex=True)
    temp = ""
    j = 0
    for i in e:
        if i.group != 'Corbeille':
            temp += i.title+" | "
            j+=len(i.title)+3
            if j >= 80:
                temp+="\n"
                j = 0
    print(temp)

def print_help():
    print("m : copier mot de passe\n\
n : copier nom d'utilisateur\n\
r : séléctionner un autre identifiant\n\
l : lister les identifiants\n\
t : copier le code totp \n\
d : supprimer l'entrée \n\
h : afficher cette aide \n\
q : quitter.")

if len(sys.argv) == 1 or sys.argv[1] == "-l":
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
        totp = subprocess.check_output(
            "totp.sh "+entry.get_custom_property("otp"), shell=True
        ).decode('utf-8').replace("\n", "")
    except:
        totp = None
    if totp == None:
        print("\033[4m"+entry.title+"\033[0m")
        print("Nom d'utilisateur : "+entry.username+"\nMot de passe : "+"*"*len(entry.password))
    else:
        print("\033[4m"+entry.title+"\033[0m")
        print("Nom d'utilisateur : "+entry.username+"\nMot de passe : "+"*"*len(entry.password)+"\n TOTP : "+totp)
    r = input(":")
    if r == "q":
        break
    elif r == "m":
        copy(entry.password)
    elif r == "n":
        copy(entry.username)
    elif r == "r":
        print_entries()
        r = input("Nom de l'id. : ")
        entry = new_entry(r)
    elif r == "t":
        totp = subprocess.check_output(
            "totp.sh "+entry.get_custom_property("otp"), shell=True
        ).decode('utf-8').replace("\n", "")
        copy(totp)
    elif r == "l":
        print_entries()
    elif r == "d":
        confirm = input("Êtes-vous sûr de vouloir supprimer l'id. "+entry.title+" ? (o/n) : ")
        if confirm == "o":
            del_entry(entry)
    elif r == "h" or r == "help":
        print_help()
