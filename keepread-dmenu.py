#!/usr/bin/env python3
from pykeepass import PyKeePass as pkp
import subprocess

path=""
print("Chemin vers la base de données : "+path)

if path == "":
    print("Veuillez editer la variable path avec le chemin vers votre base de données dans le fichier keepread.py.")
    quit()


def copy(text):
    text = str(text)
    p = subprocess.Popen(['xclip', '-selection', "clip"], stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text.encode('utf-8'))

def dmenu_show(args,items):
    try:
        proc = subprocess.Popen(
            args,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    except OSError as err:
        print("erreur lors du lancement de dmenu")

    with proc.stdin:
        for item in items:
            proc.stdin.write(item)
            proc.stdin.write('\n')

    if proc.wait() == 0:
        return proc.stdout.read().rstrip('\n')

    stderr = proc.stderr.read()

    if stderr == '':
        quit()

def show_entries(temp):
    name = dmenu_show(["dmenu", "-l", "10", "-p", "identifiants"], temp)
    return name



try:
    r=dmenu_show(["dmenu", "-p", "mot de passe", "-P"],"")
    kp = pkp(path, password=r)
except:
    print("Mot de passe erroné.")
    quit()

e = kp.find_entries(title=".*", regex=True)
temp = []
for i in e:
    field = str(i).replace("/", " ").strip().split()
    temp.append(field[2])
name = show_entries(temp)
while True:
    if name == "":
        quit()
    else:
        entry = kp.find_entries(title=name, first=True)
    if entry == None:
        print("Identifiant invalide.")
        quit()
    entry_values = ["Mot de passe : "+entry.password, "Identifiant : "+entry.username, "supprimer", "retour"]
    r = dmenu_show(["dmenu", "-l", "10", "-p", name], entry_values)
    if r == "retour":
        name = show_entries(temp)
    elif r == "supprimer":
        r = dmenu_show(["dmenu", "-l", "10", "-p", "Êtes-vous sûr de vouloir supprimer "+name+" ?"], ["oui", "non"])
        if r == "oui":
            kp.delete_entry(entry)
        name = show_entries(temp)
    else:
        copy(r.split(" ")[-1])
        proc = subprocess.Popen(["notify-send", r+" copié."])
        quit()
