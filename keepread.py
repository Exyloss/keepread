#!/usr/bin/env python3
from pykeepass import PyKeePass as pkp
from random import randint
import sys
import getpass
import subprocess
import keyring
import argparse
import os
from configparser import ConfigParser


config = ConfigParser()
parser = argparse.ArgumentParser(description='Lecteur de BDD Keepass en ligne de commande')
parser.add_argument('title', metavar='N', type=str, nargs='?',
                    help='nom de l\'entrée à rechercher')
parser.add_argument('--password', metavar='N', type=str, nargs='?',
                    help='mot de passe')
parser.add_argument('--username', metavar='N', type=str, nargs='?',
                    help='nom d\'utilisateur')
parser.add_argument('--list', action='store_true', help='liste le nom des entrées disponibles')
def copy(text):
    text = str(text)
    p = subprocess.Popen(['xclip', '-selection', "clip"],
                         stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text.encode('utf-8'))

def pass_gen():
    choice = "n"
    while choice == "n":
        chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        inp = input("Inclure les caractères spéciaux ? (o/n) ")
        if inp == "o":
            chars += "&?,.;/:!#@+-*/=_()[]çàéè~"
        len_chars=len(chars)
        try:
            inp = int(input("Longueur du mot de passe (12 par défaut) : "))
            len_pass = inp
        except:
            len_pass=12
        passwd=""
        for i in range(len_pass):
            passwd += chars[randint(0,len_chars-1)]
        inp = input(passwd+" : Ce mot de passe vous convient-il ? (o/n) ")
        if inp == "o":
            choice = "o"
    return passwd


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

def create_entry():
    groups = kp.groups
    temp = "| "
    print("Groupes disponibles : ")
    for i in groups:
        temp += i.name+" | "
        if len(temp.split("\n")[-1]) >= 80:
            temp+="\n"
    print(temp)
    g = input("Groupe de l'entrée : ")
    g = kp.find_groups(name=g, first=True)
    if g == None:
        g = kp.root_group
        print("Erreur, groupe inconnu, utilisation du groupe racine.")
    t = input("Titre de l'entrée : ")
    while t == "":
        t = input("Titre de l'entrée : ")
    r = input("Nom d'utilisateur : ")
    if r == "":
        r = "Non-renseigné"
    s = input("Mot de passe : ")
    if s == "":
        inp = input("Souhaitez-vous utiliser un mot de passe aléatoire ? (o/n) ")
        if inp == "o":
            s = pass_gen()
        else:
            s = "Non-renseigné"
    kp.add_entry(g, t, r, s)
    kp.save()
    print("Entrée créée.")

def print_entries():
    e = kp.find_entries(title=".*", regex=True)
    temp = ""
    j = 0
    for i in e:
        if i.group.name != 'Corbeille':
            temp += i.title+" | "
            j+=len(i.title)+3
            if j >= 80:
                temp+="\n"
                j = 0
    print(temp)

def print_help():
    print("m : copier mot de passe\n\
u : copier nom d'utilisateur\n\
r : séléctionner un autre identifiant\n\
l : lister les identifiants\n\
t : copier le code totp \n\
d : supprimer l'entrée \n\
a : afficher le mot de passe \n\
e : éditer cette entrée \n\
n : créer une nouvelle entrée \n\
h : afficher cette aide \n\
q : quitter.")

def print_entry(entry):
    try:
        totp = subprocess.check_output(
            "totp.sh "+entry.get_custom_property("otp"), shell=True
        ).decode('utf-8').replace("\n", "")
    except:
        totp = None
    if entry.username == None:
        usr = "Non-renseigné"
    else:
        usr = entry.username

    if entry.password == None:
        passwd = ""
    else:
        passwd = entry.password

    if totp == None:
        print("\033[4m"+entry.title+"\033[0m")
        print("Nom d'utilisateur : "+usr+"\nMot de passe : "+"*"*len(passwd))
    else:
        print("\033[4m"+entry.title+"\033[0m")
        print("Nom d'utilisateur : "+usr+"\nMot de passe : "+"*"*len(passwd)+"\nTOTP : "+totp)

config.read(os.environ["XDG_CONFIG_HOME"]+"/keepread/config.ini")
path = config["conf"]["path"]
key = config["conf"]["keyring"]

if path == "":
    print("Veuillez editer la variable path avec le chemin vers votre base de données dans le fichier keepread.py.")
    quit()

if key == "True":
    try:
        passwd = keyring.get_password("system", "keepass")
        kp = pkp(path, password=passwd)
    except:
        try:
            keyring.set_password("system", "keepass", passwd)
            passwd = keyring.get_password("system", "keepass")
            kp = pkp(path, password=passwd)
        except:
            passwd = None
else:
    passwd = None

if passwd == None:
    while True:
        passwd=getpass.getpass("mot de passe : ")
        try:
            kp = pkp(path, password=passwd)
            break
        except:
            print("Mot de passe erroné.")
            continue

args = parser.parse_args()

if args.username != None:
    entry = new_entry(args.username)
    print(entry.username)
    quit()
elif args.password != None:
    entry = new_entry(args.password)
    print(entry.password)
    quit()
elif args.list == True:
    e = kp.find_entries(title=".*", regex=True)
    for i in e:
        if i.group.name != 'Corbeille':
            print(i.title)
    quit()

if args.title != None:
    try:
        entry = new_entry(args.title)
    except:
        print_entries()
        r = input("Nom de l'id. ( q = quitter ) : ")
        entry = new_entry(r)
else:
    print_entries()
    r = input("Nom de l'id. ( q = quitter ) : ")
    entry = new_entry(r)


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
    elif r == "u":
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
    elif r == "n":
        create_entry()
        print_entry(entry)
    elif r == "d":
        confirm = input("Êtes-vous sûr de vouloir supprimer l'id. "+entry.title+" ? (o/n) : ")
        if confirm == "o":
            del_entry(entry)
            print_entries()
            r = input("Nom de l'id. : ")
            entry = new_entry(r)
            print_entry(entry)
    elif r == "h" or r == "help":
        print_help()
