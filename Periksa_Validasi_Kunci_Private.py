from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file
from tkinter.messagebox import showerror
from colorama import Fore
from getpass import getpass

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.LIGHTBLUE_EX}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file agar perintah OpenSSL dapat dijalankan")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
    DIREKTORI_FILE = pilih_file(title = "*Pilih file untuk validasi konsistensi kunci", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Personal Information Exchange", "*.pvk"), ("Semua File", "*.*")])
    if DIREKTORI_FILE:
        PERINTAH = f"openssl pkey -check -in \"{DIREKTORI_FILE}\""
        print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH}] ...{Fore.LIGHTBLUE_EX}")
        try:
            run(PERINTAH, shell = True, check = True)
        except CalledProcessError:
            print(f"{Fore.RED}File kunci private \"{DIREKTORI_FILE}\" tidak valid!")
        try:
            getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
        except KeyboardInterrupt:
            pass
    else:
        print(f"{Fore.LIGHTRED_EX}File tidak dipilih!{Fore.RESET}")