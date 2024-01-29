from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file
from colorama import Fore, Back
from os.path import exists
from os import remove
from .modul import bersihkan_layar

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    FILE_INPUT = pilih_file(title = "*Pilih file untuk dikonversi ke format .pem", filetypes = [("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
    if FILE_INPUT:
        DIREKTORI_FOLDER = "/".join(FILE_INPUT.split("/")[:-1])
        NAMA_FILE = ".".join(FILE_INPUT.split("/")[-1].split(".")[:-1]) if "." in FILE_INPUT.split("/")[-1] else FILE_INPUT.split("/")[-1]
        FILE_OUTPUT = f"{DIREKTORI_FOLDER}/{NAMA_FILE}.pem"
        PERINTAH = f"openssl pkey -in \"{FILE_INPUT}\" -out \"{FILE_OUTPUT}\" -outform PEM"
        print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
        try:
            run(PERINTAH, shell = True, check = True)
        except CalledProcessError:
            print(f"{Fore.LIGHTRED_EX}Konversi kunci ke file .pem gagal!{Fore.RESET}")
            if exists(FILE_OUTPUT):
                remove(FILE_OUTPUT)
        else:
            print(f"{Fore.LIGHTGREEN_EX}Kunci telah dikonversi ke file .pem{Fore.RESET}")
    else:
        print(f"{Fore.LIGHTRED_EX}File tidak dipilih!{Fore.RESET}")