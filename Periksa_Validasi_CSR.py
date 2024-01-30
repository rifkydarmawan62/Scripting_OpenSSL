from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file
from colorama import Fore, Back
from modul import bersihkan_layar

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    DIREKTORI_FILE_CSR = pilih_file(title = "*Pilih file CSR (Certificate Signing Requests)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
    if DIREKTORI_FILE_CSR:
        PERINTAH = f"openssl req -in \"{DIREKTORI_FILE_CSR}\" -verify -noout"
        print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
        try:
            run(PERINTAH, shell = True, check = True)
        except CalledProcessError:
            print(f"{Fore.LIGHTRED_EX}CSR tidak valid!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTGREEN_EX}CSR valid{Fore.RESET}")
    else:
        print(f"{Fore.LIGHTRED_EX}File CSR tidak dipilih!{Fore.RESET}")