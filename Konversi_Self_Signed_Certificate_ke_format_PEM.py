from colorama import Fore, Back
from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file
from tkinter.messagebox import showerror
from getpass import getpass
from os.path import exists
from os import remove

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file executable pada environment variable agar perintah OpenSSL dapat dijalankan")
else:
    try:
        print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
        DIREKTORI_FILE_SERTIFIKAT = pilih_file(title = "*Pilih file self signed certificate", filetypes = [("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_SERTIFIKAT:
            DIREKTORI_FOLDER = "/".join(DIREKTORI_FILE_SERTIFIKAT.split("/")[:-1])
            NAMA_FILE = ".".join(DIREKTORI_FILE_SERTIFIKAT.split("/")[-1].split(".")[:-1]) if "." in DIREKTORI_FILE_SERTIFIKAT.split("/")[-1] else DIREKTORI_FILE_SERTIFIKAT.split("/")[-1]
            PERINTAH = f"openssl x509 -in \"{DIREKTORI_FILE_SERTIFIKAT}\" -out \"{DIREKTORI_FOLDER}/{NAMA_FILE}.pem\" -outform PEM"
            print(f"Menjalankan perintah {Fore.BLACK}{Back.LIGHTYELLOW_EX}{PERINTAH}{Fore.RESET}{Back.RESET} ...")
            try:
                run(PERINTAH, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Konversi sertifikat ke file .pem gagal!{Fore.RESET}")
                if exists(f"{DIREKTORI_FOLDER}/{NAMA_FILE}.pem"):
                    remove(f"{DIREKTORI_FOLDER}/{NAMA_FILE}.pem")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Sertifikat telah dikonversi ke file .pem{Fore.RESET}")
            try:
                getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
            except KeyboardInterrupt:
                pass
        else:
            print(f"{Fore.LIGHTRED_EX}File sertifikat tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup{Fore.RESET}")