#!/usr/bin/env python3
import subprocess
import keyring
import os
from keeplib import *
from configparser import ConfigParser
import pyperclip
from clip_linux import *

def copy(text):
    if graphic == 'wayland':
        copy_wl(text)
    else:
        copy_xclip(text)
    return True

def write_str(string):
    if graphic == 'xorg':
        os.system("xdotool type '"+string.replace("'", "\'")+"'")
    elif graphic == 'wayland':
        os.system("wtype '"+string.replace("'", "\'")+"'")

def show_entries(temp, prompt=""):
    print(menu+" "+prompt)
    name = prompt_sel((menu+" "+prompt).split(" "), temp)
    return name

config = ConfigParser()
config.read(os.environ["XDG_CONFIG_HOME"]+"/keepread/config.ini")
path    = config["conf"]["path"]
key     = config["conf"]["keyring"]
graphic = config["conf"]["graphic"]
menu    = config["conf"]["menu"]

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
            if val != -1 and val != "supprimer l'entrée" and val != "éditer l'entrée" and 'mot de passe' not in val:
                val = ":".join(val.split(":")[1:])
                write_str(val)
            elif val != -1 and 'mot de passe' in val:
                write_str(entry.password)
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
