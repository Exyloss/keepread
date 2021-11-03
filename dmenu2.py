#!/usr/bin/env python3
import re
import subprocess

def show(args,items):
# start the dmenu process
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
        return None


