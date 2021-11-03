#!/usr/bin/env python3
import subprocess
def copy(text):
    text = str(text)
    p = subprocess.Popen(['xclip', '-selection', "clip"],
                         stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text.encode('utf-8'))
