from platform import system
from subprocess import run

def bersihkan_layar(teks : str | None = None):
    if system() == "Windows":
        run("cls", shell = True)
    else:
        run("clear", shell = True)
    if teks:
        print(teks)