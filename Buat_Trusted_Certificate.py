from getpass import getpass
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from subprocess import run, CalledProcessError
from colorama import Fore
from tkinter.messagebox import showerror
from os.path import exists
from os import remove

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.LIGHTBLUE_EX}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file executable pada environment variable agar perintah OpenSSL dapat dijalankan")
else:
    try:
        print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
        DIREKTORI_FILE_SERTIFIKAT = pilih_file(title = "*Pilih file self signed certificate", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rule", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_SERTIFIKAT:
            DIREKTORI_FILE_SERTIFIKAT_TRUSTED = simpan_file(title = "*Pilih lokasi file trusted certificate disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", confirmoverwrite = True, initialfile = ".pem", initialdir = "/".join(DIREKTORI_FILE_SERTIFIKAT.split("/")[:-1]))
            if DIREKTORI_FILE_SERTIFIKAT_TRUSTED:
                PERINTAH = f"openssl x509 -in \"{DIREKTORI_FILE_SERTIFIKAT}\" -out \"{DIREKTORI_FILE_SERTIFIKAT_TRUSTED}\" -trustout -text"
                print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH}] ...{Fore.LIGHTBLUE_EX}")
                try:
                    run(PERINTAH, shell = True, check = True)
                except CalledProcessError:
                    print(f"{Fore.LIGHTRED_EX}Gagal membuat trusted certificate!")
                    if exists(DIREKTORI_FILE_SERTIFIKAT_TRUSTED):
                        remove(DIREKTORI_FILE_SERTIFIKAT_TRUSTED)
                try:
                    getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
                except KeyboardInterrupt:
                    pass
            else:
                print(f"{Fore.LIGHTRED_EX}File trusted certificate tidak disimpan!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File self signed certificate tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\n{Fore.RESET}Program ditutup!")