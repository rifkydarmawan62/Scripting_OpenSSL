from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file
from tkinter.messagebox import showerror
from colorama import Fore, Back
from getpass import getpass

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file agar perintah OpenSSL dapat dijalankan")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    DIREKTORI_FILE = pilih_file(title = "*Pilih file untuk validasi kunci private", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Personal Information Exchange", "*.pvk"), ("Semua File", "*.*")])
    if DIREKTORI_FILE:
        PERINTAH = f"openssl pkey -check -in \"{DIREKTORI_FILE}\""
        print(f"Menjalankan perintah {Fore.BLACK}{Back.LIGHTYELLOW_EX}{PERINTAH}{Fore.RESET}{Back.RESET} ...")
        try:
            run(PERINTAH, shell = True, check = True)
        except CalledProcessError:
            print(f"{Fore.RED}Kunci private \"{DIREKTORI_FILE}\" tidak valid!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTGREEN_EX}Kunci private \"{DIREKTORI_FILE}\" valid{Fore.RESET}")
        try:
            getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
        except KeyboardInterrupt:
            pass
    else:
        print(f"{Fore.LIGHTRED_EX}File tidak dipilih!{Fore.RESET}")