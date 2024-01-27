from getpass import getpass
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from subprocess import run, CalledProcessError
from colorama import Fore, Back
from tkinter.messagebox import showerror
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
        DIREKTORI_FILE_KUNCI_PRIVATE = pilih_file(title = "*Pilih file kunci private", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            try:
                run(f"openssl pkey -check -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\"", shell = True, check = True, capture_output = True)
            except CalledProcessError:
                print(f"{Fore.RED}File kunci private \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" tidak valid!{Fore.RESET}")
            else:
                DIREKTORI_FILE_SERTIFIKAT = pilih_file(title = "*Pilih file self signed certificate", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
                if DIREKTORI_FILE_SERTIFIKAT:
                    DIREKTORI_FILE_SERTIFIKAT_PFX = simpan_file(title = "*Pilih lokasi file sertifikat Personal Information Exchange disimpan", filetypes = [("Personal Information Exchange", "*.pfx")], defaultextension = ".pfx", confirmoverwrite = True, initialfile = ".pfx")
                    if DIREKTORI_FILE_SERTIFIKAT_PFX:
                        PERINTAH = f"openssl pkcs12 -export -inkey \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -in \"{DIREKTORI_FILE_SERTIFIKAT}\" -out \"{DIREKTORI_FILE_SERTIFIKAT_PFX}\""
                        print(f"Menjalankan perintah {Fore.BLACK}{Back.LIGHTYELLOW_EX}{PERINTAH}{Fore.RESET}{Back.RESET} ...")
                        try:
                            run(PERINTAH, shell = True, check = True)
                        except CalledProcessError:
                            print(f"{Fore.LIGHTRED_EX}Sertifikat Personal Information Exchange gagal dibuat!{Fore.RESET}")
                            if exists(DIREKTORI_FILE_SERTIFIKAT_PFX):
                                remove(DIREKTORI_FILE_SERTIFIKAT_PFX)
                        else:
                            print(f"{Fore.LIGHTGREEN_EX}File sertifikat Personal Information Exchange disimpan di direktori \"{DIREKTORI_FILE_SERTIFIKAT_PFX}\"{Fore.RESET}")
                        try:
                            getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
                        except KeyboardInterrupt:
                            pass
                    else:
                        print(f"{Fore.LIGHTRED_EX}File sertifikat Personal Information Exchange tidak disimpan!{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTRED_EX}File self signed certificate tidak dipilih!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\n{Fore.RESET}Program ditutup!")