from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from tkinter.messagebox import showerror
from getpass import getpass
from colorama import Fore, Back
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
        DIREKTORI_FILE_KUNCI_PRIVATE = pilih_file(title = "*Pilih file kunci private", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            DIREKTORI_FILE_KUNCI_PUBLIK = simpan_file(title = "*Pilih lokasi file kunci publik disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der")], defaultextension = ".pem", initialdir = "/".join(DIREKTORI_FILE_KUNCI_PRIVATE.split("/")[:-1]), confirmoverwrite = True, initialfile = ".pem")
            if DIREKTORI_FILE_KUNCI_PUBLIK:
                while True:
                    try:
                        jumlah_kunci_publik = int(input(f"{Fore.RESET}Masukkan jumlah kunci publik [> 0] : ").strip())
                    except ValueError:
                        print(f"{Fore.LIGHTRED_EX}Input harus berupa angka{Fore.RESET}")
                    else:
                        if jumlah_kunci_publik >= 0:
                            break
                        else:
                            print(f"{Fore.LIGHTRED_EX}Angka tidak boleh bilangan negatif!{Fore.RESET}")
                if jumlah_kunci_publik == 1:
                    PERINTAH = f"openssl pkey -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -pubout -out \"{DIREKTORI_FILE_KUNCI_PUBLIK}\" -outform {DIREKTORI_FILE_KUNCI_PUBLIK[-3:].upper()}"
                    print(f"Menjalankan perintah {Fore.BLACK}{Back.LIGHTYELLOW_EX}{PERINTAH}{Fore.RESET}{Back.RESET} ...")
                    try:
                        run(PERINTAH, shell = True, check = True)
                    except CalledProcessError:
                        print(f"{Fore.LIGHTRED_EX}Gagal membuat kunci publik!{Fore.RESET}")
                        if exists(DIREKTORI_FILE_KUNCI_PUBLIK):
                            remove(DIREKTORI_FILE_KUNCI_PUBLIK)
                    else:
                        print(f"{Fore.LIGHTGREEN_EX}Kunci publik berhasil dibuat di direktori \"{DIREKTORI_FILE_KUNCI_PUBLIK}\"{Fore.RESET}")
                elif jumlah_kunci_publik > 1:
                    DIREKTORI_FILE = "/".join(DIREKTORI_FILE_KUNCI_PUBLIK.split("/")[:-1])
                    NAMA_FILE = ".".join(DIREKTORI_FILE_KUNCI_PUBLIK.split("/")[-1].split(".")[:-1])
                    JENIS_FILE = DIREKTORI_FILE_KUNCI_PUBLIK.split(".")[-1]
                    for urutan_kunci in range(jumlah_kunci_publik):
                        PERINTAH = f"openssl pkey -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -pubout -out \"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE}\" -outform {JENIS_FILE.upper()}"
                        print(f"Menjalankan perintah {Fore.BLACK}{Back.LIGHTYELLOW_EX}{PERINTAH}{Fore.RESET}{Back.RESET} ...")
                        try:
                            run(PERINTAH, shell = True, check = True)
                        except CalledProcessError:
                            print(f"{Fore.LIGHTRED_EX}Gagal membuat kunci publik!{Fore.RESET}")
                            if exists(f"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE}"):
                                remove(f"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE}")
                            break
                        else:
                            print(f"{Fore.LIGHTGREEN_EX}Kunci publik berhasil dibuat di direktori \"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE}\"{Fore.RESET}")
                try:
                    getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
                except KeyboardInterrupt:
                    pass
            else:
                print(f"{Fore.LIGHTRED_EX}File kunci publik tidak disimpan!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup!{Fore.RESET}")