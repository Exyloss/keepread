#!/usr/bin/env python3
from pykeepass import PyKeePass as pkp
import sys
import pyperclip as pc
import dmenu2 as d

try:
    r=d.show(["dmenu", "-p", "mot de passe", "-P"],"")
    kp = pkp("/home/antonin/media/keepass/keepass3.kdbx", password=r)
except:
    print("Mot de passe erroné.")
    quit()

def show_entries(temp):
    name = d.show(["dmenu", "-l", "10", "-p", "identifiants"], temp)
    return name

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
    entry_values = ["retour", "Mot de passe : "+entry.password, "Identifiant : "+entry.username]
    r = d.show(["dmenu", "-l", "10", "-p", name], entry_values)
    if r == "retour":
        name = show_entries(temp)
    else:
        pc.copy(r.split(" ")[-1])
        quit()
