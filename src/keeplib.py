#!/usr/bin/env python3
from pykeepass import PyKeePass as pkp
from random import randint
import subprocess

def copy(text):
    text = str(text)
    p = subprocess.Popen(['xclip', '-selection', "clip"],
                         stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text.encode('utf-8'))
    return 0

def prompt_sel(args,items):
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

def pass_gen(size=12, spe=False):
    try:
        chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if spe:
            chars += "&?,.;/:!#@+-*/=_()[]çàéè~"
        len_chars=len(chars)
        passwd = ""
        for i in range(size):
            passwd += chars[randint(0,len_chars-1)]
        return passwd
    except:
        return 1


def search_entry(kp, arg):
    entry = kp.find_entries(title=arg, first=True)
    if entry == None:
        return 1
    else:
        return entry


def del_entry(kp, entry):
    try:
        kp.delete_entry(entry)
        kp.save()
        return 0
    except:
        return 1

def edit_entry(kp, entry, uname, passwd, title):
    try:
        kp.add_entry(entry.group, title, uname, passwd)
        kp.delete_entry(entry)
        kp.save()
        return 0
    except:
        return 1

def create_entry(kp, group, title, uname, passwd):
    try:
        g = kp.find_groups(name=group, first=True)
        if g == None:
            g = kp.root_group
        kp.add_entry(g, title, uname, passwd)
        kp.save()
        return 0
    except:
        return 1

def get_entries(kp):
    e = kp.find_entries(title=".*", regex=True)
    entries = []
    for i in e:
        if i.group.name != 'Corbeille' and i.title != None:
            entries.append(i.title)
    return entries

def get_groups(kp):
    e = kp.find_groups(name=".*", regex=True)
    entries = []
    for i in e:
        if i.name != 'Corbeille':
            entries.append(i.name)
    return entries

def entry_values(entry):
    try:
        totp = subprocess.check_output(
            "totp.sh "+entry.otp, shell=True
        ).decode('utf-8').replace("\n", "")
    except:
        totp = None
    entry_result = {}
    if entry.username != None:
        entry_result["nom d'utilisateur"] = entry.username

    if entry.password != None:
        entry_result["mot de passe"] = entry.password

    if totp != None:
        entry_result["totp"] = totp
    return entry_result
