#!/usr/bin/env python3
from pykeepass import PyKeePass as pkp
import sys
import getpass
import subprocess

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
            print_entries()
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
    r = input("Nom de l'id. : ")
    entry = new_entry(r)
    print_entry(entry)

def edit_entry(entry):
    r=""
    print("Que souhaitez-vous faire ?")
    print("1) éditer le nom d'utilisateur\n\
2) éditer le mot de passe\n\
3) éditer le titre de l'entrée\n\
q) quitter l'éditeur\n")
    while r != "1" and r != "2" and r != "3" and r != "q":
        r = input(":")
        if r == "1":
            try:
                s = input("Nouveau nom d'utilisateur : ")
                kp.add_entry(entry.group, entry.title, s, entry.password)
                kp.delete_entry(entry)
                kp.save()
                print("L'entrée a bien été modifiée.")
            except:
                print("Erreur lors de la modification de l'entrée.")
        elif r == "2":
            try:
                s = getpass.getpass("Nouveau mot de passe : ")
                kp.add_entry(entry.group, entry.title, entry.username, s)
                kp.delete_entry(entry)
                kp.save()
                print("L'entrée a bien été modifiée.")
            except:
                print("Erreur lors de la modification de l'entrée.")
        elif r == "3":
            try:
                s = input("Nouveau titre de l'entrée : ")
                kp.add_entry(entry.group, s, entry.username, entry.password)
                kp.delete_entry(entry)
                kp.save()
                print("L'entrée a bien été modifiée.")
            except:
                print("Erreur lors de la modification de l'entrée.")
    print_entries()
    r = input("Nom de l'id. : ")
    entry = new_entry(r)
    print_entry(entry)


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
a : afficher le mot de passe \n\
e : éditer cette entrée \n\
h : afficher cette aide \n\
q : quitter.")

def print_entry(entry):
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
        print("Nom d'utilisateur : "+entry.username+"\nMot de passe : "+"*"*len(entry.password)+"\nTOTP : "+totp)

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


if len(sys.argv) == 1:
    print_entries()
    r = input("Nom de l'id. ( q = quitter ) : ")
    if r == "q":
        quit()
    entry = new_entry(r)
else:
    entry = new_entry(sys.argv[1])

print_entry(entry)
while True:
    try:
        totp = subprocess.check_output(
            "totp.sh "+entry.get_custom_property("otp"), shell=True
        ).decode('utf-8').replace("\n", "")
    except:
        totp = None
    r = input(":")
    if r == "q":
        break
    elif r == "m":
        copy(entry.password)
        print("Mot de passe copié.")
    elif r == "n":
        copy(entry.username)
        print("Nom d'utilisateur copié.")
    elif r == "r":
        r = input("Nom de l'id. : ")
        entry = new_entry(r)
        print_entry(entry)
    elif r == "t":
        if totp != None:
            totp = subprocess.check_output(
                "totp.sh "+entry.get_custom_property("otp"), shell=True
            ).decode('utf-8').replace("\n", "")
            copy(totp)
            print("TOTP copié.")
        else:
            print("Cet identifiant ne contient pas de code TOTP.")
    elif r == "l":
        print_entries()
    elif r == "a":
        print(entry.password)
    elif r == "e":
        edit_entry(entry)
    elif r == "d":
        confirm = input("Êtes-vous sûr de vouloir supprimer l'id. "+entry.title+" ? (o/n) : ")
        if confirm == "o":
            del_entry(entry)
    elif r == "h" or r == "help":
        print_help()
