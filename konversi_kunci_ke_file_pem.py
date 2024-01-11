from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file
from tkinter.messagebox import showerror
from colorama import Fore
from getpass import getpass
from os.path import exists
from os import remove

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.LIGHTBLUE_EX}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file agar perintah OpenSSL dapat dijalankan")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
    FILE_INPUT = pilih_file(title = "*Pilih file untuk dikonversi ke format .pem", filetypes = [("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
    if FILE_INPUT:
        DIREKTORI_FOLDER = "/".join(FILE_INPUT.split("/")[:-1])
        NAMA_FILE = ".".join(FILE_INPUT.split("/")[-1].split(".")[:-1]) if "." in FILE_INPUT.split("/")[-1] else FILE_INPUT.split("/")[-1]
        FILE_OUTPUT = f"{DIREKTORI_FOLDER}/{NAMA_FILE}.pem"
        PERINTAH = f"openssl pkey -in \"{FILE_INPUT}\" -out \"{FILE_OUTPUT}\" -outform PEM"
        print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH}] ...{Fore.LIGHTBLUE_EX}")
        try:
            run(PERINTAH, shell = True, check = True)
        except CalledProcessError:
            print(f"{Fore.LIGHTRED_EX}Konversi kunci ke file .pem gagal")
            if exists(FILE_OUTPUT):
                remove(FILE_OUTPUT)
        try:
            getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
        except KeyboardInterrupt:
            pass
    else:
        print(f"{Fore.LIGHTRED_EX}File tidak dipilih!{Fore.RESET}")