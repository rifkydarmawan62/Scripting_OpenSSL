from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from subprocess import run, CalledProcessError
from colorama import Fore, Back
from os.path import exists
from os import remove
from modul import bersihkan_layar

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        DIREKTORI_FILE_KUNCI_PRIVATE = pilih_file(title = "*Pilih file kunci private", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            PERINTAH_VALIDASI = f"openssl pkey -check -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -noout"
            print(f"{Fore.YELLOW}Menjalankan perintah validasi {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH_VALIDASI}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(PERINTAH_VALIDASI, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Kunci private tidak valid!{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Kunci private valid!\n{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
                DIREKTORI_FILE_SERTIFIKAT = pilih_file(title = "*Pilih file self signed certificate", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
                if DIREKTORI_FILE_SERTIFIKAT:
                    DIREKTORI_FILE_SERTIFIKAT_PFX = simpan_file(title = "*Pilih lokasi file sertifikat Personal Information Exchange disimpan", filetypes = [("Personal Information Exchange", "*.pfx")], defaultextension = ".pfx", confirmoverwrite = True, initialfile = ".pfx")
                    if DIREKTORI_FILE_SERTIFIKAT_PFX:
                        PERINTAH = f"openssl pkcs12 -export -inkey \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -in \"{DIREKTORI_FILE_SERTIFIKAT}\" -out \"{DIREKTORI_FILE_SERTIFIKAT_PFX}\""
                        print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                        try:
                            run(PERINTAH, shell = True, check = True)
                        except CalledProcessError:
                            print(f"{Fore.LIGHTRED_EX}Sertifikat Personal Information Exchange gagal dibuat!{Fore.RESET}")
                            if exists(DIREKTORI_FILE_SERTIFIKAT_PFX):
                                remove(DIREKTORI_FILE_SERTIFIKAT_PFX)
                        else:
                            print(f"{Fore.LIGHTGREEN_EX}File sertifikat Personal Information Exchange disimpan di direktori \"{DIREKTORI_FILE_SERTIFIKAT_PFX}\"{Fore.RESET}")
                    else:
                        print(f"{Fore.LIGHTRED_EX}File sertifikat Personal Information Exchange tidak disimpan!{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTRED_EX}File self signed certificate tidak dipilih!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup!{Fore.RESET}")