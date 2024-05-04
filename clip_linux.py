import subprocess

ENCODING = 'utf-8'

def copy_xclip(text):
    text = str(text)
    p = subprocess.Popen(['xclip', '-selection', selection],
        stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text.encode(ENCODING))

def paste_xclip():
    p = subprocess.Popen(['xclip', '-selection', selection, '-o'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    stdout, stderr = p.communicate()
    return stdout.decode(ENCODING)

def copy_wl(text):
        text = str(text)
        args = ["wl-copy"]
        if not text:
            args.append('--clear')
            subprocess.check_call(args, close_fds=True)
        else:
            pass
            p = subprocess.Popen(args, stdin=subprocess.PIPE, close_fds=True)
            p.communicate(input=text.encode(ENCODING))

def paste_wl(primary=False):
        args = ["wl-paste", "-n"]
        if primary:
            args.append(PRIMARY_SELECTION)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, close_fds=True)
        stdout, _stderr = p.communicate()
        return stdout.decode(ENCODING)
