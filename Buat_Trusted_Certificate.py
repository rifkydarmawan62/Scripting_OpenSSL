from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from subprocess import run, CalledProcessError
from colorama import Fore, Back
from os.path import exists
from os import remove
from modul import bersihkan_layar

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        DIREKTORI_FILE_SERTIFIKAT = pilih_file(title = "*Pilih file self signed certificate", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rule", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_SERTIFIKAT:
            DIREKTORI_FILE_SERTIFIKAT_TRUSTED = simpan_file(title = "*Pilih lokasi file trusted certificate disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", confirmoverwrite = True, initialfile = ".pem", initialdir = "/".join(DIREKTORI_FILE_SERTIFIKAT.split("/")[:-1]))
            if DIREKTORI_FILE_SERTIFIKAT_TRUSTED:
                PERINTAH = f"openssl x509 -in \"{DIREKTORI_FILE_SERTIFIKAT}\" -out \"{DIREKTORI_FILE_SERTIFIKAT_TRUSTED}\" -trustout -text"
                print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                try:
                    run(PERINTAH, shell = True, check = True)
                except CalledProcessError:
                    print(f"{Fore.LIGHTRED_EX}Trusted certificate gagal dibuat!{Fore.RESET}")
                    if exists(DIREKTORI_FILE_SERTIFIKAT_TRUSTED):
                        remove(DIREKTORI_FILE_SERTIFIKAT_TRUSTED)
                else:
                    print(f"{Fore.LIGHTGREEN_EX}File trusted certificate dibuat di direktori \"{DIREKTORI_FILE_SERTIFIKAT_TRUSTED}\"{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}File trusted certificate tidak disimpan!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File self signed certificate tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup!{Fore.RESET}")