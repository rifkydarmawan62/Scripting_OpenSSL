from tkinter.filedialog import asksaveasfilename as simpan_file
from colorama import Fore, Back
from subprocess import run, CalledProcessError
from os.path import exists
from os import remove
from .modul import bersihkan_layar

bersihkan_layar(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        DIREKTORI_FILE_KUNCI_PRIVATE = simpan_file(title = "*Lokasi file kunci private disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", initialfile = ".pem", confirmoverwrite = True)
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            PERINTAH = f"openssl genrsa -f4 -out \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -verbose"
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(PERINTAH, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Kunci private gagal dibuat!{Fore.RESET}")
                if exists(DIREKTORI_FILE_KUNCI_PRIVATE):
                    remove(DIREKTORI_FILE_KUNCI_PRIVATE)
            else:
                print(f"{Fore.LIGHTGREEN_EX}Kunci private berhasil dibuat di direktori \"{DIREKTORI_FILE_KUNCI_PRIVATE}\"{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak disimpan!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup!{Fore.RESET}")