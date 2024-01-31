from tkinter.filedialog import asksaveasfilename as simpan_file
from colorama import Fore, Back
from subprocess import run, CalledProcessError
from os.path import exists
from os import remove
from modul import bersihkan_layar
from tkinter.messagebox import askyesnocancel, askyesno

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        OUTPUT_KUNCI_PRIVATE = simpan_file(title = "*Lokasi file kunci private disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", initialfile = ".pem", confirmoverwrite = True)
        if OUTPUT_KUNCI_PRIVATE:
            GUNAKAN_PUBLIK_EKSPONENT = askyesnocancel("Gunakan publik eksponent?", "\"Ya\" untuk publik eksponent 3\n\"Tidak\" untuk publik eksponent 65537\n\"Batal\" untuk tidak menggunakan publik eksponent")
            if GUNAKAN_PUBLIK_EKSPONENT:
                perintah = "openssl genrsa -3 "
            elif GUNAKAN_PUBLIK_EKSPONENT == False:
                perintah = "openssl genrsa -f4 "
            else:
                perintah = "openssl genrsa "
            chiper = input("Pilih enkripsi chiper opsional [aes128 | aes192 | aes256 | camellia128 | camellia192 | camellia256 | des | des3 | idea] : ").strip().lower()
            if chiper in ("aes128", "aes192", "aes256", "camellia128", "camellia192", "camellia256", "des", "des3", "idea"):
                perintah += f"-{chiper} "
            elif chiper != "":
                print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            if askyesno("Konfirmasi jenis PKCS (Public Key Cryptography Standards)", "Gunakan format tradisional PKCS#1 bukan format PKCS#8?"):
                perintah += "-traditional "
            perintah += f"-out \"{OUTPUT_KUNCI_PRIVATE}\" -verbose "
            try:
                UKURAN_BIT = int(input("Masukkan ukuran bit kunci private (default = 2048) [> 512] : "))
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
            else:
                if UKURAN_BIT > 512:
                    perintah += f"{UKURAN_BIT}"
                else:
                    print(f"{Fore.LIGHTRED_EX}Ukuran bit harus lebih dari 512!{Fore.RESET}")
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(perintah, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Kunci private gagal dibuat!{Fore.RESET}")
                if exists(OUTPUT_KUNCI_PRIVATE):
                    remove(OUTPUT_KUNCI_PRIVATE)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Kunci private batal dibuat!{Fore.RESET}")
                if exists(OUTPUT_KUNCI_PRIVATE):
                    remove(OUTPUT_KUNCI_PRIVATE)
            else:
                print(f"{Fore.LIGHTGREEN_EX}Kunci private berhasil dibuat!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak disimpan!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C!\nProgram ditutup!{Fore.RESET}")