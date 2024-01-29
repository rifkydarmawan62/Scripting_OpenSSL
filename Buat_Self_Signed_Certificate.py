from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from subprocess import run, CalledProcessError
from colorama import Fore, Back
from os.path import exists
from os import getcwd, remove
from .modul import bersihkan_layar

bersihkan_layar(f"{Fore.YELLOW}Memeriksa Instalasi OpenSSL ...{Fore.RESET}")
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
                DIREKTORI_FILE_CSR = pilih_file(title = "*Pilih file Certificate Signing Requests (CSR)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
                if DIREKTORI_FILE_CSR:
                    PERINTAH_VALIDASI_CSR = f"openssl req -in \"{DIREKTORI_FILE_CSR}\" -verify -noout"
                    print(f"{Fore.YELLOW}Menjalankan perintah validasi {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH_VALIDASI_CSR}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                    try:
                        run(PERINTAH_VALIDASI_CSR, shell = True, check = True)
                    except CalledProcessError:
                        print(f"{Fore.LIGHTRED_EX}CSR tidak valid!{Fore.RESET}")
                    else:
                        print(f"{Fore.LIGHTGREEN_EX}CSR valid!\n{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
                        DIREKTORI_FILE_SERTIFIKAT = simpan_file(title = "*Pilih lokasi file Self Signed Certificate disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], initialfile = ".pem", initialdir = "/".join(DIREKTORI_FILE_CSR.split("/")[:-1]), defaultextension = ".pem", confirmoverwrite = True)
                        if DIREKTORI_FILE_SERTIFIKAT:
                            DIREKTORI_FILE_KONFIGURASI = f"{getcwd().replace("\\", "/")}/konfigurasi.cnf"
                            with open(f"{getcwd().replace("\\", "/")}/index.txt", "w") as file_database:
                                pass
                            with open(DIREKTORI_FILE_KONFIGURASI, "w") as file_konfigurasi:
                                file_konfigurasi.write(f"""[ ca ]
default_ca      = CA_default

[ CA_default ]
dir            = {getcwd().replace("\\", "/")}
database       = $dir/index.txt
new_certs_dir  = $dir

certificate    = none
serial         = $dir/nomor_sertifikat
rand_serial    = yes
private_key    = {DIREKTORI_FILE_KUNCI_PRIVATE}
default_days   = 1000 #kustom bebas melalui script Python
default_crl_days= 30
default_md     = sha256
policy         = policy_anything
email_in_dn    = no
name_opt       = ca_default
cert_opt       = ca_default
copy_extensions = none

[ policy_anything ]
countryName            = optional
stateOrProvinceName    = optional
organizationName       = optional
organizationalUnitName = optional
commonName             = optional
emailAddress           = optional""")
                            PERINTAH = f"openssl ca -verbose -in \"{DIREKTORI_FILE_CSR}\" -out \"{DIREKTORI_FILE_SERTIFIKAT}\" -config \"{DIREKTORI_FILE_KONFIGURASI}\" -keyfile \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -selfsign"
                            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                            try:
                                run(PERINTAH, shell = True, check = True)
                            except CalledProcessError:
                                print(f"{Fore.LIGHTRED_EX}Self signed certificate gagal dibuat!{Fore.RESET}")
                                if exists(DIREKTORI_FILE_SERTIFIKAT):
                                    remove(DIREKTORI_FILE_SERTIFIKAT)
                            else:
                                print(f"{Fore.LIGHTGREEN_EX}Self signed certificate dibuat di direktori \"{DIREKTORI_FILE_SERTIFIKAT}\"{Fore.RESET}")
                        else:
                            print(f"{Fore.LIGHTRED_EX}File self signed certificate tidak disimpan!{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTRED_EX}File CSR tidak dipilih!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup!{Fore.RESET}")