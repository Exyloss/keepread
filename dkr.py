#!/usr/bin/env python3
import subprocess
import keyring
import os
from pynput.keyboard import Controller
from keeplib import *
from configparser import ConfigParser

def write_str(string):
    for i in string:
        keyboard.press(i)

def dmenu_show(args,items):
    if items != "":
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

def show_entries(temp, prompt=""):
    name = dmenu_show(["dmenu", "-l", "10", "-p", prompt], temp)
    return name

keyboard = Controller()

config = ConfigParser()
config.read(os.environ["XDG_CONFIG_HOME"]+"/keepread/config.ini")
path = config["conf"]["path"]
key = config["conf"]["keyring"]

if bool(key):
    pw = keyring.get_password("system", "keepass")

kp = pkp(path, password=pw)

entries = get_entries(kp)
while True:
    entry_title = show_entries(entries, "entrées:")
    if entry_title in entries:
        entry = search_entry(kp, entry_title)
        entry_vals = entry_values(entry)
        entry_vals = [i+":"+entry_vals[i] for i in entry_vals]
        entry_vals.append("éditer l'entrée")
        entry_vals.append("supprimer l'entrée")
        while True:
            val = show_entries(entry_vals, "données:")
            if val != -1 and val != "supprimer l'entrée"and val != "éditer l'entrée":
                val = ":".join(val.split(":")[1:])
                write_str(val)
            elif val == "supprimer l'entrée":
                confirm = show_entries(["oui", "non"], "supprimer l'entrée:")
                if confirm == "oui":
                    del_entry(kp, entry)
                    entries = get_entries(kp)
                    break
            elif val == "éditer l'entrée":
                val_edit = show_entries(["titre", "nom d'utilisateur", "mot de passe"], "valeur à éditer:")
                new_val = show_entries(" ", "nouveau "+val_edit+":")
                confirm = show_entries(["oui", "non"], "éditer l'entrée:")
                if confirm != "oui":
                    break
                if val_edit == "titre":
                    edit_entry(kp, entry, entry.username, entry.password, new_val)
                elif val_edit == "nom d'utilisateur":
                    edit_entry(kp, entry, new_val, entry.password, entry.title)
                elif val_edit == "mot de passe":
                    edit_entry(kp, entry, entry.username, new_val, entry.title)
                entries = get_entries(kp)
                break
            elif val == -1:
                break
    elif entry_title == -1:
        quit()
    else:
        title = show_entries(" ", "titre de l'entrée:")
        if title == -1: pass
        group = show_entries(get_groups(kp), "groupe de l'entrée:")
        if group == -1: pass
        username = show_entries(" ", "nom d'utilisateur:")
        if username == -1: pass
        passwd = show_entries(" ", "mot de passe:")
        if passwd == -1: pass
        confirm = show_entries(["oui", "non"], "créer l'entrée:")
        if confirm == "oui":
            create_entry(kp, group, title, username, passwd)
        entries = get_entries(kp)
