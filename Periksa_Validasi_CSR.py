from subprocess import run, CalledProcessError
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename as pilih_file
from getpass import getpass
from colorama import Fore, Back

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file agar perintah OpenSSL dapat dijalankan")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    DIREKTORI_FILE_CSR = pilih_file(title = "*Pilih file CSR (Certificate Signing Requests)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
    if DIREKTORI_FILE_CSR:
        PERINTAH = f"openssl req -in \"{DIREKTORI_FILE_CSR}\" -verify -noout"
        print(f"Menjalankan perintah {Fore.BLACK}{Back.LIGHTYELLOW_EX}{PERINTAH}{Fore.RESET}{Back.RESET} ...")
        try:
            run(PERINTAH, shell = True, check = True)
        except CalledProcessError:
            print(f"{Fore.LIGHTRED_EX}CSR \"{DIREKTORI_FILE_CSR}\" tidak valid!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTGREEN_EX}CSR \"{DIREKTORI_FILE_CSR}\" valid{Fore.RESET}")
        try:
            getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
        except KeyboardInterrupt:
            pass
    else:
        print(f"{Fore.LIGHTRED_EX}File CSR tidak dipilih!{Fore.RESET}")