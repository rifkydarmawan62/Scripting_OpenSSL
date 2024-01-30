from colorama import Fore, Back
from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file
from os.path import exists
from os import remove
from modul import bersihkan_layar

#Sertifikat dalam format .der dapat diinstall oleh sistem operasi Windows

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        DIREKTORI_FILE_SERTIFIKAT = pilih_file(title = "*Pilih file self signed certificate", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_SERTIFIKAT:
            DIREKTORI_FOLDER = "/".join(DIREKTORI_FILE_SERTIFIKAT.split("/")[:-1])
            NAMA_FILE = ".".join(DIREKTORI_FILE_SERTIFIKAT.split("/")[-1].split(".")[:-1]) if "." in DIREKTORI_FILE_SERTIFIKAT.split("/")[-1] else DIREKTORI_FILE_SERTIFIKAT.split("/")[-1]
            PERINTAH = f"openssl x509 -in \"{DIREKTORI_FILE_SERTIFIKAT}\" -out \"{DIREKTORI_FOLDER}/{NAMA_FILE}.der\" -outform DER"
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(PERINTAH, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Konversi sertifikat ke file .der gagal!{Fore.RESET}")
                if exists(f"{DIREKTORI_FOLDER}/{NAMA_FILE}.der"):
                    remove(f"{DIREKTORI_FOLDER}/{NAMA_FILE}.der")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Sertifikat telah dikonversi ke file .der{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File sertifikat tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup!{Fore.RESET}")