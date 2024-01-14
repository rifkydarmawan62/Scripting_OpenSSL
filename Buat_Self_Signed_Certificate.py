from getpass import getpass
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from subprocess import run, CalledProcessError
from colorama import Fore
from tkinter.messagebox import showerror
from os import getcwd

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.LIGHTBLUE_EX}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file executable pada environment variable agar perintah OpenSSL dapat dijalankan")
else:
    try:
        print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
        DIREKTORI_FILE_KUNCI_PRIVATE = pilih_file(title = "*Pilih file kunci private", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            try:
                run(f"openssl pkey -check -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\"", shell = True, check = True, capture_output = True)
            except CalledProcessError:
                print(f"{Fore.RED}File kunci private \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" tidak valid!{Fore.RESET}")
            else:
                DIREKTORI_FILE_CSR = pilih_file(title = "*Pilih file Certificate Signing Requests (CSR)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
                if DIREKTORI_FILE_CSR:
                    try:
                        run(f"openssl req -in \"{DIREKTORI_FILE_CSR}\" -verify -noout", shell = True, check = True, capture_output = True)
                    except CalledProcessError:
                        print(f"{Fore.LIGHTRED_EX}File CSR \"{DIREKTORI_FILE_CSR}\" tidak valid!{Fore.RESET}")
                    else:
                        DIREKTORI_FILE_SERTIFIKAT = simpan_file(title = "*Pilih lokasi file Self Sign Certificate disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], initialfile = ".pem", initialdir = "/".join(DIREKTORI_FILE_CSR.split("/")[:-1]), defaultextension = ".pem", confirmoverwrite = True)
                        if DIREKTORI_FILE_SERTIFIKAT:
                            DIREKTORI_FILE_KONFIGURASI = f"{getcwd()}/konfigurasi.cnf"
                            with open(f"{getcwd()}/index.txt", "w") as file_database:
                                pass
                            with open(DIREKTORI_FILE_KONFIGURASI, "w") as file_konfigurasi:
                                file_konfigurasi.write(f"""[ ca ]
default_ca      = CA_default

[ CA_default ]
dir            = {getcwd()}
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
                            print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH}] ...{Fore.LIGHTBLUE_EX}")
                            try:
                                run(PERINTAH, shell = True, check = True)
                            except CalledProcessError:
                                print(f"{Fore.LIGHTRED_EX}Gagal membuat CA!")
                            try:
                                getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
                            except KeyboardInterrupt:
                                pass
                        else:
                            print(f"{Fore.LIGHTRED_EX}File CA tidak disimpan!{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTRED_EX}File CSR tidak dipilih!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\n{Fore.RESET}Program ditutup!")