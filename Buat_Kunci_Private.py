from getpass import getpass
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror
from colorama import Fore, Back
from subprocess import run, CalledProcessError
from os.path import exists
from os import remove

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file agar perintah OpenSSL dapat dijalankan")
else:
    try:
        print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
        DIREKTORI_FILE_KUNCI_PRIVATE = asksaveasfilename(title = "*Lokasi file kunci private disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", initialfile = ".pem", confirmoverwrite = True)
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            PERINTAH = f"openssl genrsa -f4 -out \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -verbose"
            print(f"Menjalankan perintah {Fore.BLACK}{Back.LIGHTYELLOW_EX}{PERINTAH}{Fore.RESET}{Back.RESET} ...")
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
        try:
            getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
        except KeyboardInterrupt:
            pass
    except KeyboardInterrupt:
        showerror("Error!", "Interupsi Keyboard Ctrl + C!\nProgram ditutup")