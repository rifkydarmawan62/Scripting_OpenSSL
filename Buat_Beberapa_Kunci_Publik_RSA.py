from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
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
                print(f"{Fore.LIGHTRED_EX}Kunci Private Tidak Valid!{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Kunci Private Valid!\n{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
                DIREKTORI_FILE_KUNCI_PUBLIK_RSA = simpan_file(title = "*Pilih lokasi file kunci publik disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der")], defaultextension = ".pem", initialdir = "/".join(DIREKTORI_FILE_KUNCI_PRIVATE.split("/")[:-1]), confirmoverwrite = True, initialfile = ".pem")
                if DIREKTORI_FILE_KUNCI_PUBLIK_RSA:
                    while True:
                        try:
                            jumlah_kunci_publik_rsa = int(input(f"{Fore.RESET}Masukkan jumlah kunci publik RSA [> 0] : ").strip())
                        except ValueError:
                            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
                        else:
                            if jumlah_kunci_publik_rsa >= 0:
                                break
                            else:
                                print(f"{Fore.LIGHTRED_EX}Angka tidak boleh bilangan negatif!{Fore.RESET}")
                    if jumlah_kunci_publik_rsa == 1:
                        PERINTAH = f"openssl pkey -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -out \"{DIREKTORI_FILE_KUNCI_PUBLIK_RSA}\" -outform {DIREKTORI_FILE_KUNCI_PUBLIK_RSA[-3:].upper()} -RSAPublicKey_out"
                        print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                        try:
                            run(PERINTAH, shell = True, check = True)
                        except CalledProcessError:
                            print(f"{Fore.LIGHTRED_EX}Gagal membuat kunci publik!{Fore.RESET}")
                            if exists(DIREKTORI_FILE_KUNCI_PUBLIK_RSA):
                                remove(DIREKTORI_FILE_KUNCI_PUBLIK_RSA)
                        else:
                            print(f"{Fore.LIGHTGREEN_EX}Kunci publik dibuat di direktori \"{DIREKTORI_FILE_KUNCI_PUBLIK_RSA}\"{Fore.RESET}")
                    elif jumlah_kunci_publik_rsa > 1:
                        DIREKTORI_FILE = "/".join(DIREKTORI_FILE_KUNCI_PUBLIK_RSA.split("/")[:-1])
                        NAMA_FILE = ".".join(DIREKTORI_FILE_KUNCI_PUBLIK_RSA.split("/")[-1].split(".")[:-1])
                        JENIS_FILE = DIREKTORI_FILE_KUNCI_PUBLIK_RSA.split(".")[-1]
                        for urutan_kunci in range(jumlah_kunci_publik_rsa):
                            PERINTAH = f"openssl pkey -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -out \"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE}\" -outform {JENIS_FILE.upper()} -RSAPublicKey_out"
                            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                            try:
                                run(PERINTAH, shell = True, check = True)
                            except CalledProcessError:
                                print(f"{Fore.LIGHTRED_EX}Gagal membuat kunci publik!{Fore.RESET}")
                                if exists(f"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE}"):
                                    remove(f"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE}")
                                break
                            else:
                                print(f"{Fore.LIGHTGREEN_EX}Kunci publik berhasil dibuat di direktori \"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE}\"{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTRED_EX}File kunci publik tidak disimpan!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup!{Fore.RESET}")